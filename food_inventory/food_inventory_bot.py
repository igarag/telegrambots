# -*- coding: utf-8 -*-

import os
import telebot, tempfile, subprocess
from telebot import types
import time
import json
from environs import Env


env = Env()
env.read_env()

token = env.str("TOKEN", "")

bot = telebot.TeleBot(token)

HELP = '\n/help - Guide to know how to use the bot   \
        \n/new_word - Add a new word to your database.\
        \n/list - Return all words of your list.\
        \n/hello - Saludo del Bot.'


GROUP = "ADMIN"

list_of_users =  ["NachoAz"]
list_of_groups = env.list("GROUPS", "")
 
chat_id = bot.get_me().id
#print("Wai --> ", bot.get_me())
############################################ 

# Checks if the user belongs to the list
def check_user(user):
    if user in list_of_users:
        return True
    return False


def check_group(group):
    if group in list_of_groups:
        return True
    return False


@bot.message_handler(commands=["chat_id"])
def chat_id(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, chat_id)


@bot.message_handler(commands=["start"])
def command_start(message):
    chat_id = message.chat.id

    if check_group(str(chat_id)):
        username = message.from_user.first_name

        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Inventario')
        itembtn2 = types.KeyboardButton('Añadir')
        itembtn3 = types.KeyboardButton('Editar')
        itembtn4 = types.KeyboardButton('Borrar')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        response = "Hola humano (también conocido como {nombre}). Puedes utilizar los siguientes comandos para interactuar conmigo:\n {HELP}"
        bot.send_message(chat_id, response.format(nombre=username, HELP=HELP), reply_markup=markup)

    else:
        response = "Permiso denegado."
        bot.send_message(chat_id, response)


@bot.message_handler(commands=['hola'])
def command_hello(m):
    chat_id = m.chat.id
    audio = open('./img/R2D2_SOUND.mp3', 'rb')
    bot.send_audio(chat_id, audio)


@bot.message_handler(commands=['inventory'])
@bot.message_handler(func=lambda message: message.text == 'Inventario')
def inventory(message):
    chat_id = message.chat.id

    with open('inventory.json', 'r') as inventory:
        raw_inventory = inventory.read()

    data = json.loads(raw_inventory)
    response = ""
    for element, value in data.items():
        response += f"- {element}: {value} \n"
    bot.send_message(chat_id, response, parse_mode='Markdown')


@bot.message_handler(commands=['add'])
@bot.message_handler(func=lambda message: message.text == 'Añadir')
def add(message):
    chat_id = message.chat.id
    response = "Add element"
    bot.send_message(chat_id, response, parse_mode='Markdown')

@bot.message_handler(commands=['edit'])
@bot.message_handler(func=lambda message: message.text=='Editar')
def edit(message):
    chat_id = message.chat.id
    response = "Edit element"
    bot.send_message(chat_id, response, parse_mode='Markdown')


@bot.message_handler(commands=['delete'])
@bot.message_handler(func=lambda message: message.text=='Borrar')
def delete(message):
    chat_id = message.chat.id
    response = "Delete element"
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


@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text == 'Ayuda')
def query_text(m):

    username = m.from_user.first_name

    chat_id = m.chat.id
    text = '\n\n\n\nEstos son los comandos que puedes usar:'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Inventario", callback_data="inventory"))
    markup.add(types.InlineKeyboardButton("Añadir", callback_data="add"))
    markup.add(types.InlineKeyboardButton("Editar", callback_data="edit"))
    markup.add(types.InlineKeyboardButton("Borrar", callback_data="delete"))
    ret_msg = bot.send_message(chat_id, text, disable_notification=True, reply_markup=markup)

    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Inventario')
    itembtn2 = types.KeyboardButton('Añadir')
    itembtn3 = types.KeyboardButton('Editar')
    itembtn4 = types.KeyboardButton('Borrar')
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
    print("                 INVENTORY FOOD (telegram bot)")
    print("=================================================================\n\n")

    # Load the data
    bot.set_update_listener(listener) # The listener function is registered.
    bot.infinity_polling(True)        # The server is listening.

