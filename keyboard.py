from telebot import types

markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_main = types.KeyboardButton('Получить цитату')
markup_main.add(key_main)
