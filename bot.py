import telebot
import database
database.start()

bot = telebot.TeleBot('1200593659:AAFMpll7K1qnrQWCF5mKHVEJK8QGJKtQjc8')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('История', 'Текущая стоимость')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Выбери нужный формат результата", reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def get_inf(message):
    if message.text == "История":
        bot.register_next_step_handler(message, get_history)
        bot.send_message(message.from_user.id, "Напишите название акции")
    elif message.text == 'Текущая стоимость':
        bot.register_next_step_handler(message, get_now)
        bot.send_message(message.from_user.id, "Напишите название акции")
    else:
        bot.send_message(message.from_user.id, "Выберите ответ из списка")


@bot.message_handler(content_types=['text'])
def get_history(message):
    database.viewhistory(message.text)
    file = open('history.txt', 'rb')
    bot.send_document(message.from_user.id, file)


def get_now(message):
    bot.send_message(message.from_user.id, database.viewnow(message.text))


bot.polling(none_stop=True, interval=0)
