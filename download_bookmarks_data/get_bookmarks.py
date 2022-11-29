import logging
import requests
import time

from .twitter_types import Tweet
from .helpers import with_retries_and_error_handling
from . import globals

MAX_PER_PAGE = 100
log = logging.getLogger(globals.NAME)

def end_of_bookmarks(page_resp):
	return (page_resp.get('meta', {}).get('result_count') == 0
			and 'next_token' not in page_resp.get('meta'))

def build_bookmarks_list():
	log.info("Getting all bookmarks...")
	next_page_token = None
	bookmarks = set()
	first = True

	while first or next_page_token is not None:
		first = False
		time.sleep(1)
		current_page = get_bookmark_page(next_page_token).json()
		bookmarks.update([Tweet(tweet, current_page.get("includes", {})) for tweet in current_page.get("data", [])])
		if end_of_bookmarks(current_page):
			log.info(f'Fetched {len(bookmarks)} bookmarks')
			return bookmarks
		next_page_token = current_page.get('meta', {}).get('next_token', None)
	return bookmarks

@with_retries_and_error_handling
def get_bookmark_page(pagination_token, request_count=0, headers={}):
	path = f'https://api.twitter.com/2/users/{globals.TWITTER_USER_ID}/bookmarks'
	data = {
		"max_results": MAX_PER_PAGE, 
		"pagination_token": pagination_token,
		"expansions": "attachments.media_keys,attachments.poll_ids,author_id,referenced_tweets.id",
		"tweet.fields": "conversation_id,in_reply_to_user_id,created_at",
		"poll.fields": "options,end_datetime,voting_status",
		"media.fields": "media_key,type,url,variants"
		}

	r = requests.get(path, headers=headers, data=data)
	return r