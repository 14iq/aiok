from . import base, fields

class Attachment(base.VkObject):
	type: base.String = fields.Field()
	photo = fields.Field()
	video = fields.Field()
	audio = fields.Field()
	doc = fields.Field()
	link = fields.Field()
	market = fields.Field()
	market_album = fields.Field()
	wall = fields.Field()
	wall_reply = fields.Field()
	sticker = fields.Field()
	gift = fields.Field()