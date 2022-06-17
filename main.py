# Custom Modules
import calendarevents
import calendartasks
import misc 
from consts import * 

# Python Modules
import datetime
import os.path
import json

# Google Calendar API Modules
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Telegram Bot API Modules
from telegram.ext import (Updater, 
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,    
    Filters
)
import telegram
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler

# Initializes Telegram API
with open("telegramapi.txt") as f:
        tokens = f.readlines()
bot_token = tokens[0].strip("\n")
updater = Updater(token=bot_token, use_context=True)
        
misc.log("Telegram Bot Initialization: ")
dispatcher = updater.dispatcher
print("SUCCESS") if updater!=0 else print("FAIL")

# Initialization of the Google Calendar API
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

misc.log("Google Calendar API Initialization: ")
global events
# Fetches the events
events = calendarevents.fetch(creds)

print("SUCCESS") if events is not None else print("FAIL")
misc.logln(f"Fetched {len(events)} events")

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu',misc.menu)],
        states={
            MENU: 
                [
                MessageHandler(Filters.regex('^(📅Events)$'), calendarevents.show),
                MessageHandler(Filters.regex('^(✅Tasks)$'), calendartasks.tasks_callback),
                MessageHandler(Filters.regex('^(🆕Add Event)$'), calendarevents.new),
                MessageHandler(Filters.regex('^(♻️Modify Event)$'), calendarevents.modify),
                MessageHandler(Filters.regex('^(💣Delete Event)$'), calendarevents.delete),
                CallbackQueryHandler(calendarevents.query)
                ],
            NEW_EVENT:
                [
                MessageHandler(Filters.text & ~Filters.command, calendarevents.add),
                ],
            NEW_EVENT_FINAL:
                [
                CallbackQueryHandler(calendarevents.query)
                ]
        },
        fallbacks=[CommandHandler('menu', misc.menu)]
)
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(CommandHandler('menu', misc.menu))
# dispatcher.add_handler(CallbackQueryHandler(calendarevents.query))

updater.start_polling()
updater.idle()