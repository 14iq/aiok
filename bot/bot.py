from random import randint

import aiohttp

from . import api


def get_random_id():
	return randint(-9223372036854775807, 9223372036854775807)

PAYLOAD_FILTER = ['self']

def prepare_payload(**kwargs):
	return {key: val for key, val in kwargs.items() if
		key not in PAYLOAD_FILTER
		and val is not None
		and not key.startswith('_')}


class Bot:
	def __init__(self, token: str, group_id: int, proxy: str = None):
		self.token = token
		self.group_id = group_id
		self.proxy = proxy

		self._session: aiohttp.ClientSession = None
	
    
	@property # <- уже исполниная функция без абьедка
	def session(self) -> aiohttp.ClientSession:
		if self._session is None or self._session.closed:
			self._session = self.get_new_session()    	
		return self._session

	def get_new_session(self) -> aiohttp.ClientSession:
		return aiohttp.ClientSession() #тут чото будит

	async def close(self):
		await self.session.close()


	async def request(self, method: str, payload: dict):
		payload['access_token'] = self.token
		payload['v'] = '5.120'

		return await api.make_request(self._session, method, payload, proxy=self.proxy)


	async def messages_send(self, peer_id: int, message: str):
		random_id = get_random_id()

		payload = prepare_payload(**locals())

		return await self.request(api.Methods.messagesSend, payload)


	async def get_long_poll_server(self):
		payload = {'group_id': self.group_id}
		
		return await self.request(api.Methods.getLongPollServer, payload)
