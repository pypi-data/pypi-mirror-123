import requests, lxml, re, time
from bs4 import BeautifulSoup
from pathlib import Path
from fake_useragent import UserAgent


def themes():
    words_path = Path(__file__).parent.resolve() / "themes.txt"
    with open(words_path, 'r') as themes:
        data = [url.replace('\n', '') for url in themes]
    return data  # list of URLS


def get_words():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    for theme in themes():
        print(f'currently parsing from {theme}')

        time.sleep(0.3)
        html = requests.get(theme, headers=headers)
        print(html.status_code)

        if html.status_code != 403:
            soup = BeautifulSoup(html.text, 'lxml')

            with open('REPLACE_THIS_TEXT.txt', 'a') as adjectives:

                theme_words = []

                for theme_word in soup.select('.wordlist-item'):
                    word = theme_word.text
                    theme_words.append(word)

                adjectives.writelines('\n'.join(theme_words))


get_words()
