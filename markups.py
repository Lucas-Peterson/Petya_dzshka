from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#----------main meny--------------
btnSub = KeyboardButton('Покупка подписки💸')
mainMenu = ReplyKeyboardMarkup(resize_keyboard= True)
mainMenu.add(btnSub)
#----------Subs Button-------------
sub_inline_markup = InlineKeyboardMarkup(row_width=1)
btnSubMonth = InlineKeyboardButton(text="Месяц - 400 рублей", callback_data="submonth")
sub_inline_markup.insert(btnSubMonth)
#----------Основа------------------


