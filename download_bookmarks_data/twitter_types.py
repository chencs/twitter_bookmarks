import json
from .helpers import sub_expanded_link

class Media:
	def __init__(self, dataObj):
		if 'media_key' not in dataObj:
			raise Exception('no media key provided')
		self.key = dataObj.get('media_key')
		self.type = dataObj.get('type')
		if self.type == 'photo':
			self.url = dataObj.get('url')
		if self.type == 'video' or self.type == 'animated_gif':
			if len(dataObj.get('variants', [])) > 1:
				mp4s = filter(lambda v: v.get('content_type') == 'video/mp4', dataObj.get('variants',[]))
				mp4 = max(mp4s, key=lambda m: m.get('bit_rate'))
				self.url = mp4.get('url')
			else:
				self.url = dataObj['variants'][0].get('url')


class Poll:
	def __init__(self, dataObj):
		if 'id' not in dataObj:
			raise Exception('no id provided')
		self.id = dataObj.get('id')
		self.options = dataObj.get('options', None)
		self.end_time = dataObj.get('end_datetime', None)
		self.voting_status = dataObj.get('voting_status', None)


class Tweet:
	def __init__(self, dataObj, includesObj=None):
		if "id" not in dataObj:
			raise Exception("no id provided")
		self.id = dataObj.get("id")
		self.author_id = dataObj.get("author_id", None)
		self.created_at = dataObj.get("created_at", None)
		self.text = sub_expanded_link(dataObj.get('text', None))
		self.conversation_id = dataObj.get('conversation_id', None)
		self.in_reply_to_user_id = dataObj.get('in_reply_to_user_id', None)
		self.referenced_tweets = dataObj.get("referenced_tweets", None)
		self.attachments = {}


		attachments = dataObj.get("attachments", None)

		if attachments is not None:
			if "poll_ids" in attachments:
				self.attachments["polls"] = [Poll(next((poll for poll in includesObj.get("polls", []) if poll['id'] == poll_id), None)) for poll_id in attachments.get("poll_ids")]
			if "media_keys" in attachments:
				self.attachments["media"] = [Media(next((m for m in includesObj.get("media", []) if m['media_key'] == media_key), None)) for media_key in attachments.get('media_keys')]
