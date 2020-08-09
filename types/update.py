from . import base, fields
from .message import Message


class Object(base.VkObject):
	message: Message = fields.Field(base=Message)


class Update(base.VkObject):
	type: base.String = fields.Field() 
	object: Object = fields.Field(base=Object)
	group_id: base.Integer = fields.Field()
