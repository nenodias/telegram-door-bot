import telebot
from utils import get_now

def create_bot(token):
    return telebot.TeleBot(token, parse_mode=None)


def init_bot(bot, session, UserApartment):

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
            except:
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
            except:
                bot.reply_to(message, "%s - Erro ao remover o usuario: '%s'." % (now, user_name))

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        now = get_now()
        bot.reply_to(message, "%s - Olá para se cadastrar como um morador use /add <número do apartamento>, para se descadastrar de TODOS os apartamentos use /remove" %(now))