from tqdm import tqdm

import pandas as pd

from timeit import timeit

from slowoku import Slowoku
from slowoku.data_loading import load_wordlist

# a path to the file containing a list of valid words in separate lines
# for Polish: https://sjp.pl/sl/growy/

# DICT_PATH = r"C:\Users\piotr\Desktop\sjp-20231112\slowa.txt"
DICT_PATH = r"/home/peter/media/temp-share/repositories/slowoku_project/sjp" \
            r"-20231112/slowa.txt"
WORD_LEN = 6


def best_initial_word_experiment(dictionary_path,
                                 word_length,
                                 games_to_average=100):
    """
    This is a basic slowoku-based experiment, which aims to produce the best
    initial word for the game. It can be treated as a workload for benchmarks.
    """
    wordlist = load_wordlist(dictionary_path, word_length)
    word_scores = dict.fromkeys(wordlist)
    game = Slowoku(wordlist, verbose=False)
    results = {}
    for word in tqdm(wordlist):
        results[word] = []
        for i in range(games_to_average):
            game.restart()
            gain = game.bet(word)
            results[word].append(gain)
    return word_scores


if __name__ == '__main__':

    best_initial_word_experiment(DICT_PATH, WORD_LEN)
    # old implementation (dictionary copy): 1.35 items/s
    # new implementation (numpy mask reset only): 1.05 items/s !!!
    wordlist = load_wordlist(DICT_PATH, WORD_LEN)
    game = Slowoku(wordlist)
    # game.secret_word = game.wordlist[7]
    game.bet("kreska")
    dbg_stp = 5
