from randomit.words_randomizer import WordRandomizer


class NamesSurnames(WordRandomizer):

    def get_random_name(self, capitalize: bool = False):
        return NamesSurnames().randomize_name(capitalize=capitalize)

    def get_random_names(self, letter_starts_with: str = '', words_to_return: int = 0, capitalize: bool = False):
        return NamesSurnames().randomize_names(letter_starts_with=letter_starts_with, words_to_return=words_to_return, capitalize=capitalize)

    def get_random_surname(self, capitalize: bool = False):
        return NamesSurnames().randomize_surname(capitalize=capitalize)

    def get_random_surnames(self, letter_starts_with: str = '', words_to_return: int = 0, capitalize: bool = False):
        return NamesSurnames().randomize_surnames(letter_starts_with=letter_starts_with, words_to_return=words_to_return, capitalize=capitalize)

    def get_random_name_surname(self, capitalize: bool = False):
        return f"{NamesSurnames().randomize_name(capitalize=capitalize)} {NamesSurnames().randomize_surname(capitalize=capitalize)}"

    def get_random_names_surnames(self, names_to_return: int = 0, capitalize: bool = False):
        all_names = NamesSurnames().randomize_names(words_to_return=names_to_return, capitalize=capitalize)
        all_surnames = NamesSurnames().randomize_surnames(words_to_return=names_to_return, capitalize=capitalize)

        return [f"{name} {surname}" for name, surname in zip(all_names, all_surnames)]
