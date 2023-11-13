from dataclasses import dataclass


# a path to the file containing a list of valid words in separate lines
# for Polish: https://sjp.pl/sl/growy/
DICT_PATH = r"C:\Users\piotr\Desktop\sjp-20231112\slowa.txt"
WORD_LEN = 5


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


def get_possible():
    pass


def get_letter_rules(guesses):
    letter_stats = []
    for i in range(WORD_LEN):
        letter_results = [(word[i], response[i]) for word, response in guesses]
        letter_stats.append(LetterRule(i, letter_results))
    return letter_stats


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


def contains_exactly(letter, word, position):
    return word[position] == letter


def not_contain(letters, word):
    return not set(letters).intersection(set(word))


def apply_letter_rule(wordlist, letter_rule):
    ind = letter_rule.letter_index
    valid = wordlist
    if green := letter_rule.green:
        valid = [word for word in valid if contains_exactly(green, word, ind)]
    if yellows := letter_rule.yellow:
        valid = [word for word in valid if contains_but_elsewhere(yellows, word, ind)]
    if greys := letter_rule.grey:
        valid = [word for word in valid if not_contain(greys, word)]

    return valid


if __name__ == '__main__':
    words = load_wordlist(DICT_PATH, word_length=WORD_LEN)

    bets = [
        ('polka', 'g----'),
        ('piech', 'g----'),
        ('budzę', '-----'),
        ('grywa', '-----'),
        ('stąpa', '---y-'),
    ]

    letter_rules = get_letter_rules(bets)

    for let_rul in letter_rules:
        words = apply_letter_rule(words, let_rul)

    for w in words:
        print(w)
    dbg_stp = 5