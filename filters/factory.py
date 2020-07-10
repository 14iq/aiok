import typing

from .filters import BaseFilter, FilterRecord



class FFactory:
	def __init__(self, dispatcher):
		self.dispatcher = dispatcher
		self._recorded: typing.List[FilterRecord] = []

	def bind(self, filter_cls, event_handlers):
		record = FilterRecord(filter_cls, event_handlers)
		self._recorded.append(record)

	def resolve(self, event_handler, *custom_filtes, **filters_config
		) -> typing.List[typing.Union[typing.Callable, BaseFilter]]:
		filters_set = []
		filters_set.extend(self._resolve_registered(event_handler,
			{key: val for key, val in filters_config.items() if val is not None}))
		if custom_filtes:
			filters_set.extend(custom_filtes)

		return filters_set

	def _resolve_registered(self, event_handler, filters_config) -> typing.Generator:
		for record in self._recorded:
			filter_ = record.resolve(self.dispatcher, event_handler, filters_config)
			if filter_:
				yield filter_

		if filters_config:
			raise ValueError(f'Invalid arg for filter(s) {", ".join(filters_config)}')
