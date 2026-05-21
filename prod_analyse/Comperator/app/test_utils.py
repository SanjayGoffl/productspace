import unittest
import sys
from unittest.mock import MagicMock

sys.modules['nltk'] = MagicMock()
sys.modules['nltk.corpus'] = MagicMock()

from utils import sample_words

class TestUtils(unittest.TestCase):
    def test_sample_words_less_than_len(self):
        words = ["apple", "banana", "cherry", "date"]
        result = sample_words(words, 2)
        self.assertEqual(len(result), 2)
        for word in result:
            self.assertIn(word, words)

    def test_sample_words_greater_than_len(self):
        words = ["apple", "banana"]
        result = sample_words(words, 5)
        self.assertEqual(len(result), 2)
        for word in result:
            self.assertIn(word, words)

    def test_sample_words_equal_to_len(self):
        words = ["apple", "banana", "cherry"]
        result = sample_words(words, 3)
        self.assertEqual(len(result), 3)
        self.assertCountEqual(result, words)

    def test_sample_words_empty_list(self):
        words = []
        result = sample_words(words, 5)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_sample_words_zero_sample_size(self):
        words = ["apple", "banana"]
        result = sample_words(words, 0)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
