import telebot
import requests as r

bot = telebot.TeleBot('user_token')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Hello':
        answer = 'Hello, how can i help you?'
        bot.send_message(message.from_user.id, answer)
    elif message.text == '/help':
        answer = 'Write "Hello"'
        bot.send_message(message.from_user.id, answer)
    elif message.text == '/check_github':
        response = r.get('https://github.com')
        if response.status_code == 200:
            bot.send_message(message.from_user.id, 'Accessible!')
        else:
            bot.send_message(message.from_user.id, 'Fail!')
    else:
        answer = 'I dont understand you!'
        bot.send_message(message.from_user.id, answer)



bot.polling(none_stop=True, interval=0)
