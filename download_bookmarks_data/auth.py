import base64
import hashlib
import logging
import os
import re
import json
import requests

from requests.auth import AuthBase, HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from .globals import NAME, Colors

log = logging.getLogger(NAME)
client_id = os.getenv('GET_BOOKMARKS_CLIENT_ID')
client_secret = os.getenv('GET_BOOKMARKS_CLIENT_SECRET')

# Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
redirect_uri = "https://www.twitter.com"

# Set the scopes
scopes = ["bookmark.read", "tweet.read", "users.read"]

# Create a code verifier
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

# Create a code challenge
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

# Start an OAuth 2.0 session
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

# Create an authorize URL
auth_url = "https://twitter.com/i/oauth2/authorize"
authorization_url, state = oauth.authorization_url(
    auth_url, code_challenge=code_challenge, code_challenge_method="S256"
)


def authorize_user():
	# Visit the URL to authorize your App to make requests on behalf of a user
	print(
	"Open the following URL in a browser to authorize this app on behalf of your Twitter handle:"
	)
	print(f'{Colors.CYAN}{authorization_url}{Colors.RESET}')

	# Paste in your authorize URL to complete the request
	authorization_response = input(
	    "Paste in the full URL from the browser after you've authorized your App: "
	)

	# Fetch your access token
	token_url = "https://api.twitter.com/2/oauth2/token"

	# The following line of code will only work if you are using a type of App that is a public client
	auth = HTTPBasicAuth(client_id, client_secret)

	log.info('Fetching access token...')

	token = oauth.fetch_token(
	    token_url=token_url,
	    authorization_response=authorization_response,
	    auth=auth,
	    client_id=client_id,
	    include_client_id=True,
	    code_verifier=code_verifier,
	)

	# Your access token
	return token["access_token"]


def set_twitter_user_id():
	print('You can use https://tweeterid.com/ to find your Twitter user ID.')
	return input(f'{Colors.CYAN}Enter your Twitter user ID: {Colors.RESET}').strip()