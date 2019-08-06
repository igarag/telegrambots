# Telegram Bot

## Vocabulary reminder



## Requirements:

### Create the Virtual Environment

```bash
virtualenv -p python3 --no-site-packages telegrambot-env
```

Activate the virtual environment (i have all virtual environments stored in `~/.virtualenvironments`).

```bash
source ~/.virtualenvironments/telegrambot-env/bin/activate
```

### Install packages

The required packages are:

- `pyTelegramBotAPI`
- `websocket-client`

And we can install from `requirements.txt` file typing:

```bash
pip install -r requirements.txt
```


### Database

The bot will connect to a simple database (`sqlite`) to exchange requests.

Documentation about how to connect Python application with simple database, can be found [here](https://medium.com/@DrGabrielA81/python-how-connect-to-and-manage-a-database-68b113a5ca62).



### TelegramBot API

```python
@bot.message_handler(commands=['piensa3D'])
def command_piensa3D(m):
    cid = m.chat.id
    Piensa3D = open('favicon_jderobot.png', 'rb')
    xxx=open('xxx.mp3', 'rb')
    yyy=open('yyy.mp4', 'rb')
    zzz=open('zzz.jpg', 'rb')
    bot.send_sticker(cid, Piensa3D)
    bot.send_audio(cid, xxx)
    bot.send_video(cid, yyy)
    bot.send_photo(cid, zzz)
    bot.send_message(cid, "hola")
    piensa3D.close()
    xxx.close()
    yyy.close()
    zzz.close()
```

