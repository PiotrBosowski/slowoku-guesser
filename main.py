from dataclasses import dataclass


# a path to the file containing a list of valid words in separate lines
# for Polish: https://sjp.pl/sl/growy/
DICT_PATH = r"C:\Users\piotr\Desktop\sjp-20230709\slowa.txt"
WORD_LEN = 5


def load_wordlist(dict_path, word_length):
    wordlist = []
    with open(dict_path, encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if len(word) == word_length:
                wordlist.append(word)
    return wordlist


@dataclass
class LetterRule:
    letter_index: int
    yellow: [str]
    green: [str]
    grey: [str]

    def __init__(self, index, letter_results):
        self.letter_index = index
        self.yellow = []
        self.green = []
        self.grey = []
        for letter, result in letter_results:
            if result == '-':
                self.grey.append(letter)
            if result == 'Y':
                self.yellow.append(letter)
            if result == 'G':
                self.green.append(letter)


def get_possible():
    pass


def get_letter_rules(guesses):
    letter_stats = []
    for i in range(WORD_LEN):
        letter_results = [(word[i], response[i]) for word, response in guesses]
        letter_stats.append(LetterRule(i, letter_results))
    return letter_stats


def yellows_in_word(yellows, word):
    return any(letter in word for letter in yellows)


def apply_letter_rule(wordlist, letter_rule):
    ind = letter_rule.letter_index
    valid = wordlist
    if greens := letter_rule.green:
        valid = [word for word in valid if word[ind] in greens]
    if greys := letter_rule.grey:
        valid = [word for word in valid if word[ind] not in greys]
    if yellows := letter_rule.yellow:
        valid = [word for word in valid if yellows_in_word(yellows, word)]
    return valid


if __name__ == '__main__':
    words = load_wordlist(DICT_PATH, word_length=WORD_LEN)
    print(len(words))

    bets = [
        ('polka', '-y---'),
        ('stryj', '-----'),
        ('budzi', '---y-'),
        ('człon', '-yyy-'),
    ]

    letter_rules = get_letter_rules(bets)

    for let_rul in letter_rules:
        words = apply_letter_rule(words, let_rul)

    for w in words:
        print(w)
    print(words)



