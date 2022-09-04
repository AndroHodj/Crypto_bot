import telebot
from extensions import APIException, CryptoConverter
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def echo_test(message:telebot.types.Message):
    text = ' Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту надо перевести> <количество переводимой валюты>\nУвидеть список доустпных валют /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key.capitalize(), ))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)

    except CryptoConverter as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except APIException as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base*int(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
