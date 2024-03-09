from tqdm import tqdm

from slowoku import Slowoku
from slowoku.data_loading import load_wordlist

# a path to the file containing a list of valid words in separate lines
# for Polish: https://sjp.pl/sl/growy/

# DICT_PATH = r"C:\Users\piotr\Desktop\sjp-20231112\slowa.txt"
DICT_PATH = r"X:\repositories\slowoku_project\sjp-20231112\slowa.txt"
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

    # best_initial_word_experiment(DICT_PATH, WORD_LEN)
    # old implementation (dictionary copy): 1.35 items/s
    # new implementation (numpy mask reset only): 1.05 items/s !!!
    wordlist = load_wordlist(DICT_PATH, WORD_LEN)
    game = Slowoku(wordlist)
    # game.secret_word = game.wordlist[7]
    # game.bet("kreska")
    # dbg_stp = 5
    while True:
        try:
            user_input = input("Enter your bet and the result (example: polska --ggy-): ")
            word, result = user_input.split()
        except (TypeError, ValueError):
            print("The word and result must be space-separated.\n"
                  "The result must use the following encoding:\n"
                  "  '-' means that the letter is absent (usually blank/grey/black)\n"
                  "  'y' means that the letter is on the wrong position (usually yellow)\n"
                  "  'g' means that the letter is on the correct position (usually green)\n")
            continue
        game.bet(word, result)
        words_left = game.help()
        if words_left == 1:
            print("You cheated successfully, congratulations!")
