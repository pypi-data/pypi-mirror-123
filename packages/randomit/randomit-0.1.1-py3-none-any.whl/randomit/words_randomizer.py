import random
from randomit.words_loader import WordsLoader


class WordRandomizer:
    '''
    if you want to use your own words text file, you need to:
    1. Change WordsLoader().load_name_words() -> WordsLoader().YOUR_LOADED_WORDS() from words_loader.py
    2.

    '''

    def randomizer(self, letter_starts_with: str = '', words_to_return: int = 0, capitalize: bool = False):
        your_words = WordsLoader().load_name_words()

        your_names_list = []

        if capitalize and words_to_return and letter_starts_with:
            for your_word in your_words:
                if your_word.startswith(letter_starts_with.lower()):
                    your_names_list.append(your_word.capitalize())

            return [your_names_list[random.randrange(0, len(your_names_list))] for _ in range(words_to_return)]

        if capitalize and words_to_return:
            for your_word in your_words:
                your_names_list.append(your_word.capitalize())

            return [your_names_list[random.randrange(0, len(your_names_list))] for _ in range(words_to_return)]

        if capitalize and letter_starts_with:
            for your_word in your_words:
                if your_word.startswith(letter_starts_with.lower()):
                    your_names_list.append(your_word.capitalize())

            return your_names_list

        if words_to_return and letter_starts_with:
            for your_word in your_words:
                if your_word.startswith(letter_starts_with.lower()):
                    your_names_list.append(your_word)

            return [your_names_list[random.randrange(0, len(your_names_list))] for _ in range(words_to_return)]

        if capitalize:
            for your_word in your_words:
                your_names_list.append(your_word.capitalize())

            return your_names_list

        elif words_to_return:
            for your_word in your_words:
                your_names_list.append(your_word)

            return [your_names_list[random.randrange(0, len(your_names_list))] for _ in range(words_to_return)]

        elif letter_starts_with:
            for your_word in your_words:
                if your_word.startswith(letter_starts_with.lower()):
                    your_names_list.append(your_word)

            return your_names_list

        else:
            for your_word in your_words:
                your_names_list.append(your_word)

            return your_names_list

    def randomize_to_get_one_word(self):
        return random.choice(WordsLoader().load_random_words())

    def randomize_to_get_multiple_words(self, words_to_return: int = 0):
        all_words = WordsLoader().load_random_words()

        if words_to_return:
            return [all_words[random.randrange(0, len(all_words))] for _ in range(words_to_return)]
        else:
            return all_words

    def randomize_words_that_start_with(self, letter: str, words_to_return: int = 0):
        all_words = WordsLoader().load_random_words()

        found_words = []

        if letter != '':
            for word in all_words:
                if word.startswith(str(letter.lower())):
                    found_words.append(word)

            if words_to_return:
                return [found_words[random.randrange(0, len(found_words))] for _ in range(words_to_return)]
            else:
                return found_words

    def randomize_name(self, capitalize: bool = False):
        all_names = WordsLoader().load_name_words()

        if capitalize:
            return random.choice([name.capitalize() for name in all_names])
        else:
            return random.choice(all_names)

    def randomize_names(self, letter_starts_with: str = '', words_to_return: int = 0, capitalize: bool = False):
        all_names = WordsLoader().load_name_words()

        names_list = []

        if capitalize and words_to_return and letter_starts_with:
            for name in all_names:
                if name.startswith(letter_starts_with.lower()):
                    names_list.append(name.capitalize())

            return [names_list[random.randrange(0, len(names_list))] for _ in range(words_to_return)]

        if capitalize and words_to_return:
            for name in all_names:
                names_list.append(name.capitalize())

            return [names_list[random.randrange(0, len(names_list))] for _ in range(words_to_return)]

        if capitalize and letter_starts_with:
            for name in all_names:
                if name.startswith(letter_starts_with.lower()):
                    names_list.append(name.capitalize())

            return names_list

        if words_to_return and letter_starts_with:
            for name in all_names:
                if name.startswith(letter_starts_with.lower()):
                    names_list.append(name)

            return [names_list[random.randrange(0, len(names_list))] for _ in range(words_to_return)]

        if capitalize:
            for name in all_names:
                names_list.append(name.capitalize())

            return names_list

        elif words_to_return:
            for name in all_names:
                names_list.append(name)

            return [names_list[random.randrange(0, len(names_list))] for _ in range(words_to_return)]

        elif letter_starts_with:
            for name in all_names:
                if name.startswith(letter_starts_with.lower()):
                    names_list.append(name)

            return names_list

        else:
            for name in all_names:
                names_list.append(name)

            return names_list

    def randomize_surname(self, capitalize: bool = False):
        all_surnames = WordsLoader().load_surname_words()

        if capitalize:
            return random.choice([name.capitalize() for name in all_surnames])
        else:
            return random.choice(all_surnames)

    def randomize_surnames(self, letter_starts_with: str = '', words_to_return: int = 0, capitalize: bool = False):
        all_surnames = WordsLoader().load_surname_words()

        names_list = []

        if capitalize and words_to_return and letter_starts_with:
            for name in all_surnames:
                if name.startswith(letter_starts_with.lower()):
                    names_list.append(name.capitalize())

            return [names_list[random.randrange(0, len(names_list))] for _ in range(words_to_return)]

        if capitalize and words_to_return:
            for name in all_surnames:
                names_list.append(name.capitalize())

            return [names_list[random.randrange(0, len(names_list))] for _ in range(words_to_return)]

        if capitalize and letter_starts_with:
            for name in all_surnames:
                if name.startswith(letter_starts_with.lower()):
                    names_list.append(name.capitalize())

            return names_list

        if words_to_return and letter_starts_with:
            for name in all_surnames:
                if name.startswith(letter_starts_with.lower()):
                    names_list.append(name)

            return [names_list[random.randrange(0, len(names_list))] for _ in range(words_to_return)]

        if capitalize:
            for name in all_surnames:
                names_list.append(name.capitalize())

            return names_list

        elif words_to_return:
            for name in all_surnames:
                names_list.append(name)

            return [names_list[random.randrange(0, len(names_list))] for _ in range(words_to_return)]

        elif letter_starts_with:
            for name in all_surnames:
                if name.startswith(letter_starts_with.lower()):
                    names_list.append(name)

            return names_list

        else:
            for name in all_surnames:
                names_list.append(name)

            return names_list
