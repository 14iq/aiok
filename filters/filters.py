import inspect


class BaseFilter:
	@classmethod
	def validate(cls, filters_config):
		"""
		this method must be overridden.

		"""
		pass

	async def check(self, *args):
		"""
		this method must be overridden.

		"""
		pass

	async def __call__(self, *args):
		return await self.check(*args)


class FilterRecord:
	def __init__(self, filter_cls, handlers):
		self.filter_ = filter_cls
		self.handlers = handlers

		self.validator = filter_cls.validate

	def _check_event_handler(self, event_handler):
		return event_handler in self.handlers
	
	def resolve(self, dispathcer, event_handler, filters_config):
		if not self._check_event_handler(event_handler):
			return

		config = self.validator(filters_config)
		if config:
			if 'dispatcher' not in config:
				if 'dispatcher' in inspect.getfullargspec(self.filter_).args:
					config['dispatcher'] = dispatcher

			return self.filter_(**config)
