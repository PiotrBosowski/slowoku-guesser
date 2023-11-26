"""
This module implements the interface between human-readable strings and their
integer-based representation through the CharCoder class.
"""


import numpy as np


class UnknownCharacter(Exception):
    """
    This exception is raised when .decode() meets a character that this
    instance of CharCoder has not seen before.
    """
    pass


class CharCoder:
    """
    CharCoder is a class that allows to encode a sequence of incoming strings
    without prior knowledge about the set of characters. Every time a new
    character occurs, it is mapped to a unique integer value. Moreover, the
    class also maintains the reverse mapping to enable decoding in the same
    manner.
    """
    def __init__(self):
        self.char_map = dict()
        self.char_map_inv = dict()
        self.next_code = 1

    def encode(self, word: str) -> np.ndarray:
        """
        The function takes a string (a word) and returns its numerical
        (integer-based) representation: a sequence of ints (np.ndarray).
        If the new word have some characters unmet before, the class
        gracefully creates new codes for these letters. There are also
        no restrictions regarding the length of the word.
        :param word: string-represented word to be encoded
        :return: 1-dimensional np.ndarray of letter-codes
        """
        chars = set(word)
        for char in chars:
            if char not in self.char_map:
                self.char_map[char] = self.next_code
                self.char_map_inv[self.next_code] = char
                self.next_code += 1
        return np.array(list(map(lambda c: self.char_map[c], word)),
                        dtype=np.int8)

    def decode(self, coded_word: np.ndarray):
        """
        The function decodes a given int-array-represented word back to the
        string representation. It is important to notice that, when decoding
        a word, the encoder must have seen all its characters previously
        (otherwise the UnknownCharacter error will be thrown).
        :param coded_word: np.ndarray representing a word to decode
        :return: string-based representation of the word
        """
        try:
            return ''.join(list(map(lambda ind: self.char_map_inv[ind], coded_word)))
        except KeyError:
            raise UnknownCharacter
