from bot import Bot
from dispatcher import Dispatcher
import executor

# нельзя забыть врубить longpoll в группе

#удалю каролче

token = 'd26916b138dcad7d8aa5490a170af3caa558a5010c9be9a8782130d7e017274dcec840e856610ddde8ac1'
group_id = 180776933

bot = Bot(token, group_id)
dp = Dispatcher(bot)


@dp.handler()
async def lol(obj):
	print(obj)


@dp.message_handler()
async def echo(message):
	await bot.messages_send(message.peer_id, message.text)


if __name__ == '__main__':
	executor.start_polling(dp)