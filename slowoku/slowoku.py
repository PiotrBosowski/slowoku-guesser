from random import choice

import numpy as np

from slowoku.charcoder import CharCoder
from slowoku.cheat_engine import CheatEngine
from slowoku.game_engine import GameEngine


class Slowoku:
    secret_word = None

    def __init__(self, dictionary_path, word_length):
        self.dictionary_path = dictionary_path
        self.word_length = word_length
        self.char_coder = CharCoder()
        self.all_words = self.load_wordlist(dictionary_path, word_length)
        self.g_engine = GameEngine()
        self.c_engine = CheatEngine(self.all_words)
        # self.secret_word = choice(self.all_words)
        self.secret_word = self.char_coder.encode('dolesi')
        print(f"Starting Słowoku with {len(self.all_words)} words.")

    def load_wordlist(self, dict_path, word_length):
        wordlist = []
        with open(dict_path, encoding='utf-8') as file:
            for line in file:
                word = line.strip()
                if len(word) == word_length:
                    wordlist.append(self.char_coder.encode(word))
        return np.stack(wordlist)

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
        cheat_output = (f"info. gain: {(init_wc - post_wc) / post_wc:.3f}"
                        f" | {init_wc}->{post_wc}")
        print(f"{output} [{cheat_output}]")
