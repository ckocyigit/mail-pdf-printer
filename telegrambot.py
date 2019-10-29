from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import telegramapi
import os
import json

updater = Updater(token=telegramapi.telegramToken, use_context=True)
dispatcher = updater.dispatcher
users=[]

def saveUser():
    global users
    with open('user.json', 'w') as f:
        json.dump(users, f)

def loadUser():
    global users
    with open('user.json') as json_file:
        users = json.load(json_file)

def printFile(file):
    os.system('lpr  -o sides=two-sided-long-edge '+file)
    os.system('rm '+file)

def start(update, context):
    message="Hi, i'am the FIUS Printer.\nPlease send me the files you want to print"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def photo(update, cbContext):
    file_id = update.message.photo[-1].file_id
    newFile = cbContext.bot.getFile(file_id)
    newFile.download('temp')
    cbContext.bot.sendMessage(chat_id=update.message.chat_id, text="download successfull")
    printFile('temp')

def document(update, cbContext):
    file_id = update.message.document.file_id
    newFile = cbContext.bot.getFile(file_id)
    newFile.download('temp')
    cbContext.bot.sendMessage(chat_id=update.message.chat_id, text="download successfull")
    printFile('temp')

pdf_handler = MessageHandler(Filters.photo, photo)
start_handler = CommandHandler('start', start)
doc_handler = MessageHandler(Filters.document, document)

dispatcher.add_handler(pdf_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(doc_handler)


updater.start_polling()