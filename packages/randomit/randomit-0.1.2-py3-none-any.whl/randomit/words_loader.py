'''
This script loads *.txt files and returns a list() of all words to
words_randomizer (WordRandomizer class) to process the randomization.
'''
from pathlib import Path

RANDOM_WORDS_FILE = Path(__file__).parent / 'words_storage' / 'random_words.txt'
NAMES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'names_list.txt'
SURNAMES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'surnames_list.txt'


class WordsLoader:
    '''
    You can use your own words by adding another function that will
    load words which will be pass to the WordsRandomizer() class.

    1. Place own file in the "words_storage" dir.
    2. Add Path to the file you want to load.

    The same return can be used. Just make sure it's clean output.

    Example:
    def load_your_words(self):
        with open(YOUR_WORDS_FILE, 'r') as your_words:
            return [your_word.replace('\n', '') for your_word in your_words]
    '''

    def load_random_words(self):
        with open(RANDOM_WORDS_FILE, 'r') as all_words:
            return [word.replace('\n', '') for word in all_words]

    def load_name_words(self):
        with open(NAMES_FILE, 'r') as all_names:
            return [word.replace('\n', '') for word in all_names]

    def load_surname_words(self):
        with open(SURNAMES_FILE, 'r') as all_surnames:
            return [word.replace('\n', '') for word in all_surnames]
