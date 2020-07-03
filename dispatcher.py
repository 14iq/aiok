from typing import Optional, Iterable
from dataclasses import dataclass

from longpoll import BotLongpoll
from bot import Bot


@dataclass
class FilterObj:
	filter: callable


class Dispatcher:
	def __init__(self, bot, loop=None):
		self.bot = bot
		self.loop = loop
		self.longpoll: BotLongpoll = None

		self._polling = True

		self.obj_handlers = Handler()
		self.message_handlers = Handler()

		if not isinstance(bot, Bot):
			raise TypeError(f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'")


	def handler(self):
		"""
		def func(messsage_obj): - return this decorator to the func
		"""
		def decorator(func):
			self.obj_handlers.register(func)
			
			return func

		return decorator


	def message_handler(self):
		"""
		def func(messsage_obj): - return this decorator to the func
		"""
		def decorator(func):
			self.message_handlers.register(func)
			
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
					for update in response.updates:
						await self.notify_update(update)

			except KeyboardInterrupt:
				await bot.close()
				self._polling = False


	async def notify_update(self, update):
		self.obj_handlers.notify(update.object)
		if update.type == 'message.new':
			self.message_handlers.notify(update.object.message)



class Handler:
	def __init__(self):
		self.handlers = []


	def register(self, func, filters=None):
		record = Handler.HandlerObject(func=func, filters=filters)
		self.handlers.append(record)


	async def notify(self, args):
		for handler_obj in self.handlers:
			await handler_obj.func(args)
			

	@dataclass
	class HandlerObject:
		func: callable
		filters: Optional[Iterable[FilterObj]] = None
		