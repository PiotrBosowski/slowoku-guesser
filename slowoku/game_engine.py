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
        """
        This function returns a hint about the guess given the secret word.
        The rules are as follows:
        - if the letter at position i in the guess is also at position i in the
          secret, a value of 2 ('g' - green in human readable) will be returned
          at position i.
        - if the letter at position i in the guess is present in the secret but
          at position different that i, a value of 1 ('y' - yellow) will be
          returned at the position i (exception from this rule is explained
          below).
        - if the letter at position i in the guess is not present in the secret
          at all, a value of 0 ('-' - grey) is returned at position i.

        The exception from the second rule:
          If there is one occurance of letter X in the secret, but in the guess
          there are two positions at which X occurs (both positions different
          than the one in the secret), only leftmost one will be gratified with
          1 (yellow) in the response, and the other one will remain 0 (grey).
          In the general case, if the secret contains N such letters X, then in
          the response only up to N occurances of the letter X in the guess
          will be gratified with 1.

          Moreover, if some of the occurances of the letter X in the secret
          will be gratified with the value of 2 (green - correct letter at
          correct position), then the number N, indicating the maximum number
          of 1's (yellows) for this letter X decreases by the number of green
          gratifications for this letter.

        This rule becomes reasonable given the example:
        - guess:  B A N A N A
        - secret: R A N G E R
        In this case (given the exception explained above), the correct
        response is: `-gg---`, which indicates that the latter A, N, and A are
        incorrect, so they should be replaced for some other letters next time.
        If it wasn't for this exception, the response would have become
        `-ggyyy`, which suggests that the secret actually contain three letters
        A and two letters N. That hint is very misleading. For this reason, the
        implementation takes into account the exception, just as the kurnik.pl
        one.

        :param guess: players guess (encoded)
        :param secret: secret word (encoded)
        :param human_reable: flag whether the output should be encoded or
          human-readable
        :return: hint regarding which letters are correct and which are on
          correct positions (encoded or in human readable format, depending
          on the above flag)
        """
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
