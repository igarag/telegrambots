# -*- coding: utf-8 -*-

import os
import telebot, tempfile, subprocess
from telebot import types
import time
import requests
import pyodbc
import sqlite3
import yaml


#cnxn = sqlite3.connect('database.db')


with open('./token.txt') as token_file:
    my_token = token_file.read()
token_file.close()

bot = telebot.TeleBot(my_token)

HELP = '\n/help - Guide to know how to use the bot   \
        \n/new_word - Add a new word to your database.\
        \n/list - Return all words of your list.\
        \n/hello - Saludo del Bot.'


# Definimos que cuando pongamos la palabra grupo lo vincule con el Id del grupo donde 
# nos encontremos.  Al meter el bot en un grupo, en la propia consola nos saldrá.
GROUP = "ADMIN"



list_of_users =  ["NachoAz"]
list_of_groups = ["-1001307082480", "10895420"]
 
chat_id = bot.get_me().id
#print("Wai --> ", bot.get_me())
############################################ 

# Checks if the user belongs to the list
def check_user(user):   return(True if user in list_of_users else False)
def check_group(group): return(True if group in list_of_groups else False)


@bot.message_handler(commands=["chat_id"])
def chat_id(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, chat_id)


# First view. When the user begins the communitaciont with the bot.
@bot.message_handler(commands=["start"])
def command_start(message):
    chat_id = message.chat.id

    if check_group(str(chat_id)):
        nombreUsuario = message.from_user.first_name

        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('New Word')
        itembtn2 = types.KeyboardButton('W12')
        itembtn3 = types.KeyboardButton('Help')
        markup.add(itembtn1, itembtn2, itembtn3)

        response = "Hola humano (también conocido como {nombre}). Puedes utilizar los siguientes comandos para interactuar conmigo:\n {HELP}"
        bot.send_message(chat_id, response.format(nombre=nombreUsuario, HELP=HELP), reply_markup=markup)

    else:
        response = "Permiso denegado."
        bot.send_message(chat_id, response)



# ==========================================================================

### STORE IN DATABASE
def store_word(english_word, meaning):
    print("Store the word: ", english_word, meaning)

    stored = False

    # Load the file
    with open('my_dict.yml', 'r') as yaml_file:
        my_english_dict = yaml.safe_load(yaml_file) or {}
        my_english_dict[english_word] = meaning
    if my_english_dict:
        with open('my_dict.yml', 'w') as yaml_file:
            yaml.dump(my_english_dict, yaml_file, default_flow_style=False)
            
    
    yaml_file.close()
    
    print("TO BIEN")


    

    


### Saludo
@bot.message_handler(commands=['hola'])
def command_hello(m):
    chat_id = m.chat.id
    audio = open('./img/R2D2_SOUND.mp3', 'rb')
    bot.send_audio(chat_id, audio)




### PARSER WORD
def parser_word(message):

    parser = message.split(" ")
    success = False

    if len(parser) == 3:
        header = parser[0]
        english_word = str(parser[1].lower().strip())
        meaning = str(parser[2].lower().strip())
        success = True

    return success, header, english_word, meaning










### NEW WORD BUTTON
@bot.message_handler(commands=['new_word'])
@bot.message_handler(func=lambda message: message.text == 'New Word')
def new_word_docs(message):

    chat_id = message.chat.id
    response = "**Type**: `/n <english word> <your language meaning>`"
    bot.send_message(chat_id, response, parse_mode='Markdown')

    
    

### NEW WORD FUNCTION
@bot.message_handler(commands=['n'])
def command_services(message):

    chat_id = message.chat.id
    
    success, header, english_word, meaning = parser_word(message.text)

    if success:
        # Save the word
        store_word(english_word, meaning)
        response = "`Word stored`"
        bot.send_message(chat_id, response, parse_mode='Markdown')
    else:
        response = "`An argument is missing`"
        bot.send_message(chat_id, response, parse_mode='Markdown')




### SERVICES
@bot.message_handler(commands=['services'])
@bot.message_handler(func=lambda message: message.text == 'Comprobar Servicios')
def command_services(message):
    chat_id = message.chat.id

    if check_group(str(chat_id)):
        # List of services than are down.
        list_services = ""

        for site in services:
            try:
                code = requests.get(site)
                if code.status_code != 200:
                    list_services += "❌ ➡️ `" + site + "`\n"
                elif code.status_code == 200:
                    list_services += "✅ ➡ `" + site + "`\n"
                else:
                    list_services += "❌ ➡️ `" + site + "`\n"
            except:
                list_services += "❌ ➡️ `" + site + "`\n"
                message = list_services


        # Send responses to users.
        if len(list_services) != 0:
            bot.send_message(chat_id, list_services,  parse_mode='Markdown')
        else:
            message = "\nAll services Up!\n"
            bot.send_message(chat_id, message, parse_mode='Markdown')
    else:
        response = "Permiso denegado."
        bot.send_message(chat_id, response)


'''
### HOSTS
@bot.message_handler(commands=['hosts'])
@bot.message_handler(func=lambda message: message.text == 'Comprobar Máquinas')
def command_hosts(message):
    chat_id = message.chat.id

    if check_group(str(chat_id)):
        # List of hosts than are down.
        downed_hosts = ""

        for host in hosts:
            ping = os.system("ping -c 1 -w2 " + host + " > /dev/null 2>&1")
            if ping == 0:
                downed_hosts += "✅ ➡️ `" + host + "`\n"
            else:
                downed_hosts += "❌ ➡️ `" + host + "`\n"

        if len(downed_hosts) != 0:
                bot.send_message(chat_id, downed_hosts,  parse_mode='Markdown')
        else:
            message = "\n**All hosts Up!**\n"
            bot.send_message(chat_id, message, parse_mode='Markdown')
    else:
        response = "Permiso denegado."
        bot.send_message(chat_id, response)
'''



### INLINE ANSWERS
@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text == 'Ayuda')
def query_text(m):

    nombreUsuario = m.from_user.first_name

    chat_id = m.chat.id
    text = '\n\n\n\nEstos son los comandos que puedes usar:'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Comprobar Servicios", callback_data="services"))
    markup.add(types.InlineKeyboardButton("Comprobar Máquinas", callback_data="hosts"))
    markup.add(types.InlineKeyboardButton("Ayuda", callback_data="help"))
    ret_msg = bot.send_message(chat_id, text, disable_notification=True, reply_markup=markup)

    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Comprobar Servicios')
    itembtn2 = types.KeyboardButton('Comprobar Máquinas')
    itembtn3 = types.KeyboardButton('Ayuda')
    markup.add(itembtn1, itembtn2, itembtn3)


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    chat_id = call.message.chat.id
    if call.data == "services":
        command_services(call.message)
    elif call.data == "help":
        query_text (call.message)
    elif call.data == "hosts":
        command_hosts(call.message)      
    else:
        response = "Error."
        bot.send_message(chat_id, response)
### END OF INLINE ANSWERS



# Listener - Monitor with all messages from the users
def listener(messages):

    for m in messages:
        chat_id = m.chat.id 
        mensaje = "[" + str(m.from_user.id) + "-" + str(m.chat.first_name) + "]: " + m.text 
        f = open( 'log.txt', 'a')
        f.write(mensaje + "\n")
        f.close()
        print(mensaje)


if __name__ == "__main__":

    print("\n\n=================================================================")
    print("                 Vocabulary Reminder (telegram bot)")
    print("=================================================================\n\n")

    # Load the data

    

    

    bot.set_update_listener(listener) # The listener function is registered.
    bot.infinity_polling(True)        # The server is listening.

