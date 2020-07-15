import logging

from ..mixins import ContextVarMixin
from ..bot import Bot, BotLongpoll
from .storage import MemoryDataStorage, StateContext, EmptyStorage
from .filters import FFactory, StatesFilter, Text
from .handler import Handler

log = logging.getLogger(__name__)

# похуй удалю патом
class Peer_id(ContextVarMixin):
 	pass


"""
except KeyboardInterrupt:
await bot.close()
self._polling = False
"""




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


class Dispatcher(ContextVarMixin):
	def __init__(self, bot, loop=None, store_data: bool=False):
		self.bot = bot
		self.loop = loop
		self.longpoll: BotLongpoll = None

		if not isinstance(bot, Bot):
			raise TypeError(f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'")

		self._polling = False

		self.message_handlers = Handler()

		self.storage = None
		if store_data:
			self._setup_storage()
		else:
			self.storage = EmptyStorage()


		self.filters_factory = FFactory(self)
		self._setup_filters()

		
	def _setup_filters(self):
		self.filters_factory.bind(StatesFilter, event_handlers=[
			self.message_handlers,
			])

		self.filters_factory.bind(Text, event_handlers=[
			self.message_handlers,
			])


	def _setup_storage(self):
		self.storage = MemoryDataStorage()


	def current_state(self):
		if not self.storage:
			raise ValueError('Cannot get state, storage is not defined')
		return StateContext(self.storage, Peer_id.get_current())


	def message_handler(self, *custom_filters, state=None, commands=None, **kwargs):
		def decorator(func):
			filters_set = self.filters_factory.resolve(self.message_handlers,
				*custom_filters,
				state=state,
				commands=commands,
				**kwargs,)
			self.message_handlers.register(func, filters_set)
			
			return func

		return decorator

	async def notify_update(self, update):
		if update.type == 'message_new':
			Peer_id.set_current(update.object.message.peer_id)
			await self.message_handlers.notify(update.object.message)

	async def start_polling(self):
		if self._polling:
			raise RuntimeError('Polling already started')

		self.bot.session
		self.longpoll = BotLongpoll(self.bot)

		self._polling = True
		log.info('Polling is started...')
		while self._polling:
			response = await self.longpoll.check()

			if response:
				for update in response['updates']:
					await self.notify_update(DotDict(update))

	def stop_polling(self):
		if self._polling:
			self._polling = False
