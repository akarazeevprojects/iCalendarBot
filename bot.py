from telegram import InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from icalendar import Calendar, Event, vText
import logging
import typing
import json


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

actions = {
    'NEXT':   '1',
    'PREV':   '2',
    'SEARCH': '3'
}

# ------------------ #
#  Here goes bot's   #
#  Implementation    #
# ------------------ #


def get_token():
    path = 'token.json'
    with open(path, 'r') as jsn:
        data = json.load(jsn)
    return data['token']

# keyboard = [[InlineKeyboardButton("Previous", callback_data=actions['PREV']),
#              InlineKeyboardButton("Search by keyword",  callback_data=actions['SEARCH']),
#              InlineKeyboardButton("Next", callback_data=actions['NEXT'])]]


def start(bot, update):
    update.message.reply_text('Start working...')

    help_text = list()
    help_text.append("Please, enter the event's info in the following format:")
    help_text.append("-----")
    help_text.append("<title>")
    help_text.append("<description>")
    help_text.append("<url>")
    help_text.append("<location>")
    help_text.append("<YYYY><MM><DD>T<hh><mm><ss> - start date")
    help_text.append("<YYYY><MM><DD>T<hh><mm><ss> - end date")
    help_text.append("-----")
    help_text = '\n'.join(help_text)
    update.message.reply_text(help_text)


# def button(bot, update):
#     global iterator
#
#     query = update.callback_query
#
#     # NEXT case
#     if query.data == actions['NEXT']:
#         bot.edit_message_text(text="Ok, next",
#                               chat_id=query.message.chat_id,
#                               message_id=query.message.message_id)
#         bot.send_message(query.message.chat_id, '--------------------------')
#         bot.send_message(query.message.chat_id, 'The End. Now send me another keyword')
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         query.message.reply_text('Choose something', reply_markup=reply_markup)
#
#     # SEARCH case
#     elif query.data == actions['SEARCH']:
#         bot.edit_message_text(text="Ok, send me a keyword",
#                               chat_id=query.message.chat_id,
#                               message_id=query.message.message_id)
#
#     # PREV case
#     elif query.data == actions['PREV']:
#         bot.edit_message_text(text="Ok, prev",
#                               chat_id=query.message.chat_id,
#                               message_id=query.message.message_id)
#
#         bot.send_message(query.message.chat_id, 'Move Next please')
#
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         query.message.reply_text('Choose something', reply_markup=reply_markup)


def send_doc(update):
    # chat_id = str(update.message.chat_id)
    #
    # update.message.reply_text('Title: "{}"'.format(doc['title']))
    #
    # with open(wcloud_path, 'rb') as f:
    #     update.message.reply_photo(photo=f)
    pass


def rules_fun(bot, update):
    query = update.message.text
    title, description, url, location, date_start, date_end = query.split('\n')

    event = Event()
    event['summary'] = title
    event['description'] = description
    event['url'] = url
    event['location'] = vText(location)
    event['dtstart'] = date_start
    event['dtend'] = date_end

    cal = Calendar()
    cal.add_component(event)
    # print(cal)

    f = open('event.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

    with open('event.ics', 'rb') as f:
        update.message.reply_document(f)


def help_function(bot, update):
    update.message.reply_text('Help!')


def main():
    updater = Updater(get_token())
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_function))

    # on non-command messages
    dp.add_handler(MessageHandler(Filters.text, rules_fun))
    # dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("-> Hi!")
    main()
