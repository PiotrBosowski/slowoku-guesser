import numpy as np


class CheatEngine:
    letter_rules = []
    wordlist = []

    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.val_mask = np.ones(len(wordlist), dtype=bool)

    @staticmethod
    def count_letter_occurrs(guess, result, color):
        color_matching_letters = guess[result == color]
        letters, counts = np.unique(color_matching_letters, return_counts=True)
        return dict(zip(letters, counts))

    def apply_green(self, guess, result):
        """
        Filters out all words that differs on green positions.
        :param guess:
        :param result:
        :return:
        """
        green_mask = \
            np.all((guess == self.wordlist[self.val_mask])[:, result == 2],
                   axis=1)
        self.val_mask[self.val_mask] = green_mask

    def apply_yellow(self, guess, result, g_occurrs, y_occurrs):
        # delete words where y_letter is on the same position:
        yellow_repeated_mask = np.all((self.wordlist[self.val_mask] != guess)
                                      [:, result == 1], axis=1)
        self.val_mask[self.val_mask] = yellow_repeated_mask
        for y_letter, y_count in y_occurrs.items():
            # calculate a lower bound of the given letter occurrence count
            threshold = y_count + (g_occurrs[y_letter]
                                   if y_letter in g_occurrs else 0)
            yellow_ok_mask = np.sum(
                (self.wordlist[self.val_mask] == y_letter),
                axis=1) >= threshold
            self.val_mask[self.val_mask] = yellow_ok_mask

    def apply_black(self, guess, result, g_occurrs, y_occurrs, b_occurrs):
        # delete words where b_letter is on the same position:
        black_repeated_mask = np.all((self.wordlist[self.val_mask] != guess)
                                     [:, result == 0], axis=1)
        self.val_mask[self.val_mask] = black_repeated_mask
        for b_letter, _ in b_occurrs.items():
            # count an upper bound of the letter occurrence count
            threshold = (g_occurrs[b_letter]
                         if b_letter in g_occurrs else 0) + \
                        (y_occurrs[b_letter]
                         if b_letter in y_occurrs else 0)
            black_ok_mask = np.sum((self.wordlist[self.val_mask] == b_letter),
                                   axis=1) <= threshold
            # self.wordlist = self.wordlist[black_ok_mask]
            self.val_mask[self.val_mask] = black_ok_mask
        return self.val_mask

    def eliminate(self, guess, result):
        # apply green:
        g_occurrs = self.count_letter_occurrs(guess, result, color=2)
        if g_occurrs:
            self.apply_green(guess, result)
        # apply yellow:
        y_occurrs = self.count_letter_occurrs(guess, result, color=1)
        self.apply_yellow(guess, result, g_occurrs, y_occurrs)
        # apply black:
        b_occurrs = self.count_letter_occurrs(guess, result, color=0)
        self.apply_black(guess, result, g_occurrs, y_occurrs, b_occurrs)
