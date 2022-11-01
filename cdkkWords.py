import csv
import re
from random import choice
from string import ascii_uppercase
import sys
import os

class Words:
    dir_wordlist = os.path.abspath(os.path.join(os.path.dirname(__file__), 'WordList'))

    def __init__(self, word_length=0, common_words=False):
        # word_length is the length of the word; 0 for any length
        # common_words = True to restrict to the most common 5000 words

        self._words = []
        if common_words:
            # wordlist.txt contains the most common 5000 words
            # The chosen word comes from ths list
            with open(f"{Words.dir_wordlist}\\wordlist.txt") as f:
                all_words = f.read().splitlines()

            for word in all_words:
                if word_length == 0 or (len(word) == word_length):
                    self._words.append(word.upper())
        else:
            if word_length == 0:
                lengths = list(range(3, 10))
            else:
                lengths = [word_length]

            for l in lengths:
                # wordlist#.txt contains all words with # letters (#=3-9)
                # Users can enter any word on this list
                with open(f"{Words.dir_wordlist}\\wordlist{l}.txt") as f:
                    all_words = f.read().splitlines()

                for word in all_words:
                    self._words.append(word.upper())

    def random_word(self):
        return choice(self._words).upper()

    def contains_word(self, word):
        return (word in self._words)

    def match_pattern(self, pattern):
        match_words = []
        for word in self._words:
            if re.search(pattern, word):
                match_words.append(word)
        return match_words

    def frequency(self, pattern = ".*", sorted_keys = True):
        freq = {x: 0 for x in list(ascii_uppercase)}
        match_words = self.match_pattern(pattern)
        for word in match_words:
            for letter in list(word):
                if letter in freq:
                    freq[letter] += 1

        if(sorted_keys):
            freq =  [k for k, v in sorted(freq.items(), key=lambda item: item[1], reverse = True)]

        return freq
                

#----------------------------------------

if __name__ == '__main__':
    game = Words()
    print("Done")
