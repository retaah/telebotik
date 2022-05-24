import requests as r
import json
import os
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
            if date.day in [today.day, today.day + 1]:
                day = {
                    'date': datetime.strftime(date, '%d.%m, %H:%M'),
                    'temp': line['main']['temp'],
                    'weather': line['weather'][0]['description']
                }
                forecast.append(day)
        return forecast
    else:
        return None

print(get_weather('Washington DC'))


