from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import utils

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

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def start(update, context):
    message="Hi, i'am the FIUS Printer.\nPlease send me the files you want to print\n"
    message+="Your chat id is: "+str(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    button_list = [
    InlineKeyboardButton("Ja", callback_data=str(update.effective_chat.id)),
    InlineKeyboardButton("Nein", callback_data="none")]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(chat_id=telegramapi.adminChatID,text='Darf '+update.effective_chat.first_name+' admin sein?', reply_markup=reply_markup)

def admin_handle(update, cbContext):
    button=update.callback_query.data
    if button is not "none":
         users.append(button)
         saveUser()

def checkAdmin(id):
    return id in users

def photo(update, cbContext):
    file_id = update.message.photo[-1].file_id
    newFile = cbContext.bot.getFile(file_id)
    newFile.download('temp')
    cbContext.bot.sendMessage(chat_id=update.message.chat_id, text="download successfull")
    if checkAdmin(update.effective_chat.id):
        printFile('temp')

def document(update, cbContext):
    file_id = update.message.document.file_id
    newFile = cbContext.bot.getFile(file_id)
    newFile.download('temp')
    cbContext.bot.sendMessage(chat_id=update.message.chat_id, text="download successfull")
    if checkAdmin(update.effective_chat.id):
        printFile('temp')

pdf_handler = MessageHandler(Filters.photo, photo)
start_handler = CommandHandler('start', start)
doc_handler = MessageHandler(Filters.document, document)
admin_handler=CallbackQueryHandler(admin_handle)

dispatcher.add_handler(pdf_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(doc_handler)
dispatcher.add_handler(admin_handler)

loadUser()

updater.start_polling()