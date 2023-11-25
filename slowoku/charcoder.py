import numpy as np


class CharCoder:
    # char_pool: set
    char_map: dict
    char_map_inv: dict

    def __init__(self):
        # self.char_pool = set()
        self.char_map = dict()
        self.char_map_inv = dict()
        self.next_code = 1

    def encode(self, word: str) -> np.ndarray:
        chars = set(word)
        for char in chars:
            if char not in self.char_map:
                self.char_map[char] = self.next_code
                self.char_map_inv[self.next_code] = char
                self.next_code += 1
        return np.array(list(map(lambda c: self.char_map[c], word)),
                        dtype=np.int8)

    def decode(self, word: np.ndarray):
        return ''.join(list(map(lambda ind: self.char_map_inv[ind], word)))
