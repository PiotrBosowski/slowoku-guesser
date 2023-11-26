from slowoku import Slowoku


# a path to the file containing a list of valid words in separate lines
# for Polish: https://sjp.pl/sl/growy/

# DICT_PATH = r"C:\Users\piotr\Desktop\sjp-20231112\slowa.txt"
DICT_PATH = r"/home/peter/media/temp-share/repositories/slowoku_project/sjp" \
            r"-20231112/slowa.txt"
WORD_LEN = 6


def best_initial_word_experiment(dictionary_path, word_length):
    game = Slowoku(dictionary_path, word_length)


if __name__ == '__main__':
    g = Slowoku(DICT_PATH, WORD_LEN)
    g.bet('wbiata')
    dbg_stp = 5


    # smarki
    # sensei
    # lżejsi
    # odlesi