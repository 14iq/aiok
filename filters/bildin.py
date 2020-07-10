from .filters import BaseFilter


class TypesFilter(BaseFilter):
	def __init__(self, types):
		if isinstance(types, str):
			types = (types, )

		self.types = types

	@classmethod
	def validate(cls, filters_config):
		config = {}
		if 'types' in filters_config:
			config['types'] = filters_config.pop('types')

		return config

	async def check(self, update):
		return update.type in self.types


class CommandFilter(BaseFilter):
	def __init__(self, commands):
		if isinstance(commands, str):
			commands = (commands, )

		self.commands = commands

	async def check(self, *args):
		pass


class StatesFilter(BaseFilter):
	def __init__(self, dispatcher, states):
		self.dispatcher = dispatcher

		self.states = states
		if not isinstance(states, (list, set, tuple, frozenset)) or states is None:
			self.states = (states, )

	@classmethod
	def validate(cls, filters_config):
		config = {}
		if 'state' in filters_config:
			config['state'] = filters_config.pop('state')

		return config

	async def check(self, message):
		if '*' in self.states:
			return {'state': self.dispatcher.current_state()}

		state = await self.dispatcher.storage.get_state(message.peer_id)
		if state in self.states:
			return {'state': self.dispatcher.current_state()}



class Text(BaseFilter):
	"""
	Inline text filter

	some info
	
	# if you wanna Set param:
	# ignore_case - use instance of Text
	# may used by importing
	
	"""
	_filter_keys = (
		('equals', 'text'),
		('startswith', 'text_startswith'),
		('endswith', 'text_endswith'),
		)


	def __init__(self, equals: str=None, ignore_case=False, startswith: str=None, endswith: str=None):
		if ignore_case: # TeXt = text (.lower())
			equals, startswith, endswith = map(lambda arg: arg.lower() if isinstance(arg, str) else arg,
				(equals, startswith, endswith))

		arg_count = sum(map(lambda arg: arg is not None, (equals, startswith, endswith)))
		if arg_count > 1:
			raise ValueError(f"arguments can't used together")
		if arg_count == 0:
			raise ValueError('No one arg is specified')

		equals, startswith, endswith = map(lambda arg: [arg] if isinstance(arg, str) else arg,
			(equals, startswith, endswith))			

		self.ignore = ignore_case
		self.equals = equals
		self.startswith = startswith
		self.endswith = endswith

	@classmethod
	def validate(cls, filters_config):
		for key, param in cls._filter_keys:
			if param in filters_config:
				return {key: filters_config.pop(param)}

	async def check(self, message):
		text = message.text.lower() if self.ignore else message.text
		
		if self.equals is not None:
			return text in self.equals

		if self.startswith is not None:
			return any(map(text.startswith, self.startswith))

		if self.endswith is not None:
			return any(map(text.endswith, self.endswith))

		return False
