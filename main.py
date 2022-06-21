import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Text
from aiogram import types

bot = Bot(token="5297937415:AAHQwWuf2AePeLVbREsBPV07xGknYVdSyv8")

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")

async def cmd_test2(message: types.Message):
    await message.reply("Test 2")

dp.register_message_handler(cmd_test2, commands="test2")


@dp.message_handler(text=("Start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Математика📕", "Информатика🖥", "Русский🪶", "География🌍", "Химия👩‍🔬", "Биология🌱", "Обществознание🧑‍️", "Планы разработчика🧑🏼‍💻", "Результат разработчика👨🏼‍💻", "Pay💸" ]
    keyboard.add(*buttons)
    await message.answer("Привет! Это твои предметы которые будут вскоре сделаны как виджет, но пока вот так.", reply_markup=keyboard)

@dp.message_handler(Text(equals="Математика📕"))
async def with_puree(message: types.Message):
    await message.reply("Твоя математика!")

@dp.message_handler(lambda message: message.text == "Информатика🖥")
async def without_puree(message: types.Message):
    await message.reply("Вот твоя дз!")

@dp.message_handler(Text(equals="Русский🪶"))
async def with_puree(message: types.Message):
    await message.reply("Do you speak russia?")

@dp.message_handler(lambda message: message.text == "География🌍")
async def without_puree(message: types.Message):
    await message.reply("Ты помнишь, где экватор?🤨")

@dp.message_handler(Text(equals="Химия👩‍🔬"))
async def with_puree(message: types.Message):
    await message.reply("Твоя химия!")

@dp.message_handler(lambda message: message.text == "Биология🌱")
async def without_puree(message: types.Message):
    await message.reply("Биолигия👉👈")

@dp.message_handler(Text(equals="Планы разработчика🧑🏼‍💻"))
async def with_puree(message: types.Message):
    await message.reply("1. Решение проблемы с отправкой фоток. " 
                        "2. Придумать как подключить оплату дани великому Казару Мазарову и чтоб вам были доступны его услуги." 
                        "3. Бот оператор 4.Подключение к серверу 5. Получить зп. "
                        "6. Создание блэкджека со шлюхами (Шлюх может и не будет, но блэкджек наверняка")

@dp.message_handler(lambda message: message.text == "Результат разработчика👨🏼‍💻")
async def without_puree(message: types.Message):
    await message.reply("За выходные был cоздан и проходящий тесты первый inline (доступен по команде /inline)."
                        " Была добавлена кнопка результатов для посетителей.Также скоро ожидается масшатбное обновление с измением меню и добавлением подписки с тестом Юkassa. "
                        "Теперь на аватарке весит флаг империи и по команде /slogan будет доступен слоган компании")

@dp.message_handler(Text(equals="Pay💸"))
async def with_puree(message: types.Message):
    await message.reply('<a href="https://yookassa.ru/developers/payment-acceptance/getting-started/payment-methods">Реквизиты оплаты</a>',parse_mode="HTML")

@dp.message_handler(lambda message: message.text == "Обществознание🧑‍️")
async def without_puree(message: types.Message):
    await message.reply("Ты станешь моим адвокатом?")

if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)