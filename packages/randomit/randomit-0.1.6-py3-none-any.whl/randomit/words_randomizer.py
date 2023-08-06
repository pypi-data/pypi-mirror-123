import random
from pathlib import Path

RANDOM_WORDS_FILE = Path(__file__).parent / 'words_storage' / 'random_words.txt'
NAMES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'names_list.txt'
SURNAMES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'surnames_list.txt'
COUNTRIES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'countries_list.txt'
CITIES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'cities_list.txt'
ADDRESS_LIST = Path(__file__).parent.resolve() / 'words_storage' / 'addresses_list.txt'


class Words:

    def __init__(self,
                 file=None,
                 theme: str = 'random words' or 'names' or 'surnames' or 'cities' or 'countries' or 'address'
                 ):
        self.theme = theme.lower().strip()
        self.file = file

    def available_themes(self) -> list[str]:
        return ['random words', 'names', 'surnames', 'cities', 'countries', 'address']

    def load_words(self) -> list[str]:

        if self.file:
            with open(self.file, 'r', encoding='utf-8') as file:
                return [word.replace('\n', '') for word in file]

        if 'random' in self.theme:
            with open(RANDOM_WORDS_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif 'random words' in self.theme:
            with open(NAMES_FILE, 'r', encoding='utf-8') as all_words:
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

        elif 'address' in self.theme:
            with open(ADDRESS_LIST, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif self.theme == '':
            raise ValueError(
                "Apparently, no theme is specified. Call available_themes() function to see available themes.")

        else:
            raise ValueError(
                "No such build-in theme. Hover over a Words() object to see available themes. Or call available_themes() function.")

    def randomizer(self,
                   letter_starts_with: str = '',
                   words_to_return: int = 0,
                   capitalize: bool = False,
                   return_one_word: bool = False,
                   ) -> list[str] or str:

        words = Words(file=self.file, theme=self.theme).load_words()

        words_list = []

        if return_one_word and capitalize:
            for word in words:
                words_list.append(word.title())

            return ''.join([words_list[random.randrange(0, len(words_list))] for _ in range(1)])

        if capitalize and words_to_return and letter_starts_with:
            for word in words:
                if word.startswith(letter_starts_with.lower()):
                    words_list.append(word.title())

            return [words_list[random.randrange(0, len(words_list))] for _ in range(words_to_return)]

        if capitalize and words_to_return:
            for word in words:
                words_list.append(word.title())

            return [words_list[random.randrange(0, len(words_list))] for _ in range(words_to_return)]

        if capitalize and letter_starts_with:
            for word in words:
                if word.startswith(letter_starts_with.lower()):
                    words_list.append(word.title())

            return words_list

        if words_to_return and letter_starts_with:
            for word in words:
                if word.startswith(letter_starts_with.lower()):
                    words_list.append(word)

            return [words_list[random.randrange(0, len(words_list))] for _ in range(words_to_return)]

        if capitalize:
            for word in words:
                words_list.append(word.title())

            return words_list

        elif words_to_return:
            for word in words:
                words_list.append(word)

            return [words_list[random.randrange(0, len(words_list))] for _ in range(words_to_return)]

        elif letter_starts_with:
            for word in words:
                if word.startswith(letter_starts_with.lower()):
                    words_list.append(word)

            return words_list

        elif return_one_word:
            return random.choice(words)

        else:
            for word in words:
                words_list.append(word)

            return words_list
