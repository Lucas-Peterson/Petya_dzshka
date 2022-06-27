import logging
from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.types.message import ContentType
import markups as nav

bot = Bot(token="5297937415:AAHQwWuf2AePeLVbREsBPV07xGknYVdSyv8")
YOOTOKEN = "381764678:TEST:38452"

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
       await bot.send_message(message.from_user.id,'Привет👋, это бот по продаже домашек уже не помню какой школы,но они будут от великого Казара Мазарова. '
                                                   'Бот ещё в разработке, но в нашем телеграмм канале kazarchikpy будет доступна вся информация. Пока доступна только тестовая покупка подписки', reply_markup = nav.sub_inline_markup)

@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == 'Покупка подписки💸':
       await bot.send_message(message.from_user.id, 'описание возможностей подписки', reply_markup = nav.sub_inline_markup)

@dp.callback_query_handler(text="submonth")
async def submonth(call: types.CallbackQuery):
        await bot.send_invoice(chat_id= call.from_user.id,
                               title="Оформление подписки на Kazarchikpy",
                               description="Тест описание",
                               payload="month_sub",
                               provider_token=YOOTOKEN,
                               currency="RUB",
                               start_parameter="get_access",
                               prices=[{"label":"Руб", "amount": 40000}])

@dp.pre_checkout_query_handler()
async def process_pre_checout_query(pre_checout_query: types.PreCheckoutQuery):
        await bot.answer_pre_checkout_query(pre_checout_query.id, ok=True)

@dp.message_handler(content_types= ContentType.SUCCESSFUL_PAYMENT)
async def procces_pay(message:types.Message):
    if message.successful_payment.invoice_payload == "month_sub":

        await bot.send_message(message.from_user.id, "Вам была выдана подписка на месяц")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)