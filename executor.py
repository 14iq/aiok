import asyncio

from dispatcher import Dispatcher


def start_polling(dp):
	if not isinstance(dp, Dispatcher):
		raise TypeError(f"Argument 'dp' must be an instance of Dispatcher,\
			not '{type(dp).__name__}'")

	loop = dp.loop

	if not loop:
		loop = asyncio.get_event_loop()

	loop.run_until_complete(dp.start_polling())
