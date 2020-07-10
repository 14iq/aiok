import inspect
from typing import Optional, Iterable
from dataclasses import dataclass

from .storage import MemoryDataStorage, StateContext
from ..mixins import ContextVarMixin
from ..filters import FFactory, TypesFilter, StatesFilter, \
	CommandFilter, Text
from ..bot import Bot, BotLongpoll


# похуй удалю патом
class Peer_id(ContextVarMixin):
 	pass



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


@dataclass
class FilterObj:
	filter: callable


class Dispatcher(ContextVarMixin):
	def __init__(self, bot, loop=None, store_data=False):
		self.bot = bot
		self.loop = loop
		self.longpoll: BotLongpoll = None

		if not isinstance(bot, Bot):
			raise TypeError(f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'")

		self.filters_factory = FFactory(self)

		self._polling = True

		if store_data:
			self.storage = MemoryDataStorage()

		self.update_handlers = Handler()
		self.message_handlers = Handler()

		self._setup_filters()


		
	def _setup_filters(self):
		self.filters_factory.bind(StatesFilter, event_handlers=[
			self.message_handlers,
			])

		self.filters_factory.bind(Text, event_handlers=[
			self.message_handlers,
			])


	def current_state(self):
		return StateContext(self.storage, Peer_id.get_current())


	def handler(self, *custom_filters, types=None, **kwargs):
		def decorator(func):
			filters_set = self.filters_factory.resolve(self.update_handlers,
				*custom_filters,
				types=types,
				**kwargs,)
			self.update_handlers.register(func, filters_set)
			
			return func

		return decorator


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


	async def start_polling(self):
		self.bot.session
		self.longpoll = BotLongpoll(self.bot)

		print('[INFO] Start polling')
		while self._polling:
			try:
				response = await self.longpoll.check()

				if response:
					for update in response['updates']:
						await self.notify_update(DotDict(update))

			except KeyboardInterrupt:
				await bot.close()
				self._polling = False


	async def notify_update(self, update):
		await self.update_handlers.notify(update)
		if update.type == 'message_new':
			Peer_id.set_current(update.object.message.peer_id)
			await self.message_handlers.notify(update.object.message)


def retrive_spec(spec: inspect.FullArgSpec, kwargs: dict):
	if isinstance(kwargs, dict):
		return {key: val for key, val in kwargs.items() if key in spec.args}
	return {}


class Handler:
	def __init__(self):
		self.handlers = []

	def _prepare_filters(self, filters: Iterable[callable]):
		data = []
		for filter_ in filters:
			data.append(FilterObj(filter_))

		return data

	def register(self, func, filters=None):
		spec = inspect.getfullargspec(func)
		filters = self._prepare_filters(filters)
		record = Handler.HandlerObject(func=func, spec=spec, filters=filters)
		self.handlers.append(record)


	async def check_filters(self, filters: Optional[Iterable[FilterObj]], *args):
		if filters:
			data = {}
			for filter_obj in filters:
				check = await filter_obj.filter(*args)
				if not check:
					return
				if isinstance(check, dict):
					data.update(check)

			if data:
				return data
		return True


	async def notify(self, *args):
		for handler_obj in self.handlers:
			filtered_result = await self.check_filters(handler_obj.filters, *args)
			if filtered_result:
				additionally = retrive_spec(handler_obj.spec, filtered_result)
				await handler_obj.func(*args, **additionally)
				return
			

	@dataclass
	class HandlerObject:
		func: callable
		spec: inspect.FullArgSpec
		filters: Optional[Iterable[FilterObj]] = None
		