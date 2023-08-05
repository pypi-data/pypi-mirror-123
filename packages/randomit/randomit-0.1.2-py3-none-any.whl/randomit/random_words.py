from randomit.words_randomizer import WordRandomizer


class Words(WordRandomizer):

    def get_random_word(self):
        return Words().randomize_to_get_one_word()

    def get_random_words(self, words_to_return: int = 0):
        return Words().randomize_to_get_multiple_words(words_to_return=words_to_return)

    def get_random_words_that_start_with(self, letter: str, words_to_return: int = 0):
        return Words().randomize_words_that_start_with(letter=letter, words_to_return=words_to_return)
