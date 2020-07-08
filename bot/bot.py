from typing import Dict, Optional
from random import randint

import aiohttp

from . import api


def get_random_id():
	return randint(-9223372036854775807, 9223372036854775807)


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


	async def request(self, method: str, data: Optional[Dict]):
		data['access_token'] = self.token
		data['v'] = '5.115'

		return await api.make_request(self._session, data, method=method, proxy=self.proxy)


	async def messages_send(self, peer_id: int, message: str):
		data = locals()
		data['random_id'] = get_random_id()

		return await self.request(api.Methods.messagesSend, data=data)


	async def get_long_poll_server(self):
		return await self.request(
			api.Methods.getLongPollServer,
			data={'group_id': self.group_id},
			)
