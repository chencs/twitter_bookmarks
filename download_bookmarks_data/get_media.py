import requests
import re

def download_media(path, media_key, url):
	filetype = re.search('^.+(\.[A-Za-z0-9]+)\??.*', url)
	if filetype is None:
		raise Exception(f'tried to download file without extension: {media_key}, {url}')
	extension = filetype.group(1)
	r = requests.get(url)
	if r.status_code != 200:
		raise Exception(f'error downloading photos: status code {r.status_code}, json: {r.json()}')
	with open(f'{path}/{media_key}{extension}', 'wb') as fd:
		for chunk in r.iter_content(chunk_size=128):
			fd.write(chunk)

def get_media(path, tweets, media_type=None):
	for tweet in tweets:
		for m in tweet.attachments.get('media', []):
			if media_type is None or m.type == media_type:
				download_media(path, m.key, m.url)
