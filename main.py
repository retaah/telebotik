import telebot
import requests as r
from datetime import datetime


def get_weather(city):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city.capitalize(),
        'appid': '7ed3ada7ce8271744deddf2c85aa256d',
        'units': 'metric',
        'lang': 'ru'
    }
    response = r.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        today = datetime.today()
        forecast = []
        for line in data['list']:
            date = datetime.fromtimestamp(line['dt'])
            if (date.hour in [9, 15, 21]) and \
                    (date.day in [today.day, today.day + 1] or date.day == 1):
                day = {
                    'date': datetime.strftime(date, '%d.%m, %H:%M'),
                    'temp': round(line['main']['temp']),
                    'weather': line['weather'][0]['description']
                }
                forecast.append(day)
        return forecast
    else:
        return None

def get_currencies():
    url_codes = 'https://api.coinbase.com/v2/currencies'
    response_code = r.get(url_codes)
    data = response_code.json()
    currencies = {}
    for cur in data['data']:
        currencies[cur['id']] = cur['name']

    return currencies

def get_rates(base, amount, target):
    url_codes = f'https://api.coinbase.com/v2/exchange-rates?currency={base.upper()}'
    try:
        response_code = r.get(url_codes)
        data = response_code.json()
        rates = data['data']['rates']

        result = round(amount * float(rates[target.upper()]))
        return result
    except:
        return None

bot = telebot.TeleBot('5114733697:AAElaHjA30DWQFnfmCON5eMoG4RwJCyyDVU')

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
    codes = get_currencies()
    if message.text.startswith('/cur_code'):
        try:
            user_message = message.text.split()
            answer = user_message[1].upper() in codes.keys()
            bot.send_message(message.chat.id, codes[user_message
            [1].upper()])
        except (ValueError, TypeError, IndexError, SyntaxError
                , KeyError):
            bot.send_message(message.caht.id, 'Error')
    elif message.text.startswith('/exchange'):
        user_message = message.text.split()
        result = get_rates(base=user_message[2],
                           amount=float(user_message[1]),
                           target=user_message[4])
        if result is not None and result != 0.0:
            base = codes[user_message[2].upper()]
            target = codes[user_message[4].upper()]
            answer = f'{user_message[1]} {base} это {result} {target}'
            bot.send_message(message.chat.id, answer)
        else:
            bot.send_message(message.chat.id, 'ERROR')
    elif message.text.startswith('/weather'):
        user_message = message.text.split()
        forecast = get_weather(user_message[1])
        answer = ''
        try:
            for line in forecast:
                answer += f'{line["date"]} {line["weather"]}, {line["temp"]}℃\n'
        except TypeError:
            answer = 'There is no city with this name!'
        bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True, interval=0)
