from typing import Dict, Optional



async def make_request(session, data: Optional[Dict],
	url: str=None, method: str=None, **kwargs):

	if method and not url:
		url = f'https://api.vk.com/method/{method}'

	async with session.post(url, data=data, **kwargs) as response:
		json = await response.json()

	return json


# there is all vk constants

class Methods():
	# all method names
	#GROUPS
	getLongPollServer = 'groups.getLongPollServer'
	#MESSAGES
	messagesSend = 'messages.send'
