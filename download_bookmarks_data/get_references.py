import logging
import requests

from .twitter_types import Tweet
from .helpers import with_retries_and_error_handling
from .globals import NAME

log = logging.getLogger(NAME)

@with_retries_and_error_handling
def fetch_tweets_by_ids(tweet_ids, headers={}):
	log.info(f'Fetching reference tweets {", ".join(tweet_ids)}')
	if len(tweet_ids) > 100:
		raise Exception("cannot fetch more than 100 tweets at a time")

	path = 'https://api.twitter.com/2/tweets'

	data = {
		"ids": ",".join(tweet_ids),
		"tweet.fields":"created_at",
		"expansions": "attachments.media_keys,attachments.poll_ids,author_id,referenced_tweets.id",
		"poll.fields": "options,end_datetime,voting_status",
		"media.fields": "media_key,type,url,variants"
		}
	resp = requests.get(path, headers=headers, data=data)
	return resp


'''
get_referenced_tweets fetches all tweets that are referenced by bookmarked tweets (and 
any tweets referenced by _those_ tweets, etc).
'''
def get_referenced_tweets(bookmarks, already_fetched_refs=set()):
	# TODO: Ensure exclusivity in fetching repeated reference tweets
	MAX_FETCH = 100
	all_fetched = bookmarks.union(already_fetched_refs)
	all_ids = [t.id for t in all_fetched]
	refs = [t for ts in map(
		lambda t: t.referenced_tweets, filter(lambda r: (
			r.referenced_tweets is not None
			# and r.in_reply_to_user_id != r.author_id
			), all_fetched)
		) for t in ts]
	ids_to_fetch = []
	for ref in refs:
		if ref['id'] not in all_ids:
			ids_to_fetch.append(ref['id'])

	if len(ids_to_fetch) == 0:
		log.info(f'Fetched {len(already_fetched_refs)} referenced tweets.')
		return already_fetched_refs

	i = 0
	fetched_tweets = []
	while i*MAX_FETCH < len(ids_to_fetch):
		start = i*MAX_FETCH
		end = (i+1)*MAX_FETCH
		fetched = fetch_tweets_by_ids(ids_to_fetch[start:end]).json()
		fetched_tweets += [Tweet(tweet, fetched.get("includes", {})) for tweet in fetched.get('data')]
		i += 1

	return get_referenced_tweets(bookmarks, already_fetched_refs=already_fetched_refs.union(fetched_tweets))

