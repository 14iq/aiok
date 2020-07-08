class TypesFilter(BaseFilter):
	def __init__(self, types):
		if isinstance(types, str):
			types = (types, )

		self.types = types

	async def check(self, update):
		return update.type in self.types


class CustomFilter(BaseFilter):
	def __init__(self, custom_filter):
		self.filter_ = custom_filter

	async def check(self, args):
		return self.filter_(args)


class StatesFilter(BaseFilter):
	def __init__(self, dispatcher, states):
		self.dispatcher = dispatcher

		self.states = states
		if not isinstance(states, (list, set, tuple, frozenset)) or states is None:
			self.states = (states, )


	async def check(self, message):
		if '*' in self.states:
			return {'state': self.dispatcher.current_state()}

		state = await self.dispatcher.storage.get_state(message.peer_id)
		if state in self.states:
			return {'state': self.dispatcher.current_state()}


class BaseFilter:
	async def check(self, *args):
		# this method must be overridden.
		pass

	def __call__(self, *args):
		return await self.check(*args)