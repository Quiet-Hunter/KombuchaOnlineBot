import subprocess
import telebot
import datetime
from telebot import types
from private import TOKEN

bot = telebot.TeleBot(TOKEN)

print("Started")

def getMeasurements():
    t = None
    pH = None
    output = subprocess.run(['/var/www/homelab/cgi-bin/get_pH.sh'], \
	stdout=subprocess.PIPE)
    output = output.stdout.decode("utf-8")
    output = output.split("\n")
    for line in output:
        if line.startswith("t"):
            t = line[2:]
        if line.startswith("pH"):
            pH = line[3:]
    return pH, t

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Check")
    markup.add(item1)
    bot.send_message(m.chat.id, 'Press "Check" to get the current measurements', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print("Message meta: \n{}".format(message.json))
    if message.text.strip() == "Check":
        (ph, t) = getMeasurements()
        answer = "{}\npH: {}\nt°: {}℃\n".format(datetime.datetime.now() \
            .strftime("%Y-%m-%d %H:%M:%S"), ph, t)
        print("Response: \n{}".format(answer))
        bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)
