import os
import pdb
import threading
from flask import Flask
from flask_cors import CORS
from utils import get_now
from bot import create_bot, init_bot
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UserApartment

config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}
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

@app.route("/door/<int:apartment>")
def door(apartment):
    bot = create_bot(config["TOKEN"]) 
    with session() as s:
        s.begin()
        try:
            users = s.query(UserApartment).filter(UserApartment.apartment == apartment).all()
            now = get_now()
            for user in users:
                bot.send_message(user.user_id, "%s - Alguém está na porta!!!" %(now))
            return "Moradores avisados!"
        except:
            s.rollback()
    return "Erro ao avisar moradores!"

@app.route("/door/<int:apartment>/<person>")
def door_person(apartment, person):
    bot = create_bot(config["TOKEN"])
    with session() as s:
        s.begin()
        try:
            users = s.query(UserApartment).filter(UserApartment.apartment == apartment).all()
            now = get_now()
            for user in users:
                bot.send_message(user.user_id, "%s - %s está na porta!!!" %(now, person))
            return "Moradores avisados!"
        except:
            s.rollback()
    return "Erro ao avisar moradores!"

def bot_thread():
    while True:
        try:
            bot = create_bot(config["TOKEN"])
            init_bot(bot, session, UserApartment)
            bot.polling()
        except Exception as ex:
            print("Exception: %s"%(ex))

if __name__=="__main__":
    try:
        t1 = threading.Thread(target=bot_thread, args=())
        t1.start()
        app.run(host="0.0.0.0", port=8000)
        t1.join()
    except KeyboardInterrupt:
        print("Bye bye")
    except Exception as ex:
        print(ex)

