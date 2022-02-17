
import telebot
import datetime
from telebot import types
from private import TOKEN

bot = telebot.TeleBot(TOKEN)

print("Started")

def getMeasurements():
    return 0, 0

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
        answer = "{}\npH: {}\nt°: {}℃\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ph, t)
        print("Response: \n{}".format(answer))
        bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)