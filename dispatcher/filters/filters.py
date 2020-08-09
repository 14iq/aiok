import inspect
from typing import Optional, Iterable

from ..handler import FilterObj


def _prepare_filters(filters: Iterable[callable]):
	data = []
	for filter_ in filters:

		#import pdb; pdb.set_trace()

		if not callable(filter_):
			raise TypeError('Filter must be callable!')

		if inspect.isawaitable(filter_) \
            	or inspect.iscoroutinefunction(filter_) \
            	or isinstance(filter_, BaseFilter):
			data.append(FilterObj(filter_=filter_, is_async=True))
		else:
			data.append(FilterObj(filter_=filter_, is_async=False))

	return data


async def execute_filter(filter_obj: FilterObj, args):
	if filter_obj.is_async:
		return await filter_obj.filter_(*args)
	else:
		return filter_obj.filter_(*args)


async def check_filters(filters: Optional[Iterable[FilterObj]], *args):
	if filters:
		data = {}
		for filter_obj in filters:
			check = await execute_filter(filter_obj, args)
			if not check:
				return
			if isinstance(check, dict):
				data.update(check)

		if data:
			return data

	return True


class FilterRecord:
	def __init__(self, filter_cls, handlers):
		self.filter_ = filter_cls
		self.handlers = handlers

		self.validator = filter_cls.validate

	def _check_event_handler(self, event_handler):
		return event_handler in self.handlers
	
	def resolve(self, dispatcher, event_handler, filters_config):
		if not self._check_event_handler(event_handler):
			return

		config = self.validator(filters_config)
		if config:
			if 'dispatcher' not in config:
				if 'dispatcher' in inspect.getfullargspec(self.filter_).args:
					config['dispatcher'] = dispatcher

			return self.filter_(**config)


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
