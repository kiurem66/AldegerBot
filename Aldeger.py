import telebot
import dice
import sys
import requests
import logging
import math
import copy
import pickle

group_id = -448687865
admins = [607608190, 640632571, 198257047, 156707897]
version = "1.0.1"

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

def get_user(user_id):
    for u in users:
        if(u.id == user_id):
            return u
    return None

def get_editing(user_id):
    for u in editingSheetUsers:
        if u.id == user_id:
            return u
    return None

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


error_message = "Questo è un messaggio di errore, se lo sta vedendo significa che il dottor Bridge non mi ha programmato in modo adeguato, per favore contatti @kiurem66"
connection_error = "Oh no, sembra che io abbia dei problemi di connessione, le chiedo cortesemente di inivare nuovamente il suo comando.\nIn caso questo errore si dovesse verificare troppo spesso le chiedo gentilmente di contattare @kiurem66, potrebbe esserci qualche errore più grave in realtà"
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
        self.skills = []
        self.platinum = 0
        self.gold = 0
        self.silver = 0
        self.copper = 0
        self.block = 0
        self.race = ""
        self.sex = ""
        self.height = 0
        self.weight = 0
        self.name = ""
        self.aclass = ""
        self.attacks = []
        self.xp = 0
    
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
    def __init__(self, name, base_car, atype):
        self.name = name
        self.atype = atype
        self.base_car = base_car

class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level


logger = telebot.logger
formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
ch = logging.StreamHandler(sys.stdout)
logger.addHandler(ch)
logger.setLevel(logging.INFO)  # or use logging.DEBUG
ch.setFormatter(formatter)
token = open("token.txt", "r").readline()
bot = telebot.TeleBot(token, False)

users = []
editingSheetUsers = []

#handlers
@bot.message_handler(content_atypes=["new_chat_members"])
def newuser(message):
    if get_user(message.from_user.id) != None:
        bot.reply_to(message, "Bentornato alla locanda " + message.from_user.username+ "!")
    else:
        bot.reply_to(message, "Bevenuto alla mia locanda " + message.from_user.username + "\nIl mio nome è Aldeger e sono l'oste, la prego di leggere il regolamento qui sotto linkato. <link regolamento>, io la assisterò nella gestione della scheda e nel tiro dei dadi. \npuò usare /help per scoprire i miei comandi.\nPer registrarsi usi /register \n\nAldeger "+version+", magirobot programmato dal dottor Bridge")

@bot.message_handler(commands=["deluser"])
def deluser(message):
    u = get_user(message.from_user.id)
    if u != None:
        try:
            response = extract_arg(message.text)
            if response == "YES":
                users.remove(u)
                u1 = get_editing(message.from_user.id)
                if u1 != None:
                    editingSheetUsers.remove(u1)
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
        for a in admins:
            bot.send_message(a, message.from_user.username + " ha pingato gli admin")
    else:
        for a in admins:
            bot.send_message(a, message.from_user.username + " ha scritto " + to_send)

@bot.message_handler(commands=["register"])
def register(message):
    try:
        if get_user(message.from_user.id) != None:
            bot.reply_to(message, "Oh... signore/a la conosco bene, credeva forse che mi dimenticassi di lei? Nel caso lo volesse veramente, usi il comando /deluser")
        else:
            users.append(User(message.from_user.id, message.from_user.username))
            bot.reply_to(message, "Capito, da questo momento mi ricorderò di lei.\nIn caso voglia creare un personaggio usi il comando /newchara, ma le consiglio di parlarne con me in un luogo più privato.")
            f = open("users","wb")
            pickle.dump(users, f)
            f.close()
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

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
        bot.reply_to(message, "/register: mi da il consenso a ricordarmi di lei e a memorizzare la sua scheda\n\n/newchara <nome>,<forza>,<destrezza>,<intelligenza>,<salute>: crea un nuovo personaggio ed entra in modalità modifica(la somma delle 4 caratteristiche deve essere 45)\n\n/helpedit: visualizza i comandi relativi alla modifica della scheda\n\n/deluser: serve a farmi dimenticare tutte le informazioni su di lei, da usare in caso voglia uscire dal gruppo o voglia creare un nuovo personaggio\n\n/editmoney <tipo><numero>: si possono aggiungere o togliere monete di tipo c,f,p,q (si ha completa libertà, evitare di andare in negativo o di aggiungersi troppe monete, può risultare in uno strike)\n\n/admin: pinga un admin\n\n/admin <messaggio>: fa arrivare un messaggio ad un admin\n\n/roll <dadi>: mi fa tirare dei dadi, la seconda cosa più importante in un GDR\n\n/rolldmg <nome>: mi fa tirare un attacco applicando già i bonus e malus della tabella, a patto che sia presente nella sua scheda ovviamente.\n\n/showchara: mostra la sua scheda (se non vuole che gli altri giocatori la vedono le condsiglio di farlo in privato)\n\nCi sono anche alcuni comandi relativi all'ambientazione che non citerò qui per motivi di trama.\n\nAldeger "+version+", magirobot programmato dal dottor Bridge")
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
                    u1 = get_editing(ban_id)
                    if u1 != None:
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
                        u1 = get_editing(ban_id)
                        if u1 != None:
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
    try:
        u = get_user(message.from_user.id)
        if u != None:
            if u.sheet == None:
                args = extract_arg(message.text).split(",")
                stre = int(args[1].strip())
                dext = int(args[2].strip())
                inte = int(args[3].strip())
                salu = int(args[4].strip())
                if (stre + dext + inte + salu) != 45:
                    bot.reply_to(message, "La somma delle caratteristiche base deve essere 45, la prego di riprovare con le caratteristiche corrette.")
                else:
                    u.sheet = CharSheet(stre, dext, inte, salu)
                    u.sheet.name = args[0]
                    editingSheetUsers.append(copy.deepcopy(u))
                    bot.reply_to(message, "Personaggio creato " +args[0] + ", ora lo potrà modificare a piacimento. Le consiglio di modificare le sue caratteristiche in privato o in un gruppo insieme ad un master. Per avere più informazioni sui comandi per la modifica dei personaggi usi il comando /helpedit")
            else:
                bot.reply_to(message, "Lei possiede già una scheda personaggio, se vuole creare un nuovo personaggio deve eliminare il suo profilo con /deluser")
        else:
            bot.reply_to(message, "Mi dispiace ma lei non è registrato/a, deve usare il comando /register per poter creare un personaggio")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"savechara"})
def savechara(message):
    try:
        to_save = get_editing(message.from_user.id)
        if to_save == None:
            bot.reply_to(message,"Lei non è registrato/a o non sta modificando lo scheda. Per entrare in modalità modifica usi /editchara")
        else:
            for u1 in users:
                if u1.id == to_save.id:
                    users.remove(u1)
                    break
            editingSheetUsers.remove(to_save)
            users.append(to_save)
            f = open("users","wb")
            pickle.dump(users, f)
            f.close()
            bot.reply_to(message,"Modifiche salvate, se vuole riprendere a modificare si /editchara")
    except Exception as e:
            bot.reply_to(message, error_message)
            print(e)

@bot.message_handler(commands={"discardedit"})
def discardedit(message):
    to_discard = get_editing(message.from_user.id)
    if to_discard == None:
        bot.reply_to(message,"Lei non è registrato/a o non sta modificando lo scheda. Per entrare in modalità modifica usi /editchara")
    else:
        editingSheetUsers.remove(to_discard)
        bot.reply_to(message,"Modifiche scartate, se vuole riprendere a modificare si /editchara")


@bot.message_handler(commands={"addattack", "addatk"})
def addAttack(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None:
            args = extract_arg(message.text).split(",")
            try:
                name = args[0]
                base_car = args[1].strip()
                atype = args[2].strip()
            except:
                print("a")
                raise NoArgumentsError
            if (atype != "i" and atype != "f" and atype != "a") or (base_car != "f" and base_car != "d" and base_car != "i"):
                bot.reply_to(message, user_error)
                print("b")
                return
            to_add = Attack(name, base_car, atype)
            u.sheet.attacks.append(to_add)
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
        to_calc = extract_arg(message.text)
        u = get_user(message.from_user.id)
        if u == None:
            bot.reply_to(message, "Mi duole informarla che non ho trovato l'attacco che mi ha chiesto, oppure lei non è registrato")
        else:
            if u.id == message.from_user.id:
                found = False
                for atk in u.sheet.attacks:
                    if atk.name == to_calc:
                        found = True
                        if atk.base_car == "f":
                            to_roll = atkCalc(u.strength, atk.atype)
                        elif atk.base_car == "d":
                            to_roll = atkCalc(u.dexterity, atk.atype)
                        else:
                            to_roll = atkCalc(u.intelligence, atk.atype)
                        dmg = dice.roll(to_roll)
                        bot.reply_to(message, "I danni sono " + str(dmg))
                        break
                if not found:
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
            args = extract_arg(message.text).split(",")
            try:
                name = args[0]
                to_give = int(args[1].strip())
            except:
                raise NoArgumentsError
            found = False
            for u in users:
                if u.name == name:
                    found = True
                    u.sheet.xp += to_give
                    if u.sheet.xp < 0:
                        u.sheet.xp = 0
                    u1 = get_editing(u.id)
                    if u1 != None:
                        u1.sheet.xp += to_give
                        if u1.sheet.xp < 0:
                            u1.sheet.xp = 0
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
        bot.reply_to(message, "/newchara <nome>,<forza>,<destrezza>,<intelligenza>: crea un nuovo personaggio ed entra in modalità modifica(la somma delle 4 caratteristiche deve essere 45)\n\n/editchara: entra in modalità modifica\n\n/addatk <nome>,<caratteristica>,<tipo>: aggiunge un attacco di tipo f, a, i. Con una caratteristica base\n\n/addskill <nome>,<livello>: aggiunge un'abilità\n\n/lvlskill <skill>: aumenta il livello di una skill\n\n/lvlcar <car>: aumenta il livello di una caratteristica base (f,d,i,s)\n\n/buyaction: spende punti xp per comprare un azione\n\n/setrace <razza>: imposta la razza\n\n/setclass <classe>: imposta la classe\n\n/setsex <sesso>: imposta il sesso\n\n/setweight <peso>: imposta il peso\n\n/setheight <altezza>: imposta l'altezza\n\n/setblock <blocco>: imposta il blocco\n\n/savechara: salva le modifiche al personaggio. Se le modifiche non vengono salvate verranno usate le vecchie caratteristiche")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"showchara"})
def showchara(message):
    try:
        u = get_user(message.from_user.id)
        if u == None:
            bot.reply_to(message, "Mi dispiace ma lei non è registrato/a, deve usare il comando /register per poter creare un personaggio")
        else:
            if u.sheet == None:
                bot.reply_to(message, "Mi dispiace ma lei non ha alcuna scheda personaggio, può crearla con il comando /newchara")
            else:
                to_print = "---Scheda Personaggio---\n\n"
                to_print += "Nome: " + u.sheet.name + "\nRazza: " + u.sheet.race + "\nClasse: " + u.sheet.aclass + "\nSesso: " + u.sheet.sex + "\nAltezza: " + str(u.sheet.height) + "\nPeso: " + str(u.sheet.weight) + "\n\n"
                to_print += "Caratteristiche\nFOR: " + str(u.sheet.strength) + "\nDES: " + str(u.sheet.dexterity) + "\nINT: " + str(u.sheet.intelligence) + "\nSAL: " + str(u.sheet.health) + "\n\n"
                to_print += "Costituzione: " + str(u.sheet.constitution) + "\nVelocità base: " + str(u.sheet.base_speed) + "\nSchivata: " + str(u.sheet.dodge) + "\nMovimento: " + str(u.sheet.movement) + "\nParata: " + str(u.sheet.parry) + "\nBlocco: " + str(u.sheet.block) + "\nAzioni: " + str(u.sheet.actions) + "\n\n"
                to_print += "Attacchi:\n"
                for a in u.sheet.attacks:
                    to_print += a.name + " caratteristica: " + str(a.base_car) + " tipo: " + a.atype + "\n"
                to_print += "\n"
                to_print += "Abilità:\n"
                for a in u.sheet.skills:
                    to_print += a.name + " lv: " + str(a.level) + "\n"
                to_print += "\nCuori: " + str(u.sheet.platinum) + "\nFiorini: " + str(u.sheet.gold) + "\nPunte: " + str(u.sheet.silver) + "\nQuarti: " +str(u.sheet.copper)
                to_print += "\n\nPunti Esperienza: " + str(u.sheet.xp)
                bot.reply_to(message, to_print)
            
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"editchara"})
def editchara(message):
    try:
        u = get_user(message.from_user.id)
        if u == None:
            bot.reply_to(message, "Mi dispiace ma lei non è registrato/a, deve usare il comando /register per poter creare un personaggio")
        else:
            if u.sheet == None:
                bot.reply_to(message, "Mi dispiace ma lei non ha alcuna scheda personaggio, può crearla con il comando /newchara")
            else:
                editingSheetUsers.append(copy.deepcopy(u))
                bot.reply_to(message, "Modalità modifica attivata")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"addskill"})
def addskill(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None and u.sheet != None:
            arg = extract_arg(message.text)
            if u.sheet.xp<1:
                bot.reply_to(message, "Mi duole informarla che non ha abbastanza punti esperienza")
            else:
                u.sheet.xp -= 1
                to_add = Skill(arg, 1)
                u.sheet.skills.append(to_add)
                bot.reply_to(message, "abilità " + arg + " aggiunta")        
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)


@bot.message_handler(commands={"lvlskill"})
def lvlskill(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None and u.sheet != None:
            arg = extract_arg(message.text)
            Found = False
            for s in u.sheet.skills:
                if s.name == arg:
                    Found=True
                    to_spend = s.level
                    if u.sheet.xp < to_spend:
                        bot.reply_to(message, "Mi duole informarla che non ha abbastanza punti esperienza, ha bisogno di " + str(to_spend) + "px")
                        break
                    s.level += 1
                    u.sheet.xp -= to_spend
                    bot.reply_to(message,"il livello dell'abilità da lei scelta è stato aumentato a " + str(s.level))
            if not Found:
                raise NoArgumentsError            
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"lvlcar"})
def lvlcar(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None:
            arg = extract_arg(message.text)
            if arg == "f" or arg =="F":
                to_spend = u.sheet.strength
                if u.sheet.xp < to_spend:
                    bot.reply_to(message, "Mi duole informarla che non ha abbastanza punti esperienza, ha bisogno di " + str(to_spend) + "px")
                else:
                    u.sheet.add_strength(1)
                    u.sheet.xp -= to_spend
                    bot.reply_to(message,"la forza è stata aumentata a " + str(u.sheet.strength))
            elif arg == "d" or arg =="D":
                to_spend = u.sheet.dexterity
                if u.sheet.xp < to_spend:
                    bot.reply_to(message, "Mi duole informarla che non ha abbastanza punti esperienza, ha bisogno di " + str(to_spend) + "px")
                else:
                    u.sheet.add_dexterity(1)
                    u.sheet.xp -= to_spend
                    bot.reply_to(message,"la destrezza è stata aumentata a " + str(u.sheet.dexterity))
            elif arg == "i" or arg =="I":
                to_spend = u.sheet.intelligence
                if u.sheet.xp < to_spend:
                    bot.reply_to(message, "Mi duole informarla che non ha abbastanza punti esperienza, ha bisogno di " + str(to_spend) + "px")
                else:
                    u.sheet.add_intelligence(1)
                    u.sheet.xp -= to_spend
                    bot.reply_to(message,"l'intelligenza è stata aumentata a " + str(u.sheet.intelligence))
            elif arg == "s" or arg =="S":
                to_spend = u.sheet.health
                if u.sheet.xp < to_spend:
                    bot.reply_to(message, "Mi duole informarla che non ha abbastanza punti esperienza, ha bisogno di " + str(to_spend) + "px")
                else:
                    u.sheet.add_health(1)
                    u.sheet.xp -= to_spend
                    bot.reply_to(message,"la salute è stata aumentata a " + str(u.sheet.health))
            else:
                bot.reply_to(message, user_error)
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"mastercar"})
def mastercar(message):
    try:
        if isAdmin(message.from_user.id):
            u = get_editing(message.from_user.id)
            args = extract_arg(message.text).split(",")
            try:
                arg = args[0].strip()
                lvl = int(args[1].strip())
            except:
                raise NoArgumentsError
            if arg == "f" or arg =="F":
                u.sheet.add_strength(lvl)
                bot.reply_to(message,"La forza è stata aumentata a " + str(u.sheet.strength))
            elif arg == "d" or arg =="D":
                u.sheet.add_dexterity(lvl)
                bot.reply_to(message,"La destrezza è stata aumentata a " + str(u.sheet.dexterity))
            elif arg == "i" or arg =="I":
                u.sheet.add_intelligence(lvl)
                bot.reply_to(message,"L'intelligenza è stata aumentata a " + str(u.sheet.intelligence))
            elif arg == "s" or arg =="S":
                u.sheet.add_health(lvl)
                bot.reply_to(message,"La salute è stata aumentata a " + str(u.sheet.health))
            else:
                bot.reply_to(message, user_error)
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"masterskill"})
def masterskill(message):
    try:
        if isAdmin(message.from_user.id):
            u = get_editing(message.from_user.id)
            args = extract_arg(message.text).split(",")
            try:
                arg = args[0]
                lvl = int(args[1].strip())
            except:
                raise NoArgumentsError
            Found = False
            for s in u.sheet.skills:
                if s.name == arg:
                    Found=True
                    s.level += lvl
                    bot.reply_to(message,"il livello dell'abilità da lei scelta è stato aumentato a " + str(s.level))
            if not Found:
                raise NoArgumentsError
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"mastershow"})
def mastershow(message):
    try:
        if isAdmin(message.from_user.id):
            to_show = extract_arg(message.text)
            found = False
            for u in users:
                if u.name == to_show:
                    found = True
                    if u.sheet == None:
                        bot.reply_to(message, "Mi dispiace ma l'utente da lei scelto non ha una scheda personaggio.")
                    else:
                        to_print = "---Scheda Personaggio---\n\n"
                        to_print += "Nome: " + u.sheet.name + "\nRazza: " + u.sheet.race + "\nClasse: " + u.sheet.aclass + "\nSesso: " + u.sheet.sex + "\nAltezza: " + str(u.sheet.height) + "\nPeso: " + str(u.sheet.weight) + "\n\n"
                        to_print += "Caratteristiche\nFOR: " + str(u.sheet.strength) + "\nDES: " + str(u.sheet.dexterity) + "\nINT: " + str(u.sheet.intelligence) + "\nSAL: " + str(u.sheet.health) + "\n\n"
                        to_print += "Costituzione: " + str(u.sheet.constitution) + "\nVelocità base: " + str(u.sheet.base_speed) + "\nSchivata: " + str(u.sheet.dodge) + "\nMovimento: " + str(u.sheet.movement) + "\nParata: " + str(u.sheet.parry) + "\nBlocco: " + str(u.sheet.block) + "\nAzioni: " + str(u.sheet.actions) + "\n\n"
                        to_print += "Attacchi:\n"
                        for a in u.sheet.attacks:
                            to_print += a.name + " caratteristica: " + str(a.base_car) + " tipo: " + a.atype + "\n"
                        to_print += "\n"
                        to_print += "Abilità:\n"
                        for a in u.sheet.skills:
                            to_print += a.name + " lv: " + str(a.level) + "\n"
                        to_print += "\nCuori: " + str(u.sheet.platinum) + "\nFiorini: " + str(u.sheet.gold) + "\nPunte: " + str(u.sheet.silver) + "\nQuarti: " +str(u.sheet.copper)
                        to_print += "\n\nPunti Esperienza: " + str(u.sheet.xp)
                        bot.reply_to(message, to_print)
                    break
            if not found:
                bot.reply_to(message, "Mi dispiace ma l'utente da lei scelto non esiste.")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)


@bot.message_handler(commands={"buyaction"})
def buyaction(message):
    u = get_editing(message.from_user.id)
    if u != None and u.sheet != None:
        to_spend = (u.sheet.actions * 10)-10
        if to_spend > u.sheet.xp:
            bot.reply_to(message, "Mi duole informarla che non ha abbastanza punti esperienza, ha bisogno di " + str(to_spend) + "px")
        else:
            u.sheet.actions += 1
            u.sheet.xp -= to_spend
            bot.reply_to(message,"le azioni sono state aumentate a " + str(u.sheet.actions))

@bot.message_handler(commands={"editmoney"})
def setmoney(message):
    try:
        if get_editing(message.from_user.id) != None:
            bot.reply_to(message, "Per evitare errori di calcoli del denaro è impossibile modifcarlo mentre è in modalità modifica, le chiedo scusa per il disagio.")
            return
        u = get_user(message.from_user.id)
        if u == None or u.sheet == None:
            bot.reply_to(message, "Lei non è registrato/a oppure non ha una scheda personaggio.")
            return
        args = extract_arg(message.text).split(",")
        try:
            mtype = args[0].strip()
            number = int(args[1].strip())
        except:
            raise NoArgumentsError
        if mtype == "c" or mtype == "C":
            u.sheet.platinum += number
        elif mtype == "f" or mtype == "F":
            u.sheet.gold += number
        elif mtype == "p" or mtype == "P":
            u.sheet.silver += number
        elif mtype == "q" or mtype == "Q":
            u.sheet.copper += number
        else:
            raise NoArgumentsError
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"setclass"})
def setclass(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None:
            arg = extract_arg(message.text)
            u.sheet.aclass = arg
            bot.reply_to(message, "Medifica effettuata!")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"setrace"})
def setrace(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None:
            arg = extract_arg(message.text)
            u.sheet.race = arg
            bot.reply_to(message, "Modifica effettuata!")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"setsex"})
def setsex(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None:
            arg = extract_arg(message.text)
            if arg != "m" and arg != "M" and arg != "f" and arg != "F" and arg != "a" and arg != "A":
                bot.reply_to(message, "Capisco che nel mondo reale sono accettati vari generi sessuali ma questa è un ambientazione fantasy medievale, se lei si riconosce in una sessualità particolare non ho problemi ma le chiedo cortesemente di creare un personaggio che sia maschio(M), femmina(F) o assessuato(A). In caso di personaggi che nascondono il proprio sesso le chiedo di specificare il sesso reale (gli altri giocatori non potranno vedere la sua scheda).")
                return
            u.sheet.sex = arg
            bot.reply_to(message, "Modifica effettuata!")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"setheight"})
def setheight(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None:
            arg = int(extract_arg(message.text).strip())
            u.sheet.height = arg
            bot.reply_to(message, "Modifica effettuata!")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"setweight"})
def setweight(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None:
            arg = int(extract_arg(message.text).strip())
            u.sheet.weight = arg
            bot.reply_to(message, "Modifica effettuata!")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"setblock"})
def setblock(message):
    try:
        u = get_editing(message.from_user.id)
        if u != None:
            arg = int(extract_arg(message.text).strip())
            u.sheet.block = arg
            bot.reply_to(message, "Modifica effettuata!")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, connection_error)
    except NoArgumentsError:
        bot.reply_to(message, user_error)
    except ValueError:
        bot.reply_to(message, user_error)
    except Exception as e:
        bot.reply_to(message, error_message)
        print(e)

@bot.message_handler(commands={"helpmaster"})
def helpmaster(message):
    if isAdmin(message.from_user.id):
        bot.reply_to(message, "/ban <utente>: mi fa bannare un utente\n\n/strike <utente>: mi fa dare uno strike ad un utente, a 3 verrà bannato\n\n/givexp <utente>,<quantità>: assegna punti esperienza ad un utente\n\n/masterskill <abilità>,<livello>: aggiunge un livello che vuole ad un'abilità a sua scelta\n\n/mastercar <caratteristica>,<livello> aggiunge un valore a sua scelta alle caratteristiche base (f,d,i,s)\n\n/mastershow <utente>: mostra la scheda di utente a sua scelta")

try:
    f = open("users","rb")
    users = pickle.load(f)
    f.close()
except:
    users = []
print("Aldeger is running")
while True:
    bot.delete_webhook()
    bot.polling(none_stop=True)
    print("bot reboot")