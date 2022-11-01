import unittest
from cdkkWords import Words

class Test_Words(unittest.TestCase):

    def test_random(self):
        words = Words(9)
        self.assertEqual(len(words.random_word()), 9)

    def test_contains_word(self):
        words6 = Words(6)
        self.assertTrue(words6.contains_word("PYTHON"))
        self.assertFalse(words6.contains_word("PYTHONIC"))

        words_all = Words()
        self.assertTrue(words_all.contains_word("PYTHON"))
        self.assertTrue(words_all.contains_word("PYTHONIC"))

    def test_match_pattern01(self):
        common_words = Words(8, common_words = True)
        found_words = common_words.match_pattern("^HOME[a-zA-Z]{4}$")
        self.assertEqual(len(found_words), 3)

    def test_match_pattern02(self):
        all_words = Words(6, common_words = False)
        found_words = all_words.match_pattern("^PYTH[A-Z]N$")
        self.assertEqual(len(found_words), 1)

    def test_frequency(self):
        all_words = Words()
        freq = all_words.frequency(pattern="^IGLOO$")
        self.assertEqual(freq[0], "O")

        freq = all_words.frequency(pattern="^IGLOO$", sorted_keys=False)
        self.assertEqual(freq["Q"], 0)

        freq = all_words.frequency()
        self.assertEqual(freq[0], "E")



    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()