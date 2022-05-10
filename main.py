import telebot
import requests as r

bot = telebot.TeleBot('5114733697:AAElaHjA30DWQFnfmCON5eMoG4RwJCyyDVU')

@bot.message_handler(commands=['start'])
def start_message(message):
    with open('assets/greeting.txt') as file:
        greeting = file.read()
    bot.send_message(message.chat.id, greeting)




bot.polling(none_stop=True, interval=0)
