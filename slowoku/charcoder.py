import numpy as np


class CharCoder:
    char_pool: set
    char_map: dict
    char_map_inv: dict

    def __init__(self):
        self.char_pool = set()
        self.char_map = dict()
        self.char_map_inv = dict()

    def encode(self, word: str) -> np.ndarray:
        chars = set(word)
        if chars not in self.char_pool:
            self.char_pool.update(chars)
            self.__update_char_maps()
        return np.array(list(map(lambda c: self.char_map[c], word)), dtype=np.int8)

    def decode(self, word: np.ndarray):
        return ''.join(list(map(lambda ind: self.char_map_inv[ind], word)))

    def __update_char_maps(self):
        self.char_map = dict(zip(self.char_pool, range(0, len(self.char_pool))))
        self.char_map_inv = {v: k for k, v in self.char_map.items()}