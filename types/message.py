from __future__ import annotations

from typing import List

from . import base, fields
from .attachment import Attachment

class Message(base.VkObject):
	"""
	object from:
		https://vk.com/dev/objects/message
	
	"""
	id: base.Integer = fields.Field()
	date: base.Integer = fields.Field()
	peer_id: base.Integer = fields.Field()
	from_id: base.Integer = fields.Field()
	text: base.String = fields.Field()
	random_id: base.Integer = fields.Field()
	ref: base.String = fields.Field()
	ref_source: base.String = fields.Field()
	attachments: List[Attachment] = fields.ListField(base=Attachment)
	important: base.Boolean = fields.Field()
	#geo
	payload: base.String = fields.Field()
	#keyboard
	#fwd_messages
	#reply_message: Message = fields.Field(base=Message)
	#action: Action = fields.Field(base=Action)

	async def answer(text: str):
		"""
		You can easy answer to message without peer_id
			await message.answer(your_text, ...)
		"""
		await self.bot.messages_send(self.peer_id, text)