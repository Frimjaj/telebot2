import requests

from telebot import types

# bot = telebot.TeleBot("5494054794:AAG4jIdW1E5k4IaNIv5-LdZw9KhJR8o0-6g")
anime_query = '''
   query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''
url = 'https://graphql.anilist.co'

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Поиск Аниме":
        my_input(bot, chat_id)

def my_input(bot, chat_id):
    message = bot.send_message(chat_id, "Что ищем")
    bot.register_next_step_handler(message, anime, bot)

def shorten(description, info='anilist.co'):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        msg += f"\nОписание: {description}[Read More]({info})"
    else:
        msg += f"\nОписание: {description}"
    return msg

def anime(message, bot):
    msg = message.text
    search = msg.split(' ', 1)
    if len(search) == 1:
        bot.send_message(message.chat.id, 'Ты ввел что то не то')
        from menuBot import goto_menu
        goto_menu(bot, message.chat.id, "Главное меню")
        return
    else:
        search = search[1]
    variables = {'search': search}
    json = requests.post(url, json={
            'query': anime_query,
            'variables': variables
        }).json()
    if 'errors' in json.keys():
        bot.send_message(message.chat.id, 'Ничего не найдено')
        return
    if json:
        json = json['data']['Media']
        msg = f"{json['title']['romaji']}*(`{json['title']['native']}`)" \
              f"\nТип: {json['format']}" \
              f"\nСтатус: {json['status']}" \
              f"\nЭпизодов: {json.get('episodes', 'N/A')}" \
              f"\nПродолжительность: {json.get('duration', 'N/A')} Per Ep." \
              f"\nРейтинг: {json['averageScore']}" \
              f"\nЖанры: "
        for x in json['genres']:
            msg += f"{x}, "
        msg = msg[:-2] + '\n'
        msg += "Студия: "
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '\n'
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        anime_id = json['id']
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get('description', 'N/A').replace('<i>', '').replace(
            '</i>', '').replace('<br>', '')
        msg += shorten(description, info)
        image = json.get('bannerImage', None)
        if trailer:
            buttons = [
                types.InlineKeyboardButton("Подробнее", url=info),
                types.InlineKeyboardButton("Трейлер 🎬", url=trailer)
            ]
        else:
            buttons = [types.InlineKeyboardButton("Подробнее", url=info)]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        if image:
            try:
                bot.send_photo(message.chat.id, photo=image, caption=msg, reply_markup=keyboard)
            except:
                msg += f" [〽️]({image})"
                bot.send_message(message.chat.id, msg, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, msg, reply_markup=keyboard)
