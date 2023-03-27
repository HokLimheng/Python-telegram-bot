from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# initialize telegram bot
update = Updater(
    token="5616684519:AAF6CpH3ESy58bED-39a2KTR05PGrgeZvVQ", use_context=True)

# declear delivery man!
dispatcher = update.dispatcher

# telegram command


def start(update, context):
    greet = '''Thank for trying out CS111 Covid Bot
to get covid number by country, simply tpye the name of the country'''

    context.bot.send_chat_action(chat_id=update.effective_message.chat_id,
                                 action="typing")

    context.bot.send_message(chat_id=update.effective_chat.id, text=greet)


def handle_message(update, context):
    # update parameter is value recieve from telegram bot,
    # # context is action send back to telegram bot.
    # print(update)

    last_name = update['message']['chat']['last_name']

    text = str(update.message.text).lower()

    import requests

    endpoint = f'https://api.covid19api.com/summary'

    r = requests.get(endpoint).json()

    for i in range(len(r['Countries'])):
        if r['Countries'][i]['Slug'] == text:
            statement = r['Countries'][i]
            Actived = statement['TotalConfirmed']-(statement['TotalDeaths']+statement['TotalRecovered'])
            result = f"Country: {statement['Country']} \nComfirmed: {statement['TotalConfirmed']} \nDeadths: {statement['TotalDeaths']} \nRecovered: {statement['TotalRecovered']} \n\
Active: {Actived} \nSource: https://covid19api.com/"
            # result = f"Country: {r['Countries'][i]['Country']} \nComfirmed: {r['Countries'][i]['TotalConfirmed']} \nDeath: {r['Countries'][i]['TotalDeaths']} \nRecovered: {r['Countries'][i]['TotalRecovered']}"
            break
        else:
            result = f"Sorry {last_name}, we don't have the information of this country."



    context.bot.send_chat_action(chat_id=update.effective_message.chat_id,
                                 action="typing")

    # send response back to telegram user
    context.bot.send_message(   
        chat_id=update.effective_message.chat_id, text=f"{result}" )


# # instruction for telegram bot to start the thread
# # command section
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# response section
handle_message = MessageHandler(Filters.text, handle_message)
dispatcher.add_handler(handle_message)


# # start telegram bot
update.start_polling()

# # waiting to exit
update.idle()

