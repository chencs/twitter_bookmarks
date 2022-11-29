import logging
import time 
import requests
import re

from . import globals

log = logging.getLogger(globals.NAME)

def with_retries_and_error_handling(f, max_retries=15):
	def wrapper(*args, **kwargs):
		headers =  {"Authorization" : f'Bearer {globals.BEARER_TOKEN}'}
		for retry_count in range(max_retries):
			resp = f(*args, **kwargs, headers=headers)
			if resp.status_code == 200 and 'data' not in resp.json():
				metadata = resp.json().get('meta', {})
				if 'previous_token' in metadata and 'next_token' not in metadata:
					break
				log.info(f'Retrying ({retry_count+1} of {max_retries})...')
				log.debug(resp.json())
				time.sleep(1*retry_count)
				continue
			else:
				break
		if resp.status_code == 401:
			log.critical(f'Unauthorized. Check your auth credentials')
		if resp.json().get('errors'):
			raise Exception(f'Error retrieving Twitter data: {resp.json()}')
		return resp
	return wrapper



def sub_expanded_link(text):
	tco_regex = 'https://t\.co\/[A-Za-z0-9]+'
	if not text:
		return None
	tco_url = re.search(tco_regex, text)
	if tco_url:
		return re.sub(tco_regex, expand_tco_link(tco_url.group()), text)
	
	return text

def expand_tco_link(url):
	# Uhh hopefully this never breaks lol
	r = requests.get(url)
	return r.url
