#!/usr/bin/python
#-*- coding: utf-8 -*-

# Telegram Bot

import telebot # Importamos las librería

TOKEN = '359085395:AAF5U9e8czMwEdj4fcF8pYR-bf1YZHYf-Qg' # Ponemos nuestro Token generado con el @BotFather
ID_BOT = 10895420

tb = telebot.TeleBot(TOKEN) # Combinamos la declaración del Token con la función de la API

tb.send_message(ID_BOT, 'Hola Carlos, soy tu bot!') # Ejemplo tb.send_message('10895420', 'Hola mundo!')
print "Wai --> ", tb.get_me()


#tb.get_update()


# Teclado de acciones
from telebot import types

markup = types.ReplyKeyboardMarkup()
markup.row('Actualizar', 'Boton2')
markup.row('Boton3', 'Boton4', 'Boton4')
tb.send_message(ID_BOT, "Mensaje 2", None, None, markup)

