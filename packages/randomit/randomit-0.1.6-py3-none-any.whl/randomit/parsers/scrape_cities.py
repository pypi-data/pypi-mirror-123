import requests, lxml
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def scrape_all_cities():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    # with open('../words_storage/countries_list.txt', 'w', encoding="utf-8") as cities_file:

    html = requests.get('https://www.worldometers.info/geography/alphabetical-list-of-countries/', headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    cities = []

    for city in soup.select('td:nth-child(2)'):
        cities.append(city.text.strip().lower())


def thing():
    with open('../words_storage/addresses_list.txt', 'w', encoding='utf-8') as write_file:
        with open('../words_storage/addresses_list.txt', 'r', encoding='utf-8') as file:

            list_=[]

            for word in file:
                list_.append(word.lower().strip())

            write_file.writelines('\n'.join(list_))

