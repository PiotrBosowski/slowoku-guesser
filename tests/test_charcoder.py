import unittest as ut
import numpy as np

from slowoku.charcoder import CharCoder, UnknownCharacter


class TestCharCoder(ut.TestCase):
    def test_encode_basic(self):
        # given
        cc = CharCoder()
        str_6_uq = 'abcdef'
        # when
        cc.encode(str_6_uq)
        # then
        self.assertEqual(cc.char_map.keys(),  set(str_6_uq))

    def test_encode_repeating(self):
        # given
        cc = CharCoder()
        str_6_uq = 'abcdef'
        # when
        cc.encode(str_6_uq + str_6_uq)
        # then
        self.assertEqual(cc.char_map.keys(),  set(str_6_uq))

    def test_encode_twice(self):
        # given
        cc = CharCoder()
        str_6_uq = 'abcdef'
        # when
        cc.encode(str_6_uq)
        cc.encode(str_6_uq)
        # then
        self.assertEqual(cc.char_map.keys(), set(str_6_uq))

    def test_encode_twice_nonoverlapping(self):
        # given
        cc = CharCoder()
        str_6_uq = 'abcdef'
        str_6_uq_2 = 'ghijkl'
        # when
        cc.encode(str_6_uq)
        cc.encode(str_6_uq_2)
        # then
        self.assertEqual(cc.char_map.keys(), set(str_6_uq + str_6_uq_2))

    def test_decode(self):
        # given
        cc = CharCoder()
        str_6_uq = 'abcdef'
        # when
        coded = cc.encode(str_6_uq)
        word = cc.decode(coded)
        # then
        self.assertEqual(str_6_uq, word)

    def test_decode_distributed(self):
        # given
        cc = CharCoder()
        str_6_uq = 'abcdef'
        # when
        codes = [cc.encode(letter) for letter in str_6_uq]
        codes = np.concatenate(codes)
        word = cc.decode(codes)
        # then
        self.assertEqual(str_6_uq, word)

    def test_decode_missing_char(self):
        # given
        cc = CharCoder()
        str_6_uq = 'abcdef'
        # when
        coded = cc.encode(str_6_uq)
        # then
        self.assertRaises(UnknownCharacter,
                          cc.decode,
                          np.concatenate((coded, np.array([-256]))))

    def test_polish_sentence(self):
        # given
        cc = CharCoder()
        polish_sentence = 'Zażółć Gęślą Jaźń'
        # when
        coded = cc.encode(polish_sentence)
        # then
        self.assertEqual(polish_sentence, cc.decode(coded))
