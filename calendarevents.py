# Custom Modules
import misc
from consts import *

# Python Modules
import datetime
import json

# Google Calendar API Modules
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Telegram Bot API Modules
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import telegram

# Loads the events from the local JSON
def load():
    with open('currentevents.json', 'r') as f:
        return json.load(f)
    
# Fetches the events from the server
def fetch(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                singleEvents=True, maxResults=100,
                                                orderBy='startTime').execute()
        events = events_result.get('items')
        if not events:
            return []

    except HttpError as error:
        misc.logln("HTTP Error in fetching the events from the server - "+error)
        return None
        
    # Standardizes the event data starting and ending date and time
    for k,e in enumerate(events):
        if 'date' in e['start'].keys():
            events[k]['start']['date'] = datetime.datetime.strptime(events[k]['start']['date'],"%Y-%m-%d")
            events[k]['end']['date'] = datetime.datetime.strptime(events[k]['end']['date'],"%Y-%m-%d")
            
            events[k]['start']['date'] = events[k]['start']["date"].strftime("%d/%m/%Y")
            events[k]['start']['time'] = "All Day"
            events[k]['end']['date'] = events[k]['end']["date"].strftime("%d/%m/%Y")
            events[k]['end']['time'] = "All Day"
            
        elif 'dateTime' in e['start'].keys():     
            events[k]['start']['dateTime'] = datetime.datetime.strptime(events[k]['start']['dateTime'],"%Y-%m-%dT%H:%M:%S+%U:%W")
            events[k]['end']['dateTime'] = datetime.datetime.strptime(events[k]['end']['dateTime'],"%Y-%m-%dT%H:%M:%S+%U:%W")
            
            events[k]['start']['date'] = events[k]['start']["dateTime"].strftime("%d/%m/%Y")
            events[k]['start']['time'] = events[k]['start']["dateTime"].strftime("%H:%M")
            events[k]['end']['date'] = events[k]['end']["dateTime"].strftime("%d/%m/%Y")
            events[k]['end']['time'] = events[k]['end']["dateTime"].strftime("%H:%M")
            events[k]['start'].pop("dateTime")
            events[k]['end'].pop("dateTime")
    
    # Filters only relevant event parameters
    keys = ['summary','description','start','end','colorId']
    for k,e in enumerate(events):
        events[k] = { your_key: e.get(your_key) for your_key in keys }
    
    # Writes to JSON file
    eventsjson = json.dumps(events, indent = 4)
    with open("currentevents.json", "w") as f:
        f.write(eventsjson)
        
    return events


def modifychosen_callback(update, context):
    return


def modify_callback(update, context):
    events_keyboard = []
    global events
    for e in events:
        events_keyboard.append(
            [InlineKeyboardButton(color[e['colorId']]+" "+e['summary'], callback_data=modifychosen_callback)]
        )
        
        update.message.reply_text(
            "Which event do you want to modify?",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    return MENU

def add_callback(update,context):
    query = update.callback_query
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Type the details of the event you want to create:\n"+
        "_Start Date_\n"+
        "_Start Time_\n"+
        "_Name_\n"+
        "_Description_\n"+
        "(write '.' in the field you want to ignore)",
        parse_mode=telegram.ParseMode.MARKDOWN,
    )
    return NEW_EVENT

def new_callback(update, context):
    query = update.callback_query
    eventtext = update.message.text.split("\n")
    global event
    event = events[-1]
    event['date']['start'] = eventtext[0] if eventtext[0]!="." else None
    event['time']['start'] = eventtext[1] if eventtext[1]!="." else None
    event['summary'] = eventtext[2] if eventtext[2]!="." else None
    event['description'] = eventtext[3] if eventtext[3]!="." else None
    
    events.append((event))
    symbols = [
        [InlineKeyboardButton(color[None],callback_data=color[None]),
         InlineKeyboardButton(color['1'],callback_data=color['1']),
         InlineKeyboardButton(color['2'],callback_data=color['2']),
         InlineKeyboardButton(color['3'],callback_data=color['3']),],
        
        [InlineKeyboardButton(color['4'],callback_data=color['4']),
         InlineKeyboardButton(color['5'],callback_data=color['5']),
         InlineKeyboardButton(color['6'],callback_data=color['6']),
         InlineKeyboardButton(color['7'],callback_data=color['7']),],
        
        [InlineKeyboardButton(color['8'],callback_data=color['8']),
         InlineKeyboardButton(color['9'],callback_data=color['9']),
         InlineKeyboardButton(color['10'],callback_data=color['10']),
         InlineKeyboardButton(color['11'],callback_data=color['11']),],
    ]
    
    reply_markup = InlineKeyboardMarkup(symbols)
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Choose the category",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup = reply_markup
    )
    return finalize_callback(update,context)
    # event = service.events().insert(calendarId='primary', body=event).execute()
    
def finalize_callback(update, context):
    event['colorID'] = update.callback_query.data
    events.append((event))
    return MENU
    
def show_callback(update, context):
    events = load()
    
    for e in events:
        # One day events
        if e['start']['date'] == e['end']['date']:
            
            # All day events
            if e['start']['time'] == "All Day":
                msg_text = "*"+e['start']['date']+"  All Day*\n"
                msg_text += color[e.get("colorId")]+" "+e['summary']+"\n\n"
                if e.get("description") is not None: msg_text += e.get('description')[:100]
                
            else:
                msg_text = "*"+e['start']['date']+"*-_"+e['start']['time']+"_ ➡️ *"+ e['end']['date']+"*-_"+e['end']['time']+"_\n"
                msg_text += color[e.get("colorId")]+" "+e['summary']+"\n\n"
                if e.get("description") is not None: msg_text += e.get('description')[:100]
                
        # Multiple day events
        else:
            msg_text = "*"+e['start']['date']+" ➡️ "+ e['end']['date']+"*\n"
            msg_text += color[e.get("colorId")]+" "+e['summary']+"\n\n"
            if e.get("description") is not None: msg_text += e.get('description')[:100]
            
        update.message.reply_text(
            msg_text,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    buttons = [
        [InlineKeyboardButton("🆕Add Event",callback_data="addevent_callback"),
        InlineKeyboardButton("♻️Modify Event",callback_data="modifyevent_callback"),
        InlineKeyboardButton("💣Delete Event",callback_data="deleteevent_callback")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        "Next",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup = reply_markup
    )
    return MENU