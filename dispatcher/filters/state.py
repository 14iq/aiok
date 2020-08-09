from ..dispatcher import Dispatcher


class State:
	async def set(self):
		state = Dispatcher.get_current().current_state()
		await state.set_state(self)

	async def reset(self):
		state = Dispatcher.get_current().current_state()
		await state.set_state('*')