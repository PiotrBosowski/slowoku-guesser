from random import choice

import numpy as np

from slowoku.charcoder import CharCoder
from slowoku.cheat_engine import CheatEngine
from slowoku.game_engine import GameEngine


class Slowoku:
    secret_word = None
    c_engine: CheatEngine

    def __init__(self, wordlist, verbose=True):
        self.verbose = verbose
        self.char_coder = CharCoder()
        self.g_engine = GameEngine()
        self.wordlist = np.stack([self.char_coder.encode(word)
                                  for word in wordlist])
        self.restart()

    def restart(self):
        self.c_engine = CheatEngine(self.wordlist)
        self.secret_word = choice(self.wordlist)
        if self.verbose:
            print(f"Starting Słowoku with {len(self.wordlist)} words.")

    def help(self):
        for word in self.c_engine.valid_words:
            word = self.char_coder.decode(word)
            print(word)

    def bet(self, word):
        word = self.char_coder.encode(word)
        result, result_hmn = self.g_engine.get_color_hint(
            word,
            self.secret_word,
            return_human_readable=True)
        output = f"{self.char_coder.decode(word)}\n{result_hmn}"
        init_wc = len(self.c_engine.valid_words)
        self.c_engine.eliminate(word, result)
        post_wc = len(self.c_engine.valid_words)
        info_gain = (init_wc - post_wc) / post_wc
        cheat_output = (f"information gain: {info_gain:.3f}"
                        f" | {init_wc}->{post_wc}")
        if self.verbose:
            print(f"{output} [{cheat_output}]")
        return info_gain
