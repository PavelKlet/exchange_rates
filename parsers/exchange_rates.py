import aiohttp
from bs4 import BeautifulSoup


async def fetch(url: str) -> str:

    """Функция отправки запроса на сайт"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse(response: str) -> str:

    """Функция поиска нужных позиций из ответа сайта"""

    soup = BeautifulSoup(response, "html.parser")

    section = soup.find("section", class_="widget")
    div = section.find("div", class_="currency-table")
    table = div.find("table", class_="currency-table__table")

    td_divs = table.find_all("td")

    for td in td_divs:
        large_text = td.find("div", class_="currency-table__large-text")
        rate_text = td.find("div", class_="currency-table__rate__text")

        if large_text and rate_text:
            value = large_text.text.strip()
            rate = rate_text.text.strip()
            return f"{value} {rate}"


async def start_parse(url: str) -> str:

    """Функция запуска парсинга"""

    response = await fetch(url)
    return await parse(response)

