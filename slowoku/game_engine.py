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
    HUMAN_REPR = {0: '-',
                  1: 'y',
                  2: 'g'}

    def get_color_hint(self,
                       guess: np.ndarray,
                       secret: np.ndarray,
                       human_reable: bool = False):
        repeating = np.intersect1d(guess, secret)
        # green assignments:
        greens = guess == secret  # immediately give green where chars match
        # then count, how many yellow letters should still be considered:
        counting = np.array([np.count_nonzero((secret == letter) & ~greens)
                             for letter in repeating])
        yellows = np.zeros_like(greens)
        for letter, count in zip(repeating, counting):
            # take count most-left occurrences of the yellow letter
            occurrences = np.argwhere(guess * ~greens == letter)[:count]
            yellows[occurrences] = True
        output = np.zeros_like(greens) + yellows + 2 * greens
        return ''.join(self.HUMAN_REPR[c] for c in output) \
            if human_reable else output
