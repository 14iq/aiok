import asyncio

from .dispatcher import Dispatcher


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



	def start_polling(self):
		self.loop.run_until_complete(self.dispatcher.start_polling())
