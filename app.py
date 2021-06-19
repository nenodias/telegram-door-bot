import telebot
import json
import os
from flask import Flask
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}
app = Flask(__name__)

'''
Criar o usuário utilizandoo @botFather
/newbot
Recebendo o token você pode validar o token e o bot chamando
https://api.telegram.org/bot<TOKEN>/getMe
'''

bot = telebot.TeleBot(config["TOKEN"], parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    dados = message.chat
    pdb.set_trace()
    #print(dados)
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    #print(message)
    pdb.set_trace()
    bot.reply_to(message, message.text)


@app.route("/")
def index():
    bot.send_message(72520957,'Hello')
    return "Hello World!"

if __name__=="__main__":
    #bot.polling()
    #pdb.set_trace()
    app.run(host="0.0.0.0", port=80)

