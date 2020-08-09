from __future__ import annotations

import typing

from ..bot.bot import Bot

from .fields import BaseField
from ..utils import json
from ..utils.mixins import ContextVarMixin

PROPS_ATTR = '_props'
VALUES_ATTR = '_values'
ALIASES_ATTR = '_aliases'


Integer = typing.TypeVar('Integer', bound=int)
Float = typing.TypeVar('Float', bound=float)
String = typing.TypeVar('String', bound=str)
Boolean = typing.TypeVar('Boolean', bound=bool)
T = typing.TypeVar('T')

class MetaVkObject(type):
	def __new__(cls: typing.Type[T], name: str, bases: typing.Tuple[typing.Type], namespace: typing.Dict[str, typing.Any]) -> typing.Type[T]:
		cls = super(MetaVkObject, cls).__new__(cls, name, bases, namespace)

		props = {}
		aliases = {}

		fields = ((name, prop) for name, prop in namespace.items() if isinstance(prop, BaseField))
		
		for name, prop in fields:
			props[prop.alias] = prop
			aliases[name] = prop.alias

		setattr(cls, PROPS_ATTR, props)
		setattr(cls, VALUES_ATTR, {})
		setattr(cls, ALIASES_ATTR, aliases)

		return cls


class VkObject(ContextVarMixin, metaclass=MetaVkObject):
	def __init__(self, **kwargs: typing.Any) -> None:
		# load values that give
		for key, val in kwargs.items():
			if key in self.props:
				self.props[key].set_value(self, val)
			else:
				self.values[key] = val
		
		# load default values if it is set
		for key, val in self.props.items():
			if val.default and key not in self.values:
				self.values[key] = val.default

	@property
	def props(self) -> typing.Dict[str, BaseField]:
		return getattr(self, PROPS_ATTR, {})

	@property
	def values(self) -> typing.Dict[str, typing.Any]:
		return getattr(self, VALUES_ATTR, {})

	@property
	def aliases(self) -> typing.Dict[str, str]:
		return getattr(self, ALIASES_ATTR, {})

	@property
	def bot(self) -> Bot:
		bot = Bot.get_current()
		if bot is None:
			raise RuntimeError("VkObject can't get bot from context.\ntry - 'Bot.set_current(bot_instance)'")
		return bot

	def to_python(self) -> typing.Dict[str, typing.Any]:
		"""
		represents data in terms familiar to Python
		"""
		result = {}
		for name, val in self.values.items():
			if name in self.props:
				val = self.props[name].represent(self)
			elif isinstance(val, VkObject):
				val = val.to_python()
			result[self.aliases.get(name, name)] = val
		return result

	def to_json(self) -> str:
		"""
		represents json data
		"""
		return json.dumps(self.to_python())

	def __str__(self) -> str:
		return self.to_json()

	def __contains__(self, item: str) -> bool:
		return bool(self.values.get(item, None))

	def __getitem__(self, item: typing.Union[str, int]) -> typing.typing.Any:
		if item in self.values:
			return self.values[item]
		raise KeyError(item)

	def __iter__(self) -> typing.Iterator[typing.Tuple[str, typing.Any]]:
		for item in self.to_python().items():
			yield item

	def __eq__(self, other: VkObject) -> bool:
		return isinstance(other, self.__class__)
