from . import api



class BotLongpoll:
	def __init__(self, bot, mode: int=2, wait: int=25):
		self.bot: Bot = bot

		self.wait = wait
		self.mode = mode

		self.ts = None
		self.key = None
		self.server = None


	async def update_longpoll_server(self, update_ts=True):
		response = await self.bot.get_long_poll_server()

		if 'error' in response:
			raise ValueError(f'register longpoll server error: {response["error"]}')

		self.key = response['response']['key']
		self.server = response['response']['server']

		if update_ts:
			self.ts = response['response']['ts']


	async def check(self):
		if not self.key:
			await self.update_longpoll_server()

		payload = {
			'act': 'a_check',
			'key': self.key,
			'ts': self.ts,
			'wait': self.wait,
			'mode': self.mode,
			'version': 3
		}

		response = await api.make_server_request(self.bot.session, self.server, payload)

		if not 'failed' in response:
			self.ts = response['ts'] # skip last update to this

			return response


		elif response['failed'] == 1:
			self.ts = response['ts']

		elif response['failed'] == 2:
			await self.update_longpoll_server(update_ts=False)

		elif response['failed'] == 3:
			await self.update_longpoll_server()
