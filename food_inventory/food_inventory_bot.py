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

# Load Inventory
inventory_file = "./inventory.json"
with open(inventory_file, 'r') as inventory:
    raw_inventory = inventory.read()
inventory = json.loads(raw_inventory)


commands = {
    'start': 'Comenzar a usar el bot',
    'help': 'Información con los comandos disponibles',
    'inv': 'Muestra el *inventario*.',
    'add': '*Añadir* un elemento: `add producto cantidad`.',
    'edit': '*Editar* un elemento: `edit producto cantidad`.',
    'del': '*Borrar* un elemento: `del producto`.'
}


# GROUP = "ADMIN"

list_of_users = env.list("AVAILABLE_USERS")
list_of_groups = env.list("AVAILABLE_GROUPS")
print(bot.get_me())
chat_id = bot.get_me().id
# print("Wai --> ", bot.get_me())
############################################

# Checks if the user belongs to the list
def check_user(user: str):
    if user in list_of_users:
        return True
    return False


def update_inventory(item: str, value: int, action: str):
    if action == "del":
        inventory.pop(item)
    elif action == "add" or action == "edit":
        inventory[item] = value
    with open(inventory_file, 'w') as outfile:
        json.dump(inventory, outfile)


def check_group(group: str):
    if group in list_of_groups:
        return True
    return False


@bot.message_handler(commands=["start"])
def command_start(message):
    chat_id = message.chat.id
    if check_group(str(chat_id)) or check_user(str(chat_id)):
        username = message.from_user.first_name

        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Inventario')
        itembtn2 = types.KeyboardButton('Ayuda')
        markup.add(itembtn1, itembtn2)

        response = "Hola humano (también conocido como {nombre}). \
                    Escribe `/help` o pulsa en el botón de `Ayuda` para \
                    obtener más información"

        bot.send_message(chat_id,
                         response,
                         reply_markup=markup,
                         parse_mode="Markdown")

    else:
        response = "Permiso denegado."
        bot.send_message(chat_id, response)


@bot.message_handler(commands=['hola'])
def command_hello(m):
    chat_id = m.chat.id
    audio = open('./img/R2D2_SOUND.mp3', 'rb')
    bot.send_audio(chat_id, audio)


@bot.message_handler(commands=['inv'])
@bot.message_handler(func=lambda message: "Inventario" in message.text)
def show_inventory(message):
    chat_id = message.chat.id

    response = ""
    for element, value in inventory.items():
        response += f"- {element}: {value} \n"
    if response == "":
        response = "No tienes productos en el inventario. \xF0\x9F\x98\x94"
    bot.send_message(chat_id, response, parse_mode='Markdown')



@bot.message_handler(commands=['add', 'edit'])
# @bot.message_handler(func=lambda message: "edit" or "Edit" in message.text)
def command_add_edit(message):
    chat_id = message.chat.id
    if len(message.text.split(" ")) == 1:
        response = "Faltan argumentos detrás del comando :-)"
        bot.send_message(chat_id, response, parse_mode="Markdown")
    else:
        raw_content = message.text.split(" ")
        command = str(raw_content[0])
        item = str(raw_content[1])
        value = int(raw_content[2])
        action = "edit"
        print(f"{command} - {item} - {value}")
        update_inventory(item, value, action)

        response = f"Elemento {item} editado. Ahora tiene {value} unidades"
        bot.send_message(chat_id, response, parse_mode='Markdown')


@bot.message_handler(commands=['del'])
# @bot.message_handler(func=lambda message: "del" or "Del" in message.text)
def delete(message):
    chat_id = message.chat.id

    raw_content = message.text.split(" ")
    command = str(raw_content[0])
    item = str(raw_content[1])
    value = 0
    action = "del"
    print(f"{command} - {item} - {value}")
    update_inventory(item, value, action)

    response = f"Has eliminado *{item}*"
    bot.send_message(chat_id, response, parse_mode='Markdown')

    
@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: "Ayuda" in message.text)
def command_help(m):
    cid = m.chat.id
    help_text = "Los comandos disponibles son:\n\n"
    for key in commands:
        help_text += "`/" + key + "`: "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text, parse_mode="Markdown")

# Listener - Monitor with all messages from the users
def listener(messages):

    for m in messages:
        mensaje = "[" + str(m.from_user.id) + "-" + str(m.chat.first_name) + "]: " + m.text 
        f = open( 'log.txt', 'a')
        f.write(mensaje + "\n")
        f.close()
        print(mensaje)


if __name__ == "__main__":

    print("\n\n=============================================================")
    print("             INVENTORY FOOD (telegram bot)")
    print("=============================================================\n\n")

    # Load the data
    bot.set_update_listener(listener)  # The listener function is registered.
    bot.infinity_polling(True)         # The server is listening.

