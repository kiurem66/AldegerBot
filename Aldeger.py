import telebot
import dice

def extract_arg(arg):
    command_length = len(arg.split()[0])
    return arg[command_length:]

error_message = "Questo è un messaggio di errore, se lo vedi significa che Bridge non mi ha programmato decentemente, per favore contatta @kiurem66"


class Scheda:
    def __init__(self, strength, dexterity, intelligence, health):
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.health = health
        self.constitution = health*10
        self.base_speed = (dexterity + health)/4
        #todo le altre statistiche



token = "1336753758:AAHMkoEpI1S_DMSZI3M2LyOy_AP5KPyJp9A"

bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(content_types=["new_chat_members"])
def foo(message):
    bot.reply_to(message, "Bevenuto alla mia locanda " + message.from_user.first_name + "\nIl mio nome è Aldeger e sono l'oste, la prego di leggere il regolamento qui sotto linkato. <link regolamento>, io la assisterò nella gestione della scheda e nel tiro dei dadi. \npuò usare /help per scoprire i miei comandi. \n\nAldeger Nothing v0.0.2BETA, magirobot programmato dal professor Bridge")

@bot.message_handler(commands=["vivalon"])
def city(message):
    try:
        chat_id = message.chat.id
        bot.send_photo(chat_id, photo=open("images/vivalon.jpg","rb"))
        bot.send_message(chat_id, "Questa è Vivalon, la nostra splendida città, in una foto scattata da me medesimo durante una gita in mongolfiera")
    except:
        bot.reply_to(message, error_message)

@bot.message_handler(commands=["mercato"])
def market(message):
    try:
        chat_id = message.chat.id
        bot.send_photo(chat_id, photo=open("images/mercato.jpg","rb"))
        bot.send_message(chat_id, "Questo è il mercato cittadino, se hai bisogno di fare acquisti puoi dirigerti lì.\nPer farlo puoi passare di qui\n--->tg://join?invite=AAAAAFevPSByNw5y9nkasA")
    except:
        bot.reply_to(message, error_message)
@bot.message_handler(commands={"roll", "r"})
def rollbot(message):
    try:
        command = message.text
        id_chat = message.chat.id
        to_parse = extract_arg(command) + "+0"
        result = dice.roll(to_parse.strip())
        to_send = "I dadi hanno detto " + str(result)
        bot.reply_to(message, to_send)
    except:
        bot.reply_to(message, error_message)

@bot.message_handler(commands={"help"})
def help(message):
    try:
        bot.reply_to(message, "TODO")
    except:
        bot.reply_to(message, error_message)

print("Aldeger is running")
while True:
    bot.polling()
    print("bot reboot")