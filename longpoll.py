import api
from bot import Bot


class DotDict(dict):
    """
    a dictionary that supports dot notation 
    as well as dictionary access notation 
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value



class BotLongpoll:
	def __init__(self, bot, mode: int=2, wait: int=25):
		self.bot: Bot = bot

		self.wait = wait
		self.mode = mode

		self.ts = None
		self.url = None
		self.key = None
		self.server = None


		if not isinstance(bot, Bot):
			raise TypeError(f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'")


	async def update_longpoll_server(self, update_ts=True):
		response = await self.bot.get_long_poll_server()

		self.key = response['response']['key']
		self.url = response['response']['server']

		if update_ts:
			self.ts = response['response']['ts']


	async def check(self):
		if not self.key:
			await self.update_longpoll_server()

		data = {
			'act': 'a_check',
			'key': self.key,
			'ts': self.ts,
			'wait': self.wait,
			'mode': self.mode,
			'version': 3
		}

		response = await api.make_request(self.bot.session, data, url=self.url)
		self.ts = response['ts'] # skip last update to this

		return response
