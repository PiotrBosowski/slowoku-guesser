from dataclasses import dataclass


@dataclass
class LetterRules:
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
