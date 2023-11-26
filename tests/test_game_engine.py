import unittest as ut
import numpy as np

from slowoku.game_engine import Engine


class TestGameEngine(ut.TestCase):

    def test_all_green(self):
        # given
        ge = Engine()
        guess = np.array([1, 2, 3, 4, 5, 6])
        secret = np.array([1, 2, 3, 4, 5, 6])
        # when
        response = ge.get_color_hint(guess, secret)
        # then
        self.assertTrue(np.all(response == np.array([2] * 6)))

    def test_green_with_yellows(self):
        # given
        ge = Engine()
        guess = np.array([1, 2, 3, 2, 3])  # banan
        secret = np.array([4, 2, 3, 3, 2])  # wanna
        # when
        response = ge.get_color_hint(guess, secret)
        # then
        self.assertTrue(np.all(response == np.array([0, 2, 2, 1, 1])))

    def test_repeating_yellows(self):
        # given
        ge = Engine()
        guess = np.array([1, 2, 1, 2])  # banan
        secret = np.array([2, 1, 2, 1])  # wanna
        # when
        response = ge.get_color_hint(guess, secret)
        # then
        self.assertTrue(np.all(response == np.array([1, 1, 1, 1])))

    def test_yellow_count_cap(self):
        # given
        ge = Engine()
        guess = np.array([1, 2, 3, 4])  # banan
        secret = np.array([2, 1, 2, 1])  # wanna
        # when
        response = ge.get_color_hint(guess, secret)
        # then
        self.assertTrue(np.all(response == np.array([1, 1, 0, 0])))

    def test_all_grey(self):
        # given
        ge = Engine()
        guess = np.array([1, 1, 1, 1])  # banan
        secret = np.array([2, 2, 2, 2])  # wanna
        # when
        response = ge.get_color_hint(guess, secret)
        # then
        self.assertTrue(np.all(response == np.array([0, 0, 0, 0])))

    def test_human_readable(self):
        # given
        ge = Engine()
        guess = np.array([1, 2, 3, 2, 3])  # banan
        secret = np.array([4, 2, 3, 3, 2])  # wanna
        # when
        response = ge.get_color_hint(guess, secret, human_reable=True)
        # then
        self.assertEqual(response, "-ggyy")
