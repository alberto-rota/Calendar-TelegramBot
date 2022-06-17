# Custom Modules
from consts import *
# Python Modules
import datetime

# Google Calendar API Modules

# Telegram Bot API Modules
from telegram import ReplyKeyboardMarkup



# Logs 'text' to the terminal with the current timestamp
def log(text, logger="BOT"):
    print(">> "+datetime.datetime.now().strftime("[%d/%m/%Y-%H:%M:%S]")
          +"-"+logger+": "+text,end="")
# Same, only with a newline
def logln(text, logger="BOT"):
    print(">> "+datetime.datetime.now().strftime("[%d/%m/%Y-%H:%M:%S]")
            +"-"+logger+": "+text,end="\n")
    
# Centers a text string
def center(text, w,sep='_'):
    ext = sep
    left = (w-len(text))//2
    right = w-left-len(text)
    return left*ext+ text + right*ext

def menu(update, context):
    user_id = update.message.from_user['id']
    print(">> "+datetime.datetime.now().strftime(f"[%d/%m/%Y-%H:%M:%S]-{user_id}: ")+
        " MENU request ")
    
    menu_options = [
        ['Events','Tasks']
    ]

    update.message.reply_text(
        "Select from the menu:  ",
        reply_markup=ReplyKeyboardMarkup(
            menu_options, 
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    return MENU