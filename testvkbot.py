from bot import Bot
from dispatcher import Dispatcher
from utils import State
from filters import State
import executor

# нельзя забыть врубить longpoll в группе

#удалю каролче

token = 'd26916b138dcad7d8aa5490a170af3caa558a5010c9be9a8782130d7e017274dcec840e856610ddde8ac1'
group_id = 180776933

bot = Bot(token, group_id)
dp = Dispatcher(bot)


sum_state = State()


@dp.handler(types='message_typing_state')
async def lol(update):
	await bot.messages_send(update.object.from_id, 'хандлинг печатанья')


@dp.message_handler(lambda mes: mes.text == 'lol')
async def echo(message):
	await bot.messages_send(message.peer_id, f'{message.text} + fl[afs[fsa')


if __name__ == '__main__':
	executor.start_polling(dp)