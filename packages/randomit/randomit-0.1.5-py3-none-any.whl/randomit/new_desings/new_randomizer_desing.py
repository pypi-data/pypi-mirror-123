import random
from pathlib import Path

RANDOM_WORDS_FILE = Path(__file__).parent / 'words_storage' / 'random_words.txt'
NAMES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'names_list.txt'
SURNAMES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'surnames_list.txt'
COUNTRIES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'countries_list.txt'
CITIES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'cities_list.txt'


class Words:

    def __init__(self, theme: str = 'random' or 'names' or 'surnames' or 'cities' or 'countries'):
        self.theme = theme.lower().strip()

    def available_themes(self) -> list[str]:
        return ['random', 'names', 'surnames', 'cities', 'countries']

    def load_words(self) -> list[str]:

        if 'random' in self.theme:
            with open(RANDOM_WORDS_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif 'random words' in self.theme:
            with open(RANDOM_WORDS_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif 'names' in self.theme:
            with open(NAMES_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif 'surnames' in self.theme:
            with open(SURNAMES_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif 'cities' in self.theme:
            with open(CITIES_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif 'countries' in self.theme:
            with open(COUNTRIES_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        else:
            raise ValueError("No such build-in theme. Hover over a Words() object to see available themes. "
                            "Or call available_themes() function.")

    def randomizer(self,
                   letter_starts_with: str = '',
                   words_to_return: int = 0,
                   capitalize: bool = False,
                   ) -> list[str]:

        words = Words(self.theme).load_words()

        your_names_list = []

        if capitalize and words_to_return and letter_starts_with:
            for your_word in words:
                if your_word.startswith(letter_starts_with.lower()):
                    your_names_list.append(your_word.capitalize())

            return [your_names_list[random.randrange(0, len(your_names_list))] for _ in range(words_to_return)]

        if capitalize and words_to_return:
            for your_word in words:
                your_names_list.append(your_word.capitalize())

            return [your_names_list[random.randrange(0, len(your_names_list))] for _ in range(words_to_return)]

        if capitalize and letter_starts_with:
            for your_word in words:
                if your_word.startswith(letter_starts_with.lower()):
                    your_names_list.append(your_word.capitalize())

            return your_names_list

        if words_to_return and letter_starts_with:
            for your_word in words:
                if your_word.startswith(letter_starts_with.lower()):
                    your_names_list.append(your_word)

            return [your_names_list[random.randrange(0, len(your_names_list))] for _ in range(words_to_return)]

        if capitalize:
            for your_word in words:
                your_names_list.append(your_word.capitalize())

            return your_names_list

        elif words_to_return:
            for your_word in words:
                your_names_list.append(your_word)

            return [your_names_list[random.randrange(0, len(your_names_list))] for _ in range(words_to_return)]

        elif letter_starts_with:
            for your_word in words:
                if your_word.startswith(letter_starts_with.lower()):
                    your_names_list.append(your_word)

            return your_names_list

        else:
            for your_word in words:
                your_names_list.append(your_word)

            return your_names_list

print(Words('lol').randomizer(words_to_return=1))