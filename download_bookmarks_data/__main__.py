import json
import logging
import os

from .auth import authorize_user, set_twitter_user_id
from .get_bookmarks import build_bookmarks_list
from .get_references import get_referenced_tweets
from .get_media import get_media
from . import globals
from .logs import setup_logger

if __name__ == '__main__':

	os.mkdir(globals.PATH)
	log = setup_logger(globals.NAME)

	globals.TWITTER_USER_ID = set_twitter_user_id()
	globals.BEARER_TOKEN = authorize_user()

	all_bookmarks = build_bookmarks_list()
	with open(f'{globals.PATH}/bookmarks.json', 'w', encoding='utf-8') as fd:
		fd.write(json.dumps(list(all_bookmarks), indent=2, sort_keys=True, default=lambda o: o.__dict__))

	log.info('Fetching all tweets referenced by bookmarks...')
	all_referenced_tweets = get_referenced_tweets(all_bookmarks)
	with open(f'{globals.PATH}/referenced_tweets.json', 'w', encoding='utf-8') as fd:
		fd.write(json.dumps(list(all_referenced_tweets), indent=2, sort_keys=True, default=lambda o: o.__dict__))

	media_path = f'{globals.PATH}/media'
	os.mkdir(media_path)
	log.info('Dowloading media for bookmarked tweets...')
	get_media(media_path, all_bookmarks)
	log.info('Dowloading media for referenced tweets...')
	get_media(media_path, all_referenced_tweets)

	log.info('All done!')

