import telebot
from getInfo import calculate_profit

API_TOKEN = open('TOKEN').read()
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, "Привет, я помогу тебе ощутить чувство упущенной выгоды. Приступим?\n"
                          "Пример использования:\n"
                          "IBM\n"
                          "200\n"
                          "2020-12-26")


@bot.message_handler(commands=['help'])
def send_help(message: telebot.types.Message):
    bot.reply_to(message, "Пример использования:\n"
                          "IBM\n"
                          "200\n"
                          "2020-12-26")


@bot.message_handler(func=lambda message: True)
def answer(message: telebot.types.Message):
    try:
        bot.reply_to(message, calculate_profit(message.text))
    except Exception as exp:
        print(exp)
        bot.reply_to(message, "Что то пошло не так, попробуйте составить запрос по-другому")

