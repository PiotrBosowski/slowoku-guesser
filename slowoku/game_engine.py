"""
The Engine is a module that takes two words:
- input guess,
- actual secret,
and returns the actual colorful hint for the player to know, which letters
are in correct positions (green), which letters are on incorrect positions
(yellow), and which letters are incorrect (grey).

This module need to reproduce the color assignment policy used on the Kurnik
website in order to constitute a nice cheat-engine backend.

It's stateless design allows for diverse usage.
"""
import numpy as np


class Engine:
    char_dict = {0: '-',
                 1: 'y',
                 2: 'g'}

    def get_color_hint(self, word: np.ndarray, secret: np.ndarray):
        repeating = np.intersect1d(word, secret)
        # green assignments:
        greens = word == secret  # immediately give green where chars match
        # then count, how many yellow letters should still be considered:
        counting = np.array([np.count_nonzero((secret == letter) & ~greens)
                             for letter in repeating])
        yellows = np.zeros_like(greens)
        for letter, count in zip(repeating, counting):
            # take count most-left occurances of the yellow letter
            occurances = np.argwhere(word * ~greens == letter)[:count]
            yellows[occurances] = True
        output = np.zeros_like(greens) + yellows + 2 * greens
        return ''.join(self.char_dict[c] for c in output)
#
#
# if __name__ == '__main__':
#     cc = CharCoder()
#     output = Engine().get_color_hint(cc.encode('banan'), cc.encode('wanna'))
#     print(output)
