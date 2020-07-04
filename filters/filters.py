from .state import State


class TypesFilter:
	def __init__(self, types):
		if isinstance(types, str):
			types = (types, )

		self.types = types

	def check(self, update):
		return update.type in self.types


class CustomFilter:
	def __init__(self, custom_filter):
		self.filter_ = custom_filter

	def check(self, args):
		return self.filter_(args)


class StateFilter:
	def __init__(self, state: State):
		self.state = state

	def check(self, current_state: State):
		return self.state is current_state
