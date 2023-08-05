import requests, lxml, re, time
from bs4 import BeautifulSoup
from pathlib import Path
from fake_useragent import UserAgent


def scrape_surnames():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    urls = [
        'https://one-name.org/surnames_A-Z/?initial=A',
        'https://one-name.org/surnames_A-Z/?initial=B',
        'https://one-name.org/surnames_A-Z/?initial=C',
        'https://one-name.org/surnames_A-Z/?initial=D',
        'https://one-name.org/surnames_A-Z/?initial=E',
        'https://one-name.org/surnames_A-Z/?initial=F',
        'https://one-name.org/surnames_A-Z/?initial=G',
        'https://one-name.org/surnames_A-Z/?initial=H',
        'https://one-name.org/surnames_A-Z/?initial=I',
        'https://one-name.org/surnames_A-Z/?initial=J',
        'https://one-name.org/surnames_A-Z/?initial=K',
        'https://one-name.org/surnames_A-Z/?initial=L',
        'https://one-name.org/surnames_A-Z/?initial=M',
        'https://one-name.org/surnames_A-Z/?initial=N',
        'https://one-name.org/surnames_A-Z/?initial=O',
        'https://one-name.org/surnames_A-Z/?initial=P',
        'https://one-name.org/surnames_A-Z/?initial=Q',
        'https://one-name.org/surnames_A-Z/?initial=R',
        'https://one-name.org/surnames_A-Z/?initial=S',
        'https://one-name.org/surnames_A-Z/?initial=T',
        'https://one-name.org/surnames_A-Z/?initial=U',
        'https://one-name.org/surnames_A-Z/?initial=V',
        'https://one-name.org/surnames_A-Z/?initial=W',
        'https://one-name.org/surnames_A-Z/?initial=X',
        'https://one-name.org/surnames_A-Z/?initial=Y',
        'https://one-name.org/surnames_A-Z/?initial=Z',
    ]

    surnames_list = []

    with open('../words_storage/surnames_list.txt', 'w', encoding="utf-8") as surnames_file:

        for url in urls:
            print(url)
            html = requests.get(url, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')

            for surnames in soup.select('button'):
                surname = surnames.text.lower()
                if surname not in surnames_list:
                    surnames_list.append(surname)

        surnames_file.writelines('\n'.join(surnames_list))


def scrape_names():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    html = requests.get('https://www.verywellfamily.com/top-1000-baby-boy-names-2757618', headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    names_list = []

    with open('../words_storage/names_list.txt', 'w', encoding='utf-8') as names_flie:
        for names in soup.select('#mntl-sc-block_1-0-12 li'):
            name = names.text.lower()
            if name not in names_list:
                names_list.append(name)

        names_flie.writelines('\n'.join(names_list))
