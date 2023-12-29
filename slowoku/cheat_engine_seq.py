import numpy as np


class CheatEngine:
    letter_rules = []
    valid_words = []

    def __init__(self, wordlist):
        self.valid_words = np.copy(wordlist)

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
            green_ok_mask = \
                np.all((guess == self.valid_words)[:, result == 2], axis=1)
            self.valid_words = self.valid_words[green_ok_mask]
        # apply yellow:
        for y_letter, y_count in y_letter_counts.items():
            threshold = y_count + (g_letter_counts[y_letter]
                                   if y_letter in g_letter_counts else 0)
            yellow_ok_mask = np.sum((self.valid_words == y_letter),
                                    axis=1) >= threshold
            self.valid_words = self.valid_words[yellow_ok_mask]
            # now also delete these words where y_letter is on its position:
            yellow_2nd_mask = np.all((self.valid_words != guess)
                                     [:, result == 1], axis=1)
            self.valid_words = self.valid_words[yellow_2nd_mask]
        # apply black:
        for b_letter, _ in b_letter_counts.items():
            threshold = (g_letter_counts[b_letter]
                         if b_letter in g_letter_counts else 0) + \
                        (y_letter_counts[b_letter]
                         if b_letter in y_letter_counts else 0)
            black_ok_mask = np.sum((self.valid_words == b_letter),
                                   axis=1) <= threshold
            self.valid_words = self.valid_words[black_ok_mask]
