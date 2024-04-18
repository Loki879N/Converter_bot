from telebot import TeleBot, types
from currency_converter import CurrencyConverter
from currency_converter import RateNotFoundError
from config import BOT_TOKEN


bot = TeleBot(BOT_TOKEN)
conv = CurrencyConverter()

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_help = types.KeyboardButton(text="/help")
button_converter = types.KeyboardButton(text="/convert")
keyboard.add(button_help)
keyboard.add(button_converter)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет. Я бот конвертер. Нажми /help чтобы узнать, как со мной работать.', reply_markup=keyboard)
    
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Чтобы конвертировать одну валюту в другую, нажмите /convert, а затем введите банковские коды валют через /. Банковские коды валют вы можете найти по ссылке https://www.iban.ru/currency-codes'
                     , reply_markup=keyboard)

@bot.message_handler(commands=['convert'])
def convert_button(message):
    bot.send_message(message.chat.id, 'Введите банковские коды валют через /. Банковские коды валют вы можете найти по ссылке https://www.iban.ru/currency-codes')
    bot.register_next_step_handler(message, check_currencies)

def check_currencies(message):
    try:
        currencies = str(message.text).strip().upper().split('/')
        curryncy_fisrt = currencies[0].strip()
        curryncy_second = currencies[1].strip()
        if len(currencies) > 2:
            raise IndexError
        bot.send_message(message.chat.id, 'Введите число которое хотите конвертировать')
        bot.register_next_step_handler(message, check_number, curryncy_fisrt, curryncy_second)
    except IndexError:
        bot.send_message(message.chat.id, 'Неправильный формат ввода')
   

def check_number(message, curryncy_first, curryncy_second):
    try:
        amount = float(str(message.text).strip())
        if amount < 0:
            raise IndexError
        report = converter(curryncy_first, curryncy_second, amount)
        bot.send_message(message.chat.id, report)
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели не число')
    except IndexError:
        bot.send_message(message.chat.id, 'Вы ввели отрицательное число')
    
def converter(curryncy_first, curryncy_second, amount):
    try:
        money = conv.convert(amount, curryncy_first, curryncy_second)
        return  str(money) + " " + curryncy_second
    except RateNotFoundError:
        return "Данных пока нет."
    except ValueError:
        return "Таких валют нет"

bot.polling(none_stop=True)
