class StateContext:
	def __init__(self, storage, peer):
		self.storage = storage
		self.peer = peer

	async def finish(self):
		await self.storage.set_state(self.peer, '*')

	async def get_data(self):
		return await self.storage.get_data(self.peer)

	async def update_data(self, data=None, **kwargs):
		await self.storage.update_data(self.peer, data, **kwargs)

	async def get_state(self):
		return await self.storage.get_state(self.peer)

	async def set_state(self, state):
		await self.storage.set_state(self.peer, state)


class MemoryDataStorage:
	async def close(self):
		self.data.clear()

	def __init__(self):
		self.data = {}

	def resolve_address(self, peer):
		if peer not in self.data:
			self.data[peer] = {'state': '*', 'data': {}}


	async def set_state(self, peer, state):
		self.resolve_address(peer)
		self.data[peer]['state'] = state


	async def get_state(self, peer):
		self.resolve_address(peer)
		return self.data[peer]['state']


	async def update_data(self, peer, data=None, **kwargs):
		self.resolve_address(peer)
		if data is None:
			data = {}

		self.data[peer]['data'].update(data, **kwargs)


	async def get_data(self, peer):
		self.resolve_address(peer)
		return self.data[peer]['data']


class EmptyStorage:
	async def close(self):
		pass

	async def set_state(self, peer, state):
		self.warn()

	async def get_state(self, peer):
		self.warn()

	async def update_data(self, peer, data=None, **kwargs):
		self.warn()

	async def get_data(self, peer):
		self.warn()
		
	@staticmethod
	def warn():
		raise ValueError("You haven’t set any storage yet, No states. No data will be saved. \n")
