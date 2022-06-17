from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
import telegram

from consts import *

import datetime

def tasks_callback(update,context):
    client=context.dispatcher.user_data['client']
    user_id = update.message.from_user['id']
    menu_options = [
        ['Events','Tasks']
    ]

    update.message.reply_text(
        text="Showing Tasks NOW",
        # chat_id=update.effective_chat.id,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(
            menu_options, 
            one_time_keyboard=True,
            resize_keyboard=True,
            )
    )
    return MENU