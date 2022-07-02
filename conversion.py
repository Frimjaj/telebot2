import telebot
import requests
import translators as ts
bot = telebot.TeleBot("5494054794:AAG4jIdW1E5k4IaNIv5-LdZw9KhJR8o0-6g")

# query_text = 'Что-то'
# print('google:\n', ts.google(query_text))

def transfer2(message):
    response = ts.google(message.text)
    bot.send_message(message.chat.id, response)

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Переводчик":
        my_input(bot, chat_id)

def my_input(bot, chat_id):
    message = bot.send_message(chat_id, "Что переведем")
    bot.register_next_step_handler(message, transfer2)

