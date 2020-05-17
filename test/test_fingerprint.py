# Copyright (c) 2020 Matt Struble. All Rights Reserved.
#
# Use is subject to license terms.
#
# Author: Matt Struble
# Date: Mar. 22 2020
import unittest

from sigmod_fingerprinting.fingerprint import Fingerprint


# https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf
class TestFingerprint(unittest.TestCase):

    def setUp(self):
        self.kgram_len = 5
        self.window_len = 4
        self.fingerprint = Fingerprint(kgram_len=self.kgram_len, window_len=self.window_len)

        self.example = "A do run run run, a do run run"
        self.complex_string = "Always enjoy new movie, tv, book, clothes and music recommendations. " \
                         "[Photo of cat!](https://imgur.com/) for what it's worth."


    def test_sanitize(self):
        expected = "adorunrunrunadorunrun"
        sanitized = self.fingerprint._sanitize(self.example)
        self.assertEqual(expected, sanitized)

        expected = "alwaysenjoynewmovietvbookclothesandmusicrecommendationsphotoofcatforwhatitsworth"
        sanitized = self.fingerprint._sanitize(self.complex_string)
        self.assertEqual(expected, sanitized)

    def assert_kgram_len(self, text):
        sanitized = self.fingerprint._sanitize(text)
        kgrams = self.fingerprint._gen_kgrams(sanitized)

        for kgram in kgrams:
            self.assertEqual(self.kgram_len, len(kgram))

    def test_gen_kgrams(self):
        expected = ['adoru', 'dorun', 'orunr', 'runru', 'unrun', 'nrunr', 'runru', 'unrun', 'nruna', 'runad', 'unado', 'nador', 'adoru', 'dorun', 'orunr', 'runru', 'unrun']
        sanitized = self.fingerprint._sanitize(self.example)
        kgrams = self.fingerprint._gen_kgrams(sanitized)
        self.assertEqual(expected, kgrams)

        self.assert_kgram_len(self.example)
        self.assert_kgram_len(self.complex_string)

    def assert_hashes(self, text):
        sanitized = self.fingerprint._sanitize(text)
        kgrams = self.fingerprint._gen_kgrams(sanitized)

        hashes = self.fingerprint._hash_kgrams(kgrams)

        # There should be a hash created for each kgram
        self.assertEqual(len(kgrams), len(hashes))

        # Assert that the same kgram values are hashed the same
        hashed_kgrams = {}
        for i in range(len(hashes)):
            if kgrams[i] not in hashed_kgrams.keys():
                hashed_kgrams[kgrams[i]] = hashes[i]
            else:
                self.assertEqual(hashed_kgrams[kgrams[i]], hashes[i])

        self.fingerprint = Fingerprint(kgram_len=self.kgram_len, window_len=self.window_len)

        # rerun the hashing and assert values stayed the same
        hashes = self.fingerprint._hash_kgrams(kgrams)
        self.assertEqual(len(kgrams), len(hashes))
        for i in range(len(hashes)):
            self.assertEqual(hashed_kgrams[kgrams[i]], hashes[i])

    def test_hash_kgrams(self):
        self.assert_hashes(self.example)
        self.assert_hashes(self.complex_string)

    def assert_fingerprints(self, text):
        sanitized = self.fingerprint._sanitize(text)
        kgrams = self.fingerprint._gen_kgrams(sanitized)
        hashes = self.fingerprint._hash_kgrams(kgrams)
        fingerprints = self.fingerprint._gen_fingerprints(hashes)

        # should be generating less fingerprints than hashes
        self.assertLess(len(fingerprints), len(hashes))

        # assert hashes line up
        for print in fingerprints:
            hash, pos = print
            self.assertEqual(hashes[pos], hash)

        # Assert that the space between fingerprints is within the window length
        prev_pos = 0
        for print in fingerprints:
            pos = print[1]
            self.assertLessEqual(pos - prev_pos, self.window_len)
            prev_pos = pos

        # Assert that no duplicate fingerprints
        prev_prints = {}
        for print in fingerprints:
            hash, pos = print
            if hash not in prev_prints.keys():
                prev_prints[hash] = [pos]
            else:
                self.assertNotIn(pos, prev_prints[hash])
                prev_prints[hash].append(pos)

        # Assert that same finger prints are always generated
        prev_prints = fingerprints

        self.fingerprint = Fingerprint(kgram_len=self.kgram_len, window_len=self.window_len)
        fingerprints = self.fingerprint._gen_fingerprints(hashes)

        self.assertEqual(len(prev_prints), len(fingerprints))

        for i in range(len(fingerprints)):
            self.assertEqual(prev_prints[i][0], fingerprints[i][0])
            self.assertEqual(prev_prints[i][1], fingerprints[i][1])


    def test_gen_fingerprints(self):
        self.assert_fingerprints(self.example)
        self.assert_fingerprints(self.complex_string)




if __name__ == '__main__':
    unittest.main()
