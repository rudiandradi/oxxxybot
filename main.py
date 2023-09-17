"""
Telegram inline bot that returns Oxxxymiron's custom quotes
"""

import telebot
import random
import config

from uuid import uuid4
from phrases import dct
from keyboard import markup_main
from telebot import types

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext

bot = telebot.TeleBot(config.bot_token)

used_punches = []

def return_punch():
    """
    Main function to return the unique qoute
    """
    global used_punches
    
    if len(used_punches) != len(dct):
        num = random.randint(1, len(dct))
        if num not in used_punches:
            used_punches.append(num)
            return dct[num]
        else:
            return_punch()
    else:
        used_punches = []
        return_punch()

def inlinequery(update: Update, _: CallbackContext):
    """
    Function that presents inline query title
    """
    results = [InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="ВЫДАТЬ ПАНЧ",
                    input_message_content=InputTextMessageContent(return_punch(),
                                                                  parse_mode=ParseMode.HTML),
                )]
    update.inline_query.answer(results, cache_time=0)

@bot.message_handler(commands=['start'])
def start(message):
    """
    Start command
    """
    msg = dct[random.randint(1, len(dct))]
    send = bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=markup_main)
    createUser(message)
    bot.register_next_step_handler(send, main)

@bot.inline_handler(func=lambda query: len(query.query) == 0)
def empty_query(query):
    r = types.InlineQueryResultArticle(
            id=str(uuid4()),
            title='Поделиться панчем',
            input_message_content=types.InputTextMessageContent(return_punch(), parse_mode='html'))

    bot.answer_inline_query(query.id, [r])

@bot.message_handler(content_types=['text'])
def message_handlers(message):
    if message.chat.type == 'private':
        if (str(message.text)).lower() == 'получить цитату':
            msg = dct[random.randint(1, len(dct))]
            send = bot.send_message(message.chat.id, msg, parse_mode='html')
            bot.register_next_step_handler(send, main)

def main() :
    updater = Updater(config.bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(InlineQueryHandler(inlinequery,run_async=True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
