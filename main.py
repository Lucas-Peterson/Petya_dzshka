import logging
import sqlite3
import time
import datetime
from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
import markups as nav

bot = Bot(token="5297937415:AAHQwWuf2AePeLVbREsBPV07xGknYVdSyv8")
YOOTOKEN = "381764678:TEST:38452"
ADMIN = 707305173

storage = MemoryStorage()

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INTEGER,
   block INTEGER);
""")
conn.commit()

class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()
#------------------------------------------------------------Data_base----------------------------------------------------------------
def set_time_sub(self, user_id, time_sub):
    with self.connection:
        return self.cursor.execute("UPDATE 'users' SET 'time_sub' = ? WHERE 'user ID' = ?", (time_sub, user_id))

def get_time_sub(self, user_id):
    with self.connection:
        result = self.cursor.execute("SELECT 'time_sub' FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchall()
        for row in result:
            time_sub = int(row[0])
        return time_sub

    def get_time_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT 'time_sub' FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])

            if time_sub > int(time.time()):
                return True
            else:
                return False

#---------------------------------------------------------------StartMeny--------------------------------------------------------------------------------------------
@dp.message_handler(commands=['start'])
async def admn(message: Message):
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=keyboard)
    # ------------------------------------------------------Payment-----------------------------------------------------------
    else:
        if result is None:
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
            entry = cur.fetchone()
            if entry is None:
                cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
            conn.commit()
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
                               description="Вы покупаете продукт от Kazarchik.py™",
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
        time_sub = int(time.time()) + days_to_seconds(30)
        db.db.set_time_sub(message.from_user_id, time_sub)
        await bot.send_message(message.from_user.id, "Вам была выдана подписка")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Математика📕"))
        keyboard.add(types.InlineKeyboardButton(text="Информатика👨🏼‍💻"))
        keyboard.add(types.InlineKeyboardButton(text="Русский🪶"))
        keyboard.add(types.InlineKeyboardButton(text="Физика📚"))
        keyboard.add(types.InlineKeyboardButton(text="Дальше"))
        await message.answer('Добро пожаловать в ваше главное меню!', reply_markup=keyboard)

        @dp.message_handler(text="Математика📕")
        async def bot_message(message: types.Message):
            await bot.send_message(message.from_user.id, 'text')

        @dp.message_handler(text="Информатика👨🏼‍💻")
        async def bot_message(message: types.Message):
            await bot.send_message(message.from_user.id, 'text')

        @dp.message_handler(text="Русский🪶")
        async def bot_message(message: types.Message):
            await bot.send_message(message.from_user.id, 'text')

        @dp.message_handler(text="Физика📚")
        async def bot_message(message: types.Message):
            await bot.send_message(message.from_user.id, 'text')

        @dp.message_handler(text="Дальше")
        async def bot_message(message: types.Message):

            keyboard.add(types.InlineKeyboardButton(text="Право🧑‍⚖️"))
            keyboard.add(types.InlineKeyboardButton(text="Биология🍀"))
            keyboard.add(types.InlineKeyboardButton(text="Химия🌱"))

        @dp.message_handler(text="Право🧑‍⚖️")
        async def bot_message(message: types.Message):
            await bot.send_message(message.from_user.id, 'text')

        @dp.message_handler(text="Биология🍀")
        async def bot_message(message: types.Message):
            await bot.send_message(message.from_user.id, 'text')

        @dp.message_handler(text="Химия🌱")
        async def bot_message(message: types.Message):
            await bot.send_message(message.from_user.id, 'text')

        #----------------------------------------------Time_sub-----------------------------------------------------------------

        def days_to_seconds(days):
            return days * 24 * 60 * 60

        def time_sub_day(get_time):
            time_now = int(time.time())
            middle_time = int(get_time) - time_now
            if middle_time <= 0:
                return False
            else:
                dt = str(datetime.timedelta(seconds=middle_time))
                return dt
#---------------------------------------------------Admin-------------------------------------------------------------------------------

@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):
    if message.from_user.id == ADMIN:
        await dialog.spam.set()
        await message.answer('Напиши текст рассылки')
    else:
        await message.answer('Вы не являетесь админом')


@dp.message_handler(state=dialog.spam)
async def start_spam(message: Message, state: FSMContext):
    if message.text == 'Назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await message.answer('Главное меню', reply_markup=keyboard)
        await state.finish()
    else:
        cur = conn.cursor()
        cur.execute(f'''SELECT user_id FROM users''')
        spam_base = cur.fetchall()
        print(spam_base)
        for z in range(len(spam_base)):
            print(spam_base[z][0])
        for z in range(len(spam_base)):
            await bot.send_message(spam_base[z][0], message.text)
        await message.answer('Рассылка завершена')
        await state.finish()


@dp.message_handler(state='*', text='Назад')
async def back(message: Message):
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await message.answer('Главное меню', reply_markup=keyboard)
    else:
        await message.answer('Вам не доступна эта функция')


@dp.message_handler(content_types=['text'], text='Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))
        await message.answer(
            'Введите id пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже',
            reply_markup=keyboard)
        await dialog.blacklist.set()


@dp.message_handler(state=dialog.blacklist)
async def proce(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await message.answer('Отмена! Возвращаю назад.', reply_markup=keyboard)
        await state.finish()
    else:
        if message.text.isdigit():
            cur = conn.cursor()
            cur.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
            result = cur.fetchall()
            # conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0]
                id = a[0]
                if id == 0:
                    cur.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    await message.answer('Пользователь успешно добавлен в ЧС.', reply_markup=keyboard)
                    await state.finish()
                    await bot.send_message(message.text, 'Ты получил от администрацией.')
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    await message.answer('Данный пользователь уже получил бан', reply_markup=keyboard)
                    await state.finish()
        else:
            await message.answer('Ты вводишь буквы...\n\nВведи ID')


@dp.message_handler(content_types=['text'], text='Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if result is None:
        if message.chat.id == ADMIN:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))
            await message.answer(
                'Введите id пользователя, которого нужно разблокировать.\nДля отмены нажмите кнопку ниже',
                reply_markup=keyboard)
            await dialog.whitelist.set()

# if db.get_sub_status(message.from_user_id):
#    await bot.send_message(message.from_user.id, "Предметы")
#  else await bot.send_message("Купите подписку")

@dp.message_handler(state=dialog.whitelist)
async def proc(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await message.answer('Отмена! Возвращаю назад.', reply_markup=keyboard)
        await state.finish()
    else:
        if message.text.isdigit():
            cur = conn.cursor()
            cur.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
            result = cur.fetchall()
            conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0]
                id = a[0]
                if id == 1:
                    cur = conn.cursor()
                    cur.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    await message.answer('Пользователь успешно разбанен.', reply_markup=keyboard)
                    await state.finish()
                    await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    await message.answer('Данный пользователь не получал бан.', reply_markup=keyboard)
                    await state.finish()
        else:
            await message.answer('Ты вводишь буквы...\n\nВведи ID')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)