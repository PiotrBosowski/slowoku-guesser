from tqdm import tqdm

import pandas as pd

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
    wordlist = load_wordlist(dictionary_path, word_length)[:]
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
    # word_scores = best_initial_word_experiment(DICT_PATH, WORD_LEN)
    # data = pd.DataFrame(word_scores)
    # score_list = sorted(list(word_scores.items()), key=lambda item: item[1])
    # for word, score in score_list[-25:]:
    #     print(f"{word}, score: {score:.4f}")

    wordlist = load_wordlist(DICT_PATH, word_length=9)
    game = Slowoku(wordlist)
    game.bet("rywalizuj")
    game.bet("rywalizuj")
    game.bet("rywalizuj")
    dbg_stp = 5
    # g = Slowoku(wordlist)
    # g.bet('wbiata')

    """
game.bet("rywalizuj")
rywalizuj
yy---yy-- [information gain: 11.407 | 335->27]
11.407407407407407
game.bet("milioners")
milioners
-y---gyy- [information gain: 2.000 | 27->9]
2.0
game.help()
przednicy
przegniły
prześniły
przygnieć
przygniłe
przyśnień
rdzennicy <- R shouldn't be on first position
trzebnicy
trześnicy

    """

    # smarki
    # sensei
    # lżejsi
    # odlesi