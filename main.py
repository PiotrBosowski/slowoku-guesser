from tqdm import tqdm

from slowoku import Slowoku
from slowoku.data_loading import load_wordlist

# a path to the file containing a list of valid words in separate lines
# for Polish: https://sjp.pl/sl/growy/

# DICT_PATH = r"C:\Users\piotr\Desktop\sjp-20231112\slowa.txt"
DICT_PATH = r"/home/peter/media/temp-share/repositories/slowoku_project/sjp" \
            r"-20231112/slowa.txt"
WORD_LEN = 6


def best_initial_word_experiment(dictionary_path, word_length):
    wordlist = load_wordlist(dictionary_path, word_length)
    word_scores = dict.fromkeys(wordlist)
    game = Slowoku(wordlist, verbose=False)
    for word in tqdm(wordlist):
        results = []
        for i in range(10):
            game.restart()
            gain = game.bet(word)
            results.append(gain)
        word_scores[word] = sum(results) / len(results)
    return sorted(word_scores, key=word_scores.get)


if __name__ == '__main__':
    word_scores = best_initial_word_experiment(DICT_PATH, WORD_LEN)
    wordlist = load_wordlist(DICT_PATH, WORD_LEN)
    g = Slowoku(wordlist)
    g.bet('wbiata')
    dbg_stp = 5


    # smarki
    # sensei
    # lżejsi
    # odlesi