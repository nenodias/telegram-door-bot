import os
import pdb
import telebot
import logging
import threading
from flask import Flask
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UserApartment



config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}
logging.basicConfig(filename=config["LOGFILE"])

app = Flask(__name__)
cors = CORS(app)

engine = create_engine(config["ENGINE"])
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

'''
Criar o usuário utilizandoo @botFather
/newbot
Recebendo o token você pode validar o token e o bot chamando
https://api.telegram.org/bot<TOKEN>/getMe
'''
print(config["TOKEN"])
bot = telebot.TeleBot(config["TOKEN"], parse_mode=None)

def get_now():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = None
    user_name = None
    apartment = None
    now = get_now()
    with session() as s:
        s.begin()
        try:
            menssagem = message.text.split()
            user_id = message.chat.id
            user_name = message.chat.username
            if not user_name:
                user_name = "%s%s"%(message.chat.first_name, message.chat.last_name)
            apartment = int(menssagem[1])
            query = s.query(UserApartment).filter(UserApartment.user_id == user_id, UserApartment.apartment == apartment)
            if not query.all():
                user = UserApartment(user_id = user_id, user_name = user_name, apartment = apartment)
                s.add(user)
                s.commit()
            bot.reply_to(message, "%s - Usuário '%s' foi cadastrado como morador do apartamento '%s'" % (now, user_name, apartment))
        except Exception as e:
            logging.error(e)
            if not apartment:
                apartment = "Vazio"
            bot.reply_to(message, "%s - Erro ao cadastrar o usuario: '%s' no apartamento '%s'" % (now, user_name, apartment))
            s.rollback()


@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = None
    user_name = None
    now = get_now()
    with session() as s:
        s.begin()
        try:
            user_id = message.chat.id
            user_name = message.chat.username
            if not user_name:
                user_name = "%s%s"%(message.chat.first_name, message.chat.last_name)
            s.query(UserApartment).filter(UserApartment.user_id == user_id).delete()
            s.commit()
            bot.reply_to(message, "%s - Usuário %s foi removido como morador." % (now, user_name))
        except Exception as e:
            logging.error(e)
            bot.reply_to(message, "%s - Erro ao remover o usuario: '%s'." % (now, user_name))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    now = get_now()
    bot.reply_to(message, "%s - Olá para se cadastrar como um morador use /add <número do apartamento>, para se descadastrar de TODOS os apartamentos use /remove" %(now))

@app.route("/door/<int:apartment>")
def door(apartment):
    with session() as s:
        s.begin()
        try:
            users = s.query(UserApartment).filter(UserApartment.apartment == apartment).all()
            now = get_now()
            for user in users:
                bot.send_message(user.user_id, "%s - Alguém está na porta!!!" %(now))
            return "Moradores avisados!"
        except Exception as e:
            logging.error(e)
            s.rollback()
    return "Erro ao avisar moradores!"

@app.route("/door/<int:apartment>/<person>")
def door_person(apartment, person):
    with session() as s:
        s.begin()
        try:
            users = s.query(UserApartment).filter(UserApartment.apartment == apartment).all()
            now = get_now()
            for user in users:
                bot.send_message(user.user_id, "%s - %s está na porta!!!" %(now, person))
            return "Moradores avisados!"
        except Exception as e:
            logging.error(e)
            s.rollback()
    return "Erro ao avisar moradores!"

def bot_thread():
    global bot
    bot.polling()

if __name__=="__main__":
    try:
        t1 = threading.Thread(target=bot_thread, args=())
        t1.start()
        app.run(host="0.0.0.0", port=8000)
        t1.join()
    except KeyboardInterrupt:
        if bot:
            bot.stop_polling()
        print("Bye bye")

