from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram import F

from config_data.config import alphabetic_currency_codes
from api.exchange_rates import ConvertCurrency, CurrencyAPI


router = Router(name=__name__)


@router.message(F.text.startswith("/convert"))
async def process_user_input_rates(message: types.Message):

    """Функция процесса конвертации"""

    convert_data = message.text.split()
    if convert_data:
        try:
            convert_number = convert_data[1]
            convert_form = convert_data[2]
            convert_to = convert_data[3]
            if (convert_number.isdigit()
                    and convert_form in alphabetic_currency_codes
                    and convert_to in alphabetic_currency_codes):

                api = CurrencyAPI("https://www.cbr-xml-daily.ru/daily_json.js")
                converter = ConvertCurrency(api)

                result = await converter.convert_currency(
                    convert_form,
                    convert_to,
                    int(convert_number))

                await message.answer(result)

            else:
                await message.answer("Такого кода валюты не существует"
                                     " или неправильно"
                                     " введено число суммы"
                                     " (вводить можно только целые числа)")
        except IndexError:
            await message.answer("Ошибка ввода")
    else:
        await message.answer("Ошибка ввода")


@router.message(CommandStart())
async def process_start(message: types.Message):

    """Функции обработки команды start"""

    await message.answer('Привет! Я бот для конвертаций валют. '
                         'Введите /help для помощи по командам')


@router.message(Command("help"))
async def process_help(message: types.Message):

    """Функции обработки команды help"""

    await message.answer('Введите команду /convert с указанием суммы и валютами '
                         'конвертации, например /convert 100 USD EUR,'
                         ' что эквивалентно "конвертировать 100 долларов в евро"')


@router.message()
async def process_message(message: types.Message):

    """Функция обработки входящих сообщений"""

    messages = {
        "greetings": ["здравствуйте", "привет",
                      "доброе утро", "добрый день", "добрый вечер"],

        "goodbyes": ["пока", "до свидания",  "прощай",
                     "всего хорошего", "счастливо", "до завтра", "до встречи"]

    }

    if message.text.lower() in messages["greetings"]:
        await message.answer("Привет! Как дела?")
    elif message.text.lower() in messages["goodbyes"]:
        await message.answer("До встречи!")
    else:
        await message.answer("Введите /start для начала работы")
