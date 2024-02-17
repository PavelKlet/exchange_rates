from decimal import Decimal, ROUND_HALF_UP

import aiohttp


async def request_data(url: str) -> dict:

    """
    Функция запроса данных от API
    :param url: строка с url API
    :return: словарь с данными в формате json
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json(content_type="application/javascript")


async def convert_currency(from_code: str, to_code: str, amount: int) -> str:
    """
    Функция конвертации валюты
    :param from_code: код валюты из которой нужно конвертировать
    :param to_code: код валюты в которую нужно конвертировать
    :param amount: сумма для конвертации
    :return: строка с данными о конвертации
    """

    data = await request_data("https://www.cbr-xml-daily.ru/daily_json.js")

    try:
        if to_code == "RUB":
            converted_amount = Decimal(
                data["Valute"][from_code]["Value"]
            ) * Decimal(amount) / Decimal(
                data["Valute"][from_code]["Nominal"]
            )
        elif from_code == "RUB":
            converted_amount = Decimal(amount) / Decimal(
                data["Valute"][to_code]["Value"]
            ) * Decimal(
                data["Valute"][to_code]["Nominal"]
            )
        else:
            from_value = Decimal(data["Valute"][from_code]["Value"]) / Decimal(
                data["Valute"][from_code]["Nominal"]
            )
            to_value = Decimal(data["Valute"][to_code]["Value"]) / Decimal(
                data["Valute"][to_code]["Nominal"]
            )
            converted_amount = Decimal(amount) / to_value * from_value

        converted_amount = converted_amount.quantize(
            Decimal("0.00"), rounding=ROUND_HALF_UP
        )

        return f"{converted_amount} {to_code} за {amount} {from_code}"
    except KeyError:
        return "Код валюты не поддерживается"
