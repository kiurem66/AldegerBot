import telebot
import dice
import sys
import requests
import logging

def extract_arg(arg):
    command_length = len(arg.split()[0])
    if len(arg) == command_length:
        raise NoArgumentsError()
    return arg[command_length:]

error_message = "Questo è un messaggio di errore, se lo vedi significa che Bridge non mi ha programmato decentemente, per favore contatta @kiurem66"
connection_error = "Oh no, sembra che io abbia dei problemi di connessione, le chiedo cortesemente di rinivare il suo comando.\nIn caso questo errore si dovesse verificare troppo spesso le chiedo gentilmente di contattare @kiurem66, potrebbe esserci qualche errore più grave in realtà"

class NoArgumentsError(Exception):
    pass


class Scheda:
    def __init__(self, strength, dexterity, intelligence, health):
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.health = health
        self.constitution = health*10
        self.base_speed = (dexterity + health)/4
        #todo le altre statistiche


logger = telebot.logger
formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
ch = logging.StreamHandler(sys.stdout)
logger.addHandler(ch)
logger.setLevel(logging.INFO)  # or use logging.INFO
ch.setFormatter(formatter)

token = open("token.txt", "r").readline()

bot = telebot.TeleBot(token, False)

@bot.message_handler(content_types=["new_chat_members"])
def foo(message):
    bot.reply_to(message, "Bevenuto alla mia locanda " + message.from_user.first_name + "\nIl mio nome è Aldeger e sono l'oste, la prego di leggere il regolamento qui sotto linkato. <link regolamento>, io la assisterò nella gestione della scheda e nel tiro dei dadi. \npuò usare /help per scoprire i miei comandi. \n\nAldeger Nothing v0.0.2BETA, magirobot programmato dal professor Bridge")

@bot.message_handler(commands=["vivalon"])
def city(message):
    try:
        chat_id = message.chat.id
        bot.send_photo(chat_id, photo=open("images/vivalon.jpg","rb"))
        bot.send_message(chat_id, "Questa è Vivalon, la nostra splendida città, in una foto scattata da me medesimo durante una gita in mongolfiera")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands=["mercato"])
def market(message):
    try:
        chat_id = message.chat.id
        bot.send_photo(chat_id, photo=open("images/mercato.jpg","rb"))
        bot.send_message(chat_id, "Questo è il mercato cittadino, se hai bisogno di fare acquisti puoi dirigerti lì.\nPer farlo puoi passare di qui\n--->tg://join?invite=AAAAAFevPSByNw5y9nkasA")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message,connection_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands=["torre"])
def tower(message):
    try:
        chat_id = message.chat.id
        bot.send_photo(chat_id, photo=open("images/torre.jpg","rb"))
        bot.send_message(chat_id, "Questa è la misteriosa torre al centro di Vivalon, non sappiamo come sia stata costruita o perché la leggenda dica che ogni avventuriero che raggiunge il fondo vedrà un suo desiderio realzzato.\nUna cosa la sappiamo però, è piena di mostri pronti a farvi la pelle e di tesori da trovare.\n In caso descidiate di entrarvici... in bocca al Worg!")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message,connection_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"roll", "r"})
def rollbot(message):
    try:
        command = message.text
        id_chat = message.chat.id
        to_parse = extract_arg(command) + "+0"
        result = dice.roll(to_parse.strip())
        to_send = "I dadi hanno detto " + str(result)
        bot.reply_to(message, to_send)
    except dice.exceptions.DiceException:
        bot.reply_to(message, "Signore, mi duole informarla che il modo in cui mi chiede di lanciare i dadi è errato.\nDovrebbe rispettare codesta sintassi:\n/roll d20\n/roll d20 + 5\n/roll 3d6")
    except NoArgumentsError:
        bot.reply_to(message, "Signore, mi duole informarla che il modo in cui mi chiede di lanciare i dadi è errato.\nDovrebbe rispettare codesta sintassi:\n/roll d20\n/roll d20 + 5\n/roll 3d6")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message,connection_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"help"})
def help(message):
    try:
        bot.reply_to(message, "lorem ipsum")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message,connection_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

print("Aldeger is running")
while True:
    bot.polling(none_stop=True)
    print("bot reboot")