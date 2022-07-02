import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

wikipedia.set_lang("ru")

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Поиск Wiki":
        my_input(bot, chat_id)

def my_input(bot, chat_id):
    message = bot.send_message(chat_id, "Что ищем")
    bot.register_next_step_handler(message, wiki, bot)

def wiki(message, bot):
    # msg = (
    #     update.effective_message.reply_to_message
    #     if update.effective_message.reply_to_message
    #     else update.effective_message
    # )
    res = ""
    msg = message.text
    search = message.text

    try:
        res = wikipedia.summary(search)
    except DisambiguationError as e:
        bot.send_message(message.chat.id, "Найдены страницы с устранением неоднозначности! Соответствующим образом скорректируйте свой запрос.\n<i>{}</i>".format(e,), parse_mode="HTML")
    except PageError as e:
        bot.send_message(message.chat.id, f"<code>{e}</code>", parse_mode="HTML")
    if res:
        result = f"<b>{search}</b>\n\n"
        result += f"<i>{res}</i>\n"
        result += f"""<a href="https://en.wikipedia.org/wiki/{search.replace(" ", "%20")}">Читать дальше...</a>"""
        if len(result) > 3000:
            with open("result.txt", "w") as f:
                print(result)
                f.write(f"{result}\n\nUwU OwO OmO UmU")
            with open("result.txt", "rb") as f:
                bot.send_document(message.chat.id, f, parse_mode="HTML")
                # splitted_text = util.split_string(str(f), 3000)
                # for text in splitted_text:
                #     bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, result, parse_mode="HTML", disable_web_page_preview=True,)
