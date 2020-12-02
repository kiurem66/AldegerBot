import telebot
import dice
import sys
import requests
import logging

def extract_arg(arg):
    command_length = len(arg.split()[0])
    if len(arg) == command_length:
        raise NoArgumentsError()
    return arg[command_length+1:]

def isUser(user_id):
    for u in users:
        if(u.id == user_id):
            return True
    return False

def isAdmin(user_id):
    if(user_id == 607608190 or user_id == 640632571): #add other admin
        return True
    return False


error_message = "Questo è un messaggio di errore, se lo vedi significa che Bridge non mi ha programmato decentemente, per favore contatta @kiurem66"
connection_error = "Oh no, sembra che io abbia dei problemi di connessione, le chiedo cortesemente di rinivare il suo comando.\nIn caso questo errore si dovesse verificare troppo spesso le chiedo gentilmente di contattare @kiurem66, potrebbe esserci qualche errore più grave in realtà"
user_error = "Signore/a, mi duole informarla che non ho capito cosa intende, forse sta usando il comando in modo errato?"

class NoArgumentsError(Exception):
    pass


class CharSheet:
    def __init__(self, strength, dexterity, intelligence, health):
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.health = health
        self.constitution = health*10
        self.base_speed = (dexterity + health)/4
        #todo le altre statistiche


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.sheet = None
        self.refMaster = None
        self.strike = 0
    def give_strike(self):
        self.strike += 1
        if self.strike == 3:
            return True
        return False


logger = telebot.logger
formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
ch = logging.StreamHandler(sys.stdout)
logger.addHandler(ch)
logger.setLevel(logging.INFO)  # or use logging.INFO
ch.setFormatter(formatter)
token = open("token.txt", "r").readline()
bot = telebot.TeleBot(token, False)
users = []

#handlers
@bot.message_handler(content_types=["new_chat_members"])
def foo(message):
    if isUser(message.from_user.id):
        bot.reply_to(message, "Bentornato alla locanda " + message.from_user.first_name+ "!")
    else:
        bot.reply_to(message, "Bevenuto alla mia locanda " + message.from_user.first_name + "\nIl mio nome è Aldeger e sono l'oste, la prego di leggere il regolamento qui sotto linkato. <link regolamento>, io la assisterò nella gestione della scheda e nel tiro dei dadi. \npuò usare /help per scoprire i miei comandi.\nPer registrarsi usi /register \n\nAldeger Nothing v0.1.0BETA, magirobot programmato dal professor Bridge")

@bot.message_handler(commands=["deluser"])
def deluser(message):
    if isUser(message.from_user.id):
        try:
            response = extract_arg(message.text)
            if response == "YES":
                for u in users:
                    if u.id == message.from_user.id:
                        users.remove(u)
                        break
                bot.reply_to(message, "Operazione completata... Scusi chi è lei?")
            else:
                bot.reply_to(message, user_error)
                print(response)
        except:
            bot.reply_to(message, "ATTENZIONE, mi sta chiedendo di eliminare il suo profilo, questo eliminerà anche la sua scheda.\n se è sicuro ripeta il comando con l'aggiunta di YES in questo modo.\n /deluser YES")            
    else:
        bot.reply_to(message, "Mi dispiace, non posso dimenticarmi di qualcuno che già non conosco")

@bot.message_handler(commands=["admin"])
def admin(message):
    to_send = message.text[7:]
    if len(to_send) == 0:
        bot.send_message(640632571, message.from_user.first_name + " ha pingato gli admin")
        bot.send_message(607608190, message.from_user.first_name + " ha pingato gli admin")
    else:
        bot.send_message(640632571, message.from_user.first_name + " ha scritto " + to_send)
        bot.send_message(607608190, message.from_user.first_name + " ha scritto " + to_send)

@bot.message_handler(commands=["register"])
def register(message):
    if isUser(message.from_user.id):
        bot.reply_to(message, "Oh... signore/a la conosco bene, credeva forse che mi dimenticassi di lei? Nel caso lo volesse veramente, usi il comando /deluser")
    else:
        users.append(User(message.from_user.id, message.from_user.first_name))
        bot.reply_to(message, "Capito, da questo momento mi ricorderò di lei.\nIn caso voglia creare un personaggio usi il comando /newchara, ma le consiglio di parlarne con me in un luogo più privato.")

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
        to_parse = extract_arg(command) + "+0"
        result = dice.roll(to_parse.strip())
        to_send = "I dadi hanno detto " + str(result)
        bot.reply_to(message, to_send)
    except dice.exceptions.DiceException:
        bot.reply_to(message, "Signore/a, mi duole informarla che il modo in cui mi chiede di lanciare i dadi è errato.\nDovrebbe rispettare codesta sintassi:\n/roll d20\n/roll d20 + 5\n/roll 3d6")
    except NoArgumentsError:
        bot.reply_to(message, "Signore/a, mi duole informarla che il modo in cui mi chiede di lanciare i dadi è errato.\nDovrebbe rispettare codesta sintassi:\n/roll d20\n/roll d20 + 5\n/roll 3d6")
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

@bot.message_handler(commands={"ban"})
def ban(message):
    try:
        if isAdmin(message.from_user.id):
            to_ban = extract_arg(message.text)
            chat_id = message.chat.id
            ban_id = 0
            for u in users:
                if u.name == to_ban:
                    ban_id = u.id
                    users.remove(u)
                    break
            if ban_id == 0:
                bot.reply_to(message, "Mi dispiace signore ma l'utente non è registrato, dovrà rimuoverlo lei")
            else:
                bot.reply_to(message, "COMANDO RICEVUTO\nAVVIO OMICIDIO.EXE\n\n*Prende una doppietta*\nMi dispiace " + to_ban +", ma devo rimuoverle i suoi privilegi di vita.")
                bot.kick_chat_member(chat_id, ban_id, 0)
        else:
            bot.reply_to(message, "Mi perdoni signore/a, ma lei non è autorizzato/a ad utilizzare questo comando.")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
         bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"strike"})
def strike(message):
    try:
        if isAdmin(message.from_user.id):
            to_ban = extract_arg(message.text)
            chat_id = message.chat.id
            ban_id = 0
            for u in users:
                if u.name == to_ban:
                    ban_id = u.id
                    if u.give_strike():
                        bot.reply_to(message, "COMANDO RICEVUTO\nAVVIO OMICIDIO.EXE\n\n*Prende una doppietta*\nMi dispiace " + to_ban +", ma lei ha raggiunto 3 strike e devo rimuoverle i suoi privilegi di vita.")
                        bot.kick_chat_member(chat_id, ban_id, 0)
                        users.remove(u)
                    else:
                        bot.reply_to(message, "Strike inviato, " + str(u.name) + " è a " + str(u.strike) + " strike, a 3 strike verrà bannato.")
                    break
            if ban_id == 0:
                bot.reply_to(message, "Mi dispiace signore ma l'utente non è registrato.")
        else:
            bot.reply_to(message, "Mi perdoni signore/a, ma lei non è autorizzato/a ad utilizzare questo comando.")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message,connection_error)
    except NoArgumentsError:
         bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

for u in users:
    print(u.name)
print("Aldeger is running")
while True:
    bot.polling(none_stop=True)
    print("bot reboot")