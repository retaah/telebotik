import telebot
import requests as r


def get_rates(base):
    url_codes = 'https://api.coinbase.com/v2/currencies'
    response_code = r.get(url_codes)
    data = response_code.json()
    currencies = {}
    for cur in data['data']:
        currencies[cur['id']] = cur['name']

    return currencies


bot = telebot.TeleBot('your)token')

@bot.message_handler(commands=['start'])
def start_message(message):
    with open('assets/greeting.txt', encoding='utf8') as file:
        greeting = file.read()
    bot.send_message(message.chat.id, greeting)

@bot.message_handler(commands=['help'])
def help_message(message):
    with open('assets/help.txt', encoding='utf8') as file:
        help_text = file.read()
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(content_types=['text'])
def get_codes(message):
    codes = get_rates('')
    if message.text.startswith('/cur_code'):
        try:
            user_message = message.text.split()
            answer = user_message[1].upper() in codes.keys()
            bot.send_message(message.chat.id, codes[user_message
            [1].upper()])
        except (ValueError, TypeError, IndexError, SyntaxError
                , KeyError):
            bot.send_message(message.caht.id, 'Error')



bot.polling(none_stop=True, interval=0)
