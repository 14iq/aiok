import contextvars


class ContextVarMixin:
	def __init_subclass__(cls):
		cls.__context_var = contextvars.ContextVar(f'var_{cls.__name__}')

	@classmethod
	def set_current(cls, obj):
		cls.__context_var.set(obj)

	@classmethod
	def get_current(cls):
		return cls.__context_var.get(None)
		