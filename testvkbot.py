import asyncio

from longpoll import BotLongpoll, DotDict
from bot import Bot


# нельзя забыть врубить longpoll в группе

#удалю каролче
async def test():
	token = 'd26916b138dcad7d8aa5490a170af3caa558a5010c9be9a8782130d7e017274dcec840e856610ddde8ac1'
	group_id = 180776933
	bot = Bot(token, group_id)
	bot.session

	longpoll = BotLongpoll(bot)

	while True:
		try:
			res = await longpoll.check()
			for upd in res['updates']:
				event = DotDict(upd)
				if event.type == 'message_new':
					await bot.messages_send(event.object.message.peer_id, event.object.message.text)
		except KeyboardInterrupt:
			break

	await bot.close()

# ета пока для тестав
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())