import asyncio
import logging

from .dispatcher import Dispatcher
from ..bot.bot import Bot

log = logging.getLogger(__name__)



def start_polling(dispatcher: Dispatcher, on_startup=None):
	executor = Executor(dispatcher, dispatcher.loop)
	executor.setup_startup(on_startup)

	executor.start_polling()


async def start_async_polling(dispatcher: Dispatcher, on_startup=None):
	executor = Executor(dispatcher, dispatcher.loop)
	await executor.setup_async_startup(on_startup)

	await executor.start_async_polling()

class Executor:
	def __init__(self, dispatcher, loop=None):
		if not isinstance(dispatcher, Dispatcher):
			raise TypeError(f"must be an instance of Dispatcher, not '{type(dp)}'")

		Dispatcher.set_current(dispatcher)
		Bot.set_current(dispatcher.bot)

		self.dispatcher = dispatcher
		
		if not loop: 
			loop = asyncio.get_event_loop()

		self.loop = loop

	async def shutdown_polling(self):
		self.dispatcher.stop_polling()
		await self.dispatcher.storage.close()
		await self.dispatcher.bot.close()

	def setup_startup(self, on_startup):
		if on_startup is not None:
			if isinstance(on_startup, (list, tuple, set)):
				for callback in on_startup: # recursively execute callback
					self.setup_startup(callback)
				return

			if not callable(on_startup): 
				raise TypeError('Arg/elements in on_startup must be callable!')

			self.loop.run_until_complete(on_startup())

	def start_polling(self):
		try:
			self.loop.run_until_complete(self.dispatcher.start_polling())
		except (KeyboardInterrupt, SystemExit):
			pass
		finally:
			self.loop.run_until_complete(self.shutdown_polling())
			log.warning('Bye (-_-)')

	async def start_async_polling(self):
		try:
			await self.dispatcher.start_polling()
		except (KeyboardInterrupt, SystemExit):
			pass
		finally:
			await self.shutdown_polling()
			log.warning('Bye (-_-)')

	async def setup_async_startup(self, on_startup):
		if on_startup is not None:
			if isinstance(on_startup, (list, tuple, set)):
				for callback in on_startup: # recursively execute callback
					await self.setup_async_startup(callback)
				return

			if not callable(on_startup): 
				raise TypeError('Arg/elements in on_startup must be callable!')

			await on_startup(self.dispatcher)