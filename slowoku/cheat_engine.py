import numpy as np


class CheatEngine:
    letter_rules = []
    wordlist = []

    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.valid_mask = np.ones(len(wordlist), dtype=bool)

    @staticmethod
    def colored_letter_counter(guess, result, color):
        color_matching_letters = guess[result == color]
        letters, counts = np.unique(color_matching_letters, return_counts=True)
        return dict(zip(letters, counts))

    def eliminate(self, guess, result):
        g_letter_counts = self.colored_letter_counter(guess, result, color=2)
        y_letter_counts = self.colored_letter_counter(guess, result, color=1)
        b_letter_counts = self.colored_letter_counter(guess, result, color=0)
        # apply green:
        if np.any(result == 2):
            cumulative_mask = \
                np.all((guess == self.wordlist)[:, result == 2], axis=1)
            # self.wordlist = self.wordlist[green_ok_mask]
        else:
            cumulative_mask = np.ones(len(self.wordlist), dtype=bool)
        # apply yellow:
        for y_letter, y_count in y_letter_counts.items():
            threshold = y_count + (g_letter_counts[y_letter]
                                   if y_letter in g_letter_counts else 0)
            yellow_ok_mask = np.sum((self.wordlist[cumulative_mask] == y_letter),
                                    axis=1) >= threshold
            cumulative_mask[cumulative_mask] = yellow_ok_mask
            # self.wordlist = self.wordlist[yellow_ok_mask]
            # now also delete these words where y_letter is on its position:
            yellow_2nd_mask = np.all((self.wordlist[cumulative_mask] != guess)
                                     [:, result == 1], axis=1)
            # self.wordlist = self.wordlist[yellow_2nd_mask]
            cumulative_mask[cumulative_mask] = yellow_2nd_mask
        # apply black:
        for b_letter, _ in b_letter_counts.items():
            threshold = (g_letter_counts[b_letter]
                         if b_letter in g_letter_counts else 0) + \
                        (y_letter_counts[b_letter]
                         if b_letter in y_letter_counts else 0)
            black_ok_mask = np.sum((self.wordlist[cumulative_mask] == b_letter),
                                   axis=1) <= threshold
            # self.wordlist = self.wordlist[black_ok_mask]
            cumulative_mask[cumulative_mask] = black_ok_mask
        self.valid_mask = cumulative_mask
