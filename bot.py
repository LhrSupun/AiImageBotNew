from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import requests
import re
import logging
import profile
import os
import redis

rsp = redis.from_url(os.environ.get(('REDISURL')))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def usrupdate(update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    rsp.set (user_name, user_id)

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_random():
    contents = requests.get('https://fakeface.rest/face/json').json()
    return contents

def get_image_url():
    allowed_extension = ['png','jpg','jpeg']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

@run_async
def boop(update, context):
    url = get_image_url()
    chat_id = update.message.chat_id

    cap = "Here's random dogo for you.. try /rnd or /help"
    context.bot.send_photo(chat_id=chat_id, photo=url, caption=cap)

@run_async
def rnd(update, context):
    chat_id = update.message.chat_id
    content = get_random()
    url = content['image_url']
    usrupdate(update)
    cap = "age: "+str(content['age'])+" gender: "+str(content['gender'])+" source: "+str(content['source'])+""
    context.bot.send_photo(chat_id=chat_id, photo=url, caption=cap)

def help_command(update, context):
    usrupdate(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text='1) To receive a Ai generated person type /rnd .\n' + '2) To receive a random dog image type /boop.\n')

def start(update: Update, _: CallbackContext) -> None:
    usrupdate(update)
    keyboard = [
        [InlineKeyboardButton("help", callback_data='/help')],
        [InlineKeyboardButton("Message the developer", callback_data='https://t.me/ultimate_lurker69')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text=f"check this out: {query.data}")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.. try /boop")

def addHandlersToTelegramBotAndStartIt(updater, dispatcher):
    unknown_handler = MessageHandler(Filters.command, unknown)
    rnd_handler = CommandHandler('boop', boop)
    newimg_handler = CommandHandler('rnd', rnd)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    update_hander = CallbackQueryHandler(button)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(update_hander)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(rnd_handler)
    dispatcher.add_handler(newimg_handler)
    dispatcher.add_handler(unknown_handler)
    updater.start_polling()

def main():
    print(os.environ.get('BOTTOKEN'))
    TOKEN = os.environ.get(('BOTTOKEN'))
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    addHandlersToTelegramBotAndStartIt(updater, dp)

if __name__ == '__main__':
    main()
