# %%
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# %% e
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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

try:
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

except HttpError as error:
    print('An error occurred: %s' % error)

from telegram.ext import (Updater, 
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,    
    Filters
)
import datetime
with open("telegramapi.txt") as f:
        tokens = f.readlines()
bot_token = tokens[0].strip("\n")
updater = Updater(token=bot_token, use_context=True)
        

        
print(">> "+datetime.datetime.now().strftime("[%d/%m/%Y-%H:%M:%S]-BOT: ")+
        " Loading Telegram bot: ",end="")
dispatcher = updater.dispatcher
print("SUCCESS") if updater!=0 else print("FAIL")

def send_message(context):
    user_id = 410773404
    context.bot.send_message(
        chat_id=user_id,
        text="Enculet!"
    )

def printid(update, context):
    userid = update.message.from_user['id']
    print(userid)
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=userid
    )


# dispatcher.add_handler(CommandHandler('send_message', send_message))
# dispatcher.add_handler(CommandHandler('start', printid))

# jobqueue = updater.job_queue
# jobqueue.run_repeating(
#     callback=send_message,
#     interval=1,
# )

MENU = 0
import telegram
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


def events_callback(update, context):
    user_id = update.message.from_user['id']
    menu_options = [
        ['Events','Tasks']
    ]
    
    events_keyboard = []
    for e in events:
        print(e['summary'])
        if 'date' in e['start'].keys():
            events_keyboard.append(
                [InlineKeyboardButton(e['start']['date']+" - "+e['summary'], 
                                     callback_data=e['id'])]
            )
        elif 'dateTime' in e['start'].keys():
            events_keyboard.append(
                [InlineKeyboardButton(e['start']['dateTime']+" - "+e['summary'], 
                                     callback_data=e['id'])]
            )
            
    reply_markup = InlineKeyboardMarkup(events_keyboard)
    
    update.message.reply_text(
       "Your Events:",
        parse_mode=telegram.ParseMode.HTML,
        reply_markup = reply_markup
    )
    return MENU

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
        reply_markup=InlineKeyboardMarkup(
            menu_options, 
            one_time_keyboard=True,
            resize_keyboard=True,
            )
    )
    return MENU

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

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu',menu)],
        states={
            MENU: 
                [
                MessageHandler(Filters.regex('^(Events)$'), events_callback),
                MessageHandler(Filters.regex('^(Tasks)$'), tasks_callback),
                ],
        },
        fallbacks=[CommandHandler('menu', menu)]
)
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(CommandHandler('menu', menu))

updater.start_polling()
updater.idle()

# %%



