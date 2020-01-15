from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import utils

import config
import os
import json
import requests
import subprocess
import shlex

updater = Updater(token=config.telegramToken, use_context=True)
dispatcher = updater.dispatcher
users=dict()

def loadUser():
    global users
    try:
        with open('user.json') as json_file:
            users = json.load(json_file)
    except FileNotFoundError:
        saveUser()

def saveUser():
    global users
    with open('user.json', 'w') as f:
        json.dump(users, f)
    loadUser()

def doCheckedPostRequest(url):
    try:
        requests.post(url,json={'color':0.6})
    except Exception as e:
        print("Error in post: ", e)

def printFile(userID,file,lprCmd=None):
    global users
    doCheckedPostRequest("http://fs-ceiling:5000/printer")
    if lprCmd is None:
        if users[str(userID)]:
            #os.system('lpr -o sides=two-sided-long-edge '+file)
            lprCommand='lpr -o sides=two-sided-long-edge '+file
            subprocess.run(shlex.split(lprCommand))
        else:
            #os.system('lpr -o sides=one-sided '+file)
            lprCommand='lpr -o sides=one-sided '+file
            subprocess.run(shlex.split(lprCommand))
    else:
        lprCommand='lpr '+str(lprCmd)+' '+file
        subprocess.run(shlex.split(lprCommand))
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="An authorization request has been sent")
    button_list = [
    InlineKeyboardButton("Ja", callback_data=str(update.effective_chat.id)),
    InlineKeyboardButton("Nein", callback_data="none")]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(chat_id=config.adminChatID,text='Darf '+update.effective_chat.first_name+' admin sein?', reply_markup=reply_markup)

def admin_handle(update, cbContext):
    global users
    button=str(update.callback_query.data)
    
    query = update.callback_query

    if button != "none":
        users[int(button)]=True
        saveUser()
        query.edit_message_text(text="User authorized")
        cbContext.bot.send_message(chat_id=int(button), text="You can now print")
    else:
        query.edit_message_text(text="Request declined")

def checkAdmin(id):
    global users
    return str(id) in users

def photo(update, cbContext):
    isAdmin=checkAdmin(update.effective_chat.id)
    if isAdmin:
        file_id = update.message.photo[-1].file_id
        newFile = cbContext.bot.getFile(file_id)
        newFile.download('temp')
        cbContext.bot.sendMessage(chat_id=update.message.chat_id, text="Picture will be printed")
    
        printFile(update.message.chat_id,'temp',lprCmd=update.effective_message.caption)

def document(update, cbContext):
    if checkAdmin(update.effective_chat.id):
        file_id = update.message.document.file_id
        newFile = cbContext.bot.getFile(file_id)
        newFile.download('temp')
        cbContext.bot.sendMessage(chat_id=update.message.chat_id, text="File will be printed")
    
        printFile(update.message.chat_id,'temp',lprCmd=update.effective_message.caption)

def makeOneSided(update, cbContext):
    global users
    isAdmin=checkAdmin(update.effective_chat.id)
    if isAdmin:
        users[str(update.effective_chat.id)]=False

def makeTwoSided(update, cbContext):
    global users
    isAdmin=checkAdmin(update.effective_chat.id)
    if isAdmin:
        users[str(update.effective_chat.id)]=True

def printAusleih(update, cbContext):
    isAdmin=checkAdmin(update.effective_chat.id)
    if isAdmin:
        splitted = update.message.text.split()
        count=1
        if(len(splitted)>1):
            count=splitted[1]
        
        if splitted[0]=="printVrFormular":
            printFile(update.effective_chat.id,config.vrFormular,"# "+count)
        elif splitted[0]=="printVrListe":
            printFile(update.effective_chat.id,config.vrListe,"# "+count)


pdf_handler = MessageHandler(Filters.photo, photo)
start_handler = CommandHandler('start', start)
oSided = CommandHandler('onesided', makeOneSided)
tSided = CommandHandler('twosided', makeTwoSided)

doc_handler = MessageHandler(Filters.document, document)
admin_handler=CallbackQueryHandler(admin_handle)

dispatcher.add_handler(pdf_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(doc_handler)
dispatcher.add_handler(admin_handler)
dispatcher.add_handler(oSided)
dispatcher.add_handler(tSided)
dispatcher.add_handler(CommandHandler('printVrFormular', printAusleih))
dispatcher.add_handler(CommandHandler('printVrListe', printAusleih))

loadUser()

updater.start_polling()