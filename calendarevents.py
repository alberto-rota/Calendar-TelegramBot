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
# Saves the events from the local JSON
def save(events):
    eventsjson = json.dumps(events, indent = 4)
    with open("currentevents.json", "w") as f:
        f.write(eventsjson)
    
# Generates a blanck empty event
def blankevent():
    return {'summary': '','description': '',
            'start': {'date':'','time':''},'end': {'date':'','time':''},
            'colorId': ''}

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
    save(events)
        
    return events


def modifychosen(update, context):
    return


def modify(update, context):
    events = load()
    events_keyboard = []
    for e in events:
        events_keyboard.append(
            [InlineKeyboardButton(color[e['colorId']]+" "+e['summary'], callback_data=modifychosen)]
        )
        
        update.message.reply_text(
            "Which event do you want to modify?",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    return MENU

def delete(update, context):
    events_keyboard = []
    events = load()
    for e in events:
        events_keyboard.append(
            [InlineKeyboardButton(color[e['colorId']]+" "+e['summary'], callback_data=modifychosen)]
        )
        
        update.message.reply_text(
            "Which event do you want to delete?",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    return MENU

def new(update,context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Type the details of the event you want to create:\n"+
        "_Start Date_\n"+
        "_Start Time_\n"+
        "_End Date_\n"+
        "_End Time_\n"+
        "_Name_\n"+
        "_Description_\n"+
        "(write '.' in the field you want to ignore)",
        parse_mode=telegram.ParseMode.MARKDOWN,
    )
    return NEW_EVENT

def add(update, context):
    eventtext = update.message.text.split("\n")
    events = load()
    
    global event
    event = blankevent()
    if len(eventtext) == 6:
        try:
            event['start']['date'] = eventtext[0] if eventtext[0]!="." else (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%d/%m/%Y")
            event['start']['time'] = eventtext[1] if eventtext[1]!="." else 'All Day'
            event['end']['date']   = eventtext[2] if eventtext[2]!="." else event['start']['date']
            event['end']['time']   = eventtext[3] if eventtext[3]!="." else 'All Day'
            event['summary']       = eventtext[4] if eventtext[4]!="." else 'NoNameEvent'
            event['description']   = eventtext[5] if eventtext[5]!="." else ''
        except IndexError:
            misc.logln("Error in adding the event",update.effective_chat.id)
            context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="❗This Event is not valid!❗",
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
            new()
        else:
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
            return NEW_EVENT_FINAL
            # event = service.events().insert(calendarId='primary', body=event).execute()
    else:
        misc.logln("Error in adding the event",str(update.effective_chat.id))
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="❗This Event is not valid!❗",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        new(update,context)
        
        
def finalize(update, context):
    events = load()
    global event
    event['colorId'] = colorcode[update.callback_query.data]
    events.append((event))
    misc.log("Event added: "+event['summary'])
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="*NEW EVENT ADDED*\n\n"+print(event),
        parse_mode=telegram.ParseMode.MARKDOWN,
    )
    save(events)
    return MENU
    
def query(update, context):
    query = update.callback_query.data
    if query == "newevent": 
        new(update,context)
        return NEW_EVENT
    elif query == "modifyevent": 
        modify(update,context)
        return NEW_EVENT
    elif query == "deleteevent": 
        delete(update,context)
        return NEW_EVENT
    else: # No explicit parameter means that the query content is one of the color
        finalize(update,context)
        return MENU
    
    
def show(update, context):
    events = load()
    
    for e in events:
        update.message.reply_text(
            print(e),
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    buttons = [
        [
        InlineKeyboardButton("🆕New Event",callback_data="newevent"),
        InlineKeyboardButton("♻️Modify Event",callback_data="modifyevent"),
        InlineKeyboardButton("💣Delete Event",callback_data="deleteevent")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        "Actions: ",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup = reply_markup
    )
    return MENU
    
# Produces a string of text sendable to the user
def print(e):
    # One day events
    if e['start']['date'] == e['end']['date']:
        
        # All day events
        if e['start']['time'] == "All Day":
            msg_text = "*"+e['start']['date']+" ➡️ All Day*\n"
        else:
            msg_text = "*"+e['start']['date']+"*-_"+e['start']['time']+"_ ➡️ *"+ e['end']['date']+"*-_"+e['end']['time']+"_\n"
            
    # Multiple day events
    else:
        msg_text = "*"+e['start']['date']+" ➡️ "+ e['end']['date']+"*\n"
        
    msg_text += color[e.get("colorId")]+" "+e['summary']+"\n\n"
    
    # Automatically generated descriptions may contain links with characters that conflic with themarkdown syntax
    try: 
        if e.get("description") is not None: 
            msg_text += "_"+e.get('description')[:100]+"_"
            if len(e.get("description"))>=100: msg_text += "_... [more]_"
    except e:
        msg_text += "_Description is not renderable_"
        
    return msg_text