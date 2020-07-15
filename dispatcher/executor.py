import asyncio
import logging

from .dispatcher import Dispatcher

log = logging.getLogger(__name__)

def start_polling(dispatcher):
	executor = Executor(dispatcher, dispatcher.loop)
	executor.start_polling()



class Executor:
	def __init__(self, dispatcher, loop):
		if not isinstance(dispatcher, Dispatcher):
			raise TypeError(f"must be an instance of Dispatcher, not '{type(dp)}'")

		Dispatcher.set_current(dispatcher)
		self.dispatcher = dispatcher
		
		if not loop:
			loop = asyncio.get_event_loop()

		self.loop = loop

	async def shutdown(self):
		self.dispatcher.stop_polling()
		await self.dispatcher.storage.close()
		await self.dispatcher.bot.close()


	def start_polling(self):
		try:
			self.loop.run_until_complete(self.dispatcher.start_polling())
		except (KeyboardInterrupt, SystemExit):
			pass
		finally:
			self.loop.run_until_complete(self.shutdown())
			log.warning('Bye (-_-)')