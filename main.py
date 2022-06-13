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


dispatcher.add_handler(CommandHandler('send_message', send_message))
dispatcher.add_handler(CommandHandler('start', printid))

jobqueue = updater.job_queue
jobqueue.run_repeating(
    callback=send_message,
    interval=1,
)


updater.start_polling()
updater.idle()
