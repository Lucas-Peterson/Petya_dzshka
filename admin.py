from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

ADMIN = 707305173

class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()

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
