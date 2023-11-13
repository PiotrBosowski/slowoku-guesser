from dataclasses import dataclass
from random import choice


class Slowoku:
    all_words = []
    bets = []
    letter_rules = []
    valid_words = []
    secret_word = None

    def __init__(self, dictionary_path, word_length, cheat_mode=False):
        self.word_length = word_length
        self.all_words = Slowoku.load_wordlist(dictionary_path, word_length)
        self.cheat_mode = cheat_mode
        self.reset()
        print(f"Starting with {len(self.valid_words)} words.")

    def reset(self):
        self.bets = []
        self.letter_rules = []
        self.valid_words = [word for word in self.all_words]
        self.secret_word = choice(self.valid_words) if not self.cheat_mode else None

    @staticmethod
    def load_wordlist(dict_path, word_length):
        wordlist = []
        with open(dict_path, encoding='utf-8') as file:
            for line in file:
                word = line.strip()
                if len(word) == word_length:
                    wordlist.append(word.lower())
        return wordlist

    @dataclass
    class LetterRule:
        letter_index: int
        green: str
        yellow: [str]
        grey: [str]

        def __init__(self, index, letter_results):
            self.letter_index = index
            self.green = ""
            self.yellow = set()
            self.grey = set()
            for letter, result in letter_results:
                if result == '-':
                    self.grey.add(letter)
                if result == 'y':
                    self.yellow.add(letter)
                if result == 'g':
                    self.green = letter

    def get_letter_rules(self):
        letter_stats = []
        for i in range(self.word_length):
            letter_results = [(word[i], response[i]) for word, response in self.bets]
            letter_stats.append(Slowoku.LetterRule(i, letter_results))
        return letter_stats

    @staticmethod
    def contains_but_elsewhere(letters, word, position):
        """
        Returns whether a word contains all the listed letters, but not on a position [ind].
        :param letters: letters the word has to contain
        :param word: word under testing
        :param position: position of the letter that is other than all the listed
        :return: True if the word contains all the letters, False otherwise.
        """
        if not all(letter in word for letter in letters):
            return False
        else:
            return all(word[position] != letter for letter in letters)

    @staticmethod
    def contains_exactly(letter, word, position):
        return word[position] == letter

    @staticmethod
    def not_contain(letters, word):
        return not set(letters).intersection(set(word))

    @classmethod
    def apply_letter_rule(cls, wordlist, letter_rule):
        ind = letter_rule.letter_index
        valid = wordlist
        if green := letter_rule.green:
            valid = [word for word in valid if cls.contains_exactly(green, word, ind)]
        if yellows := letter_rule.yellow:
            valid = [word for word in valid if cls.contains_but_elsewhere(yellows, word, ind)]
        if greys := letter_rule.grey:
            valid = [word for word in valid if cls.not_contain(greys, word)]
        return valid

    def bet(self, word, result=None, print_words=False):
        """
        Example:

        bets = [
        ('polka', 'g----'),
        ('piech', 'g----'),
        ('budzę', '-----'),
        ('grywa', '-----'),
        ('stąpa', '---y-'),
        """
        if not result:
            result = self.get_result(word)
        self.bets.append((word, result))
        self.letter_rules = self.get_letter_rules()
        wc_initial = len(self.valid_words)
        for let_rul in self.letter_rules:
            self.valid_words = self.apply_letter_rule(self.valid_words, let_rul)
        wc_final = len(self.valid_words)
        print(f"Information gain: {wc_initial/wc_final - 1:.2f}, [{wc_final} left]")
        if print_words:
            for vw in self.valid_words:
                print(vw)

    def get_result(self, word):
        repeating = set(self.secret_word).intersection(set(word))
        # no_occurence = set(self.secret_word).difference(set(word))
        outputs = []
        for ind, letter in enumerate(word):
            if letter in repeating:
                if letter == self.secret_word[ind]:
                    outputs.append('g')
                else:
                    outputs.append('y')
            else:
                outputs.append('-')
        return str(outputs)
