from slowoku import Slowoku


# a path to the file containing a list of valid words in separate lines
# for Polish: https://sjp.pl/sl/growy/

DICT_PATH = r"C:\Users\piotr\Desktop\sjp-20231112\slowa.txt"
WORD_LEN = 6


def best_initial_word_experiment(dictionary_path, word_length):
    game = Slowoku(dictionary_path, word_length)



if __name__ == '__main__':
    game = Slowoku(DICT_PATH, WORD_LEN, cheat_mode=True)
    game.bet('polska', '-gg-yy')
    game.bet('kolano', 'gggg--')

    # game.bet('polska', '-----y')
    # game.bet('budzić', '---y-g')
    # game.bet('zjawić', 'y-yy-g')
    # game.bet('korków', '-----y', print_words=True)
    # game = Slowoku(DICT_PATH, WORD_LEN)
    # game.bet('korków')
    dbg_stp = 5