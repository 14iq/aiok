from abc import abstractmethod, ABCMeta


class BaseField(metaclass=ABCMeta):
	def __init__(self, default=None, base=None, alias=None):
		self.default = default
		self.base_object = base
		self.alias = alias

	def __set_name__(self, owner, name):
		if self.alias is None:
			self.alias = name

	def get_value(self, instance):
		return instance.values.get(self.alias, self.default)

	def set_value(self, instance, value): ####
		value = self.deserialize(value)
		instance.values[self.alias] = value

	def __get__(self, instance, owner):
		return self.get_value(instance)

	def __set__(self, instance, value):
		self.set_value(instance, value)

	@abstractmethod
	def serialize(self, value):
		pass

	@abstractmethod
	def deserialize(self, value):
		pass

	def represent(self, instance):
		return self.serialize(self.get_value(instance))


class Field(BaseField):
	def serialize(self, value):
		if self.base_object is not None and hasattr(value, 'to_python'):
			return value.to_python()
		return value

	def deserialize(self, value): #
		if isinstance(value, dict) \
				and self.base_object is not None:
			return self.base_object(**value)
		return value


class ListField(Field):
	def __init__(self, default=None, base=None, alias=None):
		if default is None:
			default = []
		super(ListField, self).__init__(default, base, alias)

	def serialize(self, value): #
		result = []
		for item in value:
			result.append(super(ListField, self).serialize(item))
		return result

	def deserialize(self, value):
		result = []
		for item in value:
			result.append(super(ListField, self).deserialize(item))
		return result
