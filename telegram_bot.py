from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Привет! Я бот для конвертации валют. Чтобы узнать, как я работаю, используй команду /help.')


def help(update, context):
    update.message.reply_text('Я могу выполнить следующие команды:\n'
                              '/start - начать общение с ботом\n'
                              '/help - получить список доступных команд\n'
                              '/convert <сумма> <валюта1> в <валюта2> - конвертировать сумму из одной валюты в другую')


def convert(update, context):
    text = update.message.text.split()
    if len(text) != 5:
        update.message.reply_text('Неправильный формат команды. Используйте /convert <сумма> <валюта1> в <валюта2>')
        return
    amount = float(text[1])
    from_currency = text[2].upper()
    to_currency = text[4].upper()
    try:
        conversion_rate = get_conversion_rate(from_currency, to_currency)
        converted_amount = round(amount * conversion_rate, 2)
        update.message.reply_text(f'{amount} {from_currency} = {converted_amount} {to_currency}')
    except Exception as e:
        update.message.reply_text('Что-то пошло не так. Попробуйте позже.')


def echo(update, context):
    update.message.reply_text('Привет! Я пока что могу только отвечать на команды.')


def get_conversion_rate(from_currency, to_currency):
    url = f'https://api.exchangeratesapi.io/latest?base={from_currency}&symbols={to_currency}'
    response = requests.get(url)
    data = response.json()
    return data['rates'][to_currency]


def main():
    updater = Updater("6737884647:AAFl2IbOOhKuugEmg8tgbxfoveC2wWwMrwc", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("convert", convert))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
