import inspect
from typing import Optional, Iterable
from dataclasses import dataclass


@dataclass
class FilterObj:
	filter_: callable
	is_async: bool = False


def _retrive_spec(spec: inspect.FullArgSpec, kwargs: dict):
	if isinstance(kwargs, dict):
		return {key: val for key, val in kwargs.items() if key in spec.args}
	return {}


class Handler:
	def __init__(self):
		self.handlers = []

	def register(self, func, filters=None):
		"""
		do not worry
		import happens once
		"""
		from .filters import _prepare_filters

		spec = inspect.getfullargspec(func)
		filters = _prepare_filters(filters)
		record = Handler.HandlerObject(func=func, spec=spec, filters=filters)
		self.handlers.append(record)


	async def notify(self, *args):
		"""
		do not worry
		import happens once
		"""
		from .filters import check_filters

		for handler_obj in self.handlers:
			filtered_result = await check_filters(handler_obj.filters, *args)
			if filtered_result:
				additionally = _retrive_spec(handler_obj.spec, filtered_result)
				await handler_obj.func(*args, **additionally)
				return # 1 handler passed now can stop
			

	@dataclass
	class HandlerObject:
		func: callable
		spec: inspect.FullArgSpec
		filters: Optional[Iterable[FilterObj]] = None
		