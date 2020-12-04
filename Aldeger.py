import telebot
import dice
import sys
import requests
import logging
import math
import copy

group_id = -448687865
admins = [607608190, 640632571]

def my_round(number):
    decimal = number - int(number)
    if decimal < 0.5:
        return int(number)
    else:
        return int(number)+1


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
    for id in admins:
        if user_id == id:
            return True
    return False

def atkCalc(lvl, atype):
    base = ""
    if lvl <= 10:
        offset = -int((10-lvl)/2)
        base = "1d6"+str(offset)
        if atype == "i":
            base+="-1"
        elif atype == "a":
            base += "-2"
    elif lvl <= 250:
        if atype == "i":
            lvl -= 2
        elif atype == "a":
            lvl -= 4
        dice_number = my_round(lvl/10)
        offset = math.ceil((lvl - dice_number*10) / 2)
        base = str(dice_number)+"d6+0"+str(offset)
    elif lvl <= 260:
        offset = -int((260-lvl)/2)
        base = "8d20"+str(offset)
        if atype == "i":
            base+="-1"
        elif atype == "a":
            base += "-2"
    elif lvl <= 400:
        if atype == "i":
            lvl -= 2
        elif atype == "a":
            lvl -= 4
        dice_number = my_round((lvl-250)/10) + 7
        offset = math.ceil((lvl - my_round(lvl/10)*10) / 2)
        base = str(dice_number)+"d20+0"+str(offset)
    elif lvl <= 410:
        offset = -int((410-lvl)/2)
        base = "15d30"+str(offset)
        if atype == "i":
            base+="-1"
        elif atype == "a":
            base += "-2"
    elif lvl <= 600:
        if atype == "i":
            lvl -= 2
        elif atype == "a":
            lvl -= 4
        dice_number = my_round((lvl-400)/10) + 14
        offset = math.ceil((lvl - my_round(lvl/10)*10) / 2)
        base = str(dice_number)+"d30+0"+str(offset)
    elif lvl <= 610:
        offset = -int((610-lvl)/2)
        base = "18d60"+str(offset)
        if atype == "i":
            base+="-1"
        elif atype == "a":
            base += "-2"
    elif lvl <= 800:
        if atype == "i":
            lvl -= 2
        elif atype == "a":
            lvl -= 4
        dice_number = my_round((lvl-600)/10) + 17
        offset = math.ceil((lvl - my_round(lvl/10)*10) / 2)
        base = str(dice_number)+"d60+0"+str(offset)
    elif lvl <= 810:
        offset = -int((810-lvl)/2)
        base = "23d100"+str(offset)
        if atype == "i":
            base+="-1"
        elif atype == "a":
            base += "-2"
    elif lvl <= 900:
        if atype == "i":
            lvl -= 2
        elif atype == "a":
            lvl -= 4
        dice_number = my_round((lvl-800)/10) + 22
        offset = math.ceil((lvl - my_round(lvl/10)*10) / 2)
        base = str(dice_number)+"d100+0"+str(offset)
    elif lvl <= 910:
        offset = -int((910-lvl)/2)
        base = "28d120"+str(offset)
        if atype == "i":
            base+="-1"
        elif atype == "a":
            base += "-2"
    else:
        if atype == "i":
            lvl -= 2
        elif atype == "a":
            lvl -= 4
        dice_number = my_round((lvl-900)/10) + 27
        offset = math.ceil((lvl - my_round(lvl/10)*10) / 2)
        base = str(dice_number)+"d120+0"+str(offset)
    return base


error_message = "Questo è un messaggio di errore, se lo vedi significa che Bridge non mi ha programmato decentemente, per favore contatta @kiurem66"
connection_error = "Oh no, sembra che io abbia dei problemi di connessione, le chiedo cortesemente di rinivare il suo comando.\nIn caso questo errore si dovesse verificare troppo spesso le chiedo gentilmente di contattare @kiurem66, potrebbe esserci qualche errore più grave in realtà"
user_error = "Signore/a, mi duole informarla che non ho capito cosa intende, forse sta usando il comando in modo errato?"

class NoArgumentsError(Exception):
    pass


class CharSheet:
    def __init__(self, strength = 0, dexterity = 0, intelligence = 0, health = 0):
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.health = health
        self.constitution = health*10
        self.base_speed = (dexterity + health)/4
        self.dodge = self.base_speed + 3
        self.movement = int(self.base_speed)
        self.parry = (health + strength)/4
        self.actions = 2
        self.abilities = []
        self.weapons = []
        self.armors = []
        self.items = []
        self.gold = 0
        self.silver = 0
        self.copper = 0
        self.block = 0
        self.pros = []
        self.cons = []
        self.race = ""
        self.sex = ""
        self.height = 0
        self.weight = 0
        self.name = ""
        self.aclass = ""
        self.attacks = []
        self.xp = 40
    
    def add_strength(self, to_add):
        self.strength += to_add
        self.parry = (self.health + self.strength)/4
    
    def add_dexterity(self, to_add):
        self.dexterity += to_add
        self.base_speed = (self.dexterity + self.health)/4
        self.dodge = self.base_speed + 3
        self.movement = int(self.base_speed)
    
    def add_health(self, to_add):
        self.health += to_add
        self.constitution = self.health*10
        self.base_speed = (self.dexterity + self.health)/4
        self.parry = (self.health + self.strength)/4
    
    def add_intelligence(self, to_add):
        self.intelligence += to_add

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




class Attack:
    def __init__(self, name, level, atype):
        self.name = name
        self.atype = atype
        self.level = level
    def rolldamage(self):
        to_roll = atkCalc(self.level, self.atype)
        return dice.roll(to_roll)


logger = telebot.logger
formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
ch = logging.StreamHandler(sys.stdout)
logger.addHandler(ch)
logger.setLevel(logging.INFO)  # or use logging.INFO
ch.setFormatter(formatter)
token = open("token.txt", "r").readline()
bot = telebot.TeleBot(token, False)

users = []
editingSheetUsers = []

#handlers
@bot.message_handler(content_atypes=["new_chat_members"])
def foo(message):
    if isUser(message.from_user.id):
        bot.reply_to(message, "Bentornato alla locanda " + message.from_user.username+ "!")
    else:
        bot.reply_to(message, "Bevenuto alla mia locanda " + message.from_user.username + "\nIl mio nome è Aldeger e sono l'oste, la prego di leggere il regolamento qui sotto linkato. <link regolamento>, io la assisterò nella gestione della scheda e nel tiro dei dadi. \npuò usare /help per scoprire i miei comandi.\nPer registrarsi usi /register \n\nAldeger Nothing v0.1.0BETA, magirobot programmato dal professor Bridge")

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
        bot.send_message(640632571, message.from_user.username + " ha pingato gli admin")
        bot.send_message(607608190, message.from_user.username + " ha pingato gli admin")
    else:
        bot.send_message(640632571, message.from_user.username + " ha scritto " + to_send)
        bot.send_message(607608190, message.from_user.username + " ha scritto " + to_send)

@bot.message_handler(commands=["register"])
def register(message):
    if isUser(message.from_user.id):
        bot.reply_to(message, "Oh... signore/a la conosco bene, credeva forse che mi dimenticassi di lei? Nel caso lo volesse veramente, usi il comando /deluser")
    else:
        users.append(User(message.from_user.id, message.from_user.username))
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
        bot.reply_to(message, "/register: mi da il consenso a ricordarmi di lei e a memorizzare la sua scheda\n\n/helpedit: visualizza i comandi relativi alla modifica della scheda\n\n/deluser serve a farmi dimenticare tutte le informazioni su di lei, da usare in caso voglia uscire dal gruppo o voglia creare un nuovo personaggio\n\n/admin: pinga un admin\n\n/admin <messaggio>: fa arrivare un messaggio ad un admin\n\n/roll <dadi>: mi fa tirare dei dadi, la seconda cosa più importante in un GDR\n\n/rolldmg <nome>: mi fa tirare un attacco applicando già i bonus e malus della tabella, a patto che sia presente nella sua scheda ovviamente")
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
                    for u1 in editingSheetUsers:
                        if u1.id == ban_id:
                            editingSheetUsers.remove(u1)
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
                        for u1 in editingSheetUsers:
                            if u1.id == ban_id:
                                editingSheetUsers.remove(u1)
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

@bot.message_handler(commands={"saytogroup"})
def say(message):
    if isAdmin(message.from_user.id):
        try:
            to_say = extract_arg(message.text)
            bot.send_message(group_id, to_say)
        except requests.exceptions.ConnectionError:
            bot.reply_to(message,connection_error)
        except NoArgumentsError:
            bot.reply_to(message, user_error)
        except Exception as e:
            bot.reply_to(message, error_message)
            print(e)

@bot.message_handler(commands={"newchara"})
def newchara(message):
    if isUser(message.from_user.id):
        for u in users:
            if u.id == message.from_user.id:
                if u.sheet == None:
                    u.sheet = CharSheet()
                    editingSheetUsers.append(copy.deepcopy(u))
                    bot.reply_to(message, "Personaggio creato, ora lo potrà modificare a piacimento. Le consiglio di modificare le sue caratteristiche in privato o in un gruppo insieme ad un master. Per avere più informazioni sui comandi per la modifica dei personaggi usi il comando /helpedit")
                else:
                    bot.reply_to(message, "Lei possiede già una scheda personaggio, se vuole creare un nuovo personaggio deve eliminare il suo profilo con /deluser")
                break
    else:
        bot.reply_to(message, "Mi dispiace ma lei non è registrato/a, deve usare il comando /register per poter creare un personaggio")

@bot.message_handler(commands={"savechara"})
def savechara(message):
    found = False
    for u in editingSheetUsers:
        if u.id == message.from_user.id:
            found = True
            for u1 in users:
                if u1.id == u.id:
                    users.remove(u1)
                    break
            users.append(u)
            bot.reply_to(message,"Modifiche salvate, se vuole riprendere a modificare si /editchara")
            #codice per salvare
            break
    if not found:
        bot.reply_to(message,"Lei non è registrato/a o non sta modificando lo scheda. Per entrare in modalità modifica usi /editchara")

@bot.message_handler(commands={"discardedit"})
def discardedit(message):
    found = False
    for u in editingSheetUsers:
        if u.id == message.from_user.id:
            found = True
            editingSheetUsers.remove(u)
            bot.reply_to(message,"Modifiche scartate, se vuole riprendere a modificare si /editchara")
            break
    if not found:
        bot.reply_to(message,"Lei non è registrato/a o non sta modificando lo scheda. Per entrare in modalità modifica usi /editchara")

@bot.message_handler(commands={"usexp"})
def useXP(message):
    try:
        for u in editingSheetUsers:
            if u.id == message.from_user.id:
                xp = int(extract_arg(message.text))
                if xp<0:
                    bot.reply_to(message, "Signore/a, mi dispiace dirle che mi sono accorto di quello che sta tentando di fare, devo dire che sono deluso, aggiungersi XP in questo modo sembra una mossa molto infantile")
                    break
                u.sheet.xp -= xp
                break
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"addattack", "addatk"})
def addAttack(message):
    try:
        for u in editingSheetUsers:    
            if u.id == message.from_user.id:
                args = extract_arg(message.text).split()
                name = args[0]
                lvl = int(args[1])
                atype = args[2]
                if (atype != "i" and atype != "f" and atype != "i") or lvl<1:
                    bot.reply_to(message, user_error)
                    break
                if u.sheet.xp < lvl:
                    bot.reply_to(message, "I suoi XP sono insufficienti")
                    break
                to_add = Attack(name, lvl, atype)
                u.sheet.attacks.append(to_add)
                u.sheet.xp -= lvl
                bot.reply_to(message, "attacco " + name + " aggiunto")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"rolldmg"})
def rollDmg(message):
    try:
        found = False
        to_calc = extract_arg(message.text)
        for u in users:
            if u.id == message.from_user.id:
                for atk in u.sheet.attacks:
                    if atk.name == to_calc:
                        found = True
                        dmg = atk.rolldamage()
                        bot.reply_to(message, "I danni sono " + str(dmg))
                        break
        if found == False:
            bot.reply_to(message, "Mi duole informarla che non ho trovato l'attacco che mi ha chiesto, oppure lei non è registrato")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"givexp"})
def givexp(message):
    try:
        if isAdmin(message.from_user.id):
            args = extract_arg(message.text).split()
            name = args[0]
            to_give = int(args[1])
            found = False
            for u in users:
                if u.name == name:
                    found = True
                    u.sheet.xp += to_give
                    if u.sheet.xp < 0:
                        u.sheet.xp = 0
                    bot.reply_to(message, "Capito signore, sto dando " + str(to_give) + " punti esperienza a " + name)
                    break
            if found == False:
                bot.reply_to(message, "Mi dispiace, non ho trovato l'utente che intende")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"helpedit"})
def helpedit(message):
    try:
        bot.reply_to(message, "/newchara: crea un nuovo personaggio ed entra in modalità modifica\n\n/editchara: entra in modalità modifica\n\n/addatk <nome> <livello> <tipo>: aggiunge un attacco di tipo f, a, i\n\n/savechara: salva le modifiche al personaggio. Se le modifiche non venono salvate verranno usate le vecchie caratteristiche")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
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