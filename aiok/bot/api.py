async def make_server_request(session, server_url: str, data: dict, **kwargs):
	async with session.post(server_url, data=data, **kwargs) as response:
		return await response.json()


async def make_request(session, method: str, data: dict, **kwargs):
	
	url = f'https://api.vk.com/method/{method}'

	async with session.post(url, data=data, **kwargs) as response:
		return await response.json()


# there is all vk constants

class Methods():
	# all method names
	#GROUPS
	getLongPollServer = 'groups.getLongPollServer'
	#MESSAGES
	messagesSend = 'messages.send'
