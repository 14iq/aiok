from typing import Optional, Iterable
from dataclasses import dataclass

from filters import TypesFilter, CustomFilter
from longpoll import BotLongpoll
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


@dataclass
class FilterObj:
	filter: callable


class Dispatcher:
	def __init__(self, bot, loop=None):
		self.bot = bot
		self.loop = loop
		self.longpoll: BotLongpoll = None

		self._polling = True

		self.update_handlers = Handler()
		self.message_handlers = Handler()

		if not isinstance(bot, Bot):
			raise TypeError(f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'")


	def prepare_filters(self, *args, types=None):
		filters = []
		if types:
			filters.append(FilterObj(TypesFilter(types)))

		for filter_ in args:
			filters.append(FilterObj(CustomFilter(filter_)))

		return filters


	def handler(self, *custom_filters, types=None):
		"""
		def func(messsage_obj): - return this decorator to the func
		"""
		def decorator(func):
			filters_set = self.prepare_filters(*custom_filters, types=types)
			self.update_handlers.register(func, filters_set)
			
			return func

		return decorator


	def message_handler(self, *custom_filters):
		"""
		def func(messsage_obj): - return this decorator to the func
		"""
		def decorator(func):
			filters_set = self.prepare_filters(*custom_filters)
			self.message_handlers.register(func, filters_set)
			
			return func

		return decorator


	async def start_polling(self):
		self.bot.session
		self.longpoll = BotLongpoll(self.bot)

		print('polling is started')
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
			await self.message_handlers.notify(update.object.message)



class Handler:
	def __init__(self):
		self.handlers = []


	def register(self, func, filters=None):
		record = Handler.HandlerObject(func=func, filters=filters)
		self.handlers.append(record)


	def check_filters(self, filters: Optional[Iterable[FilterObj]], args):
		if filters:
			for filter_obj in filters:
				if not filter_obj.filter.check(args):
					return False
		return True



	async def notify(self, args):
		for handler_obj in self.handlers:
			if self.check_filters(handler_obj.filters, args):
				await handler_obj.func(args)
				return
			

	@dataclass
	class HandlerObject:
		func: callable
		filters: Optional[Iterable[FilterObj]] = None
		