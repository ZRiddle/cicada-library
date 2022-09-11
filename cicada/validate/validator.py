
import os
import functools
import re
from typing import List

from cicada.liberprimus import Cribs
from cicada.gematria import Gematria


def _load_cribs_as_runes():
    output = {}
    for i in range(1, 15):
        output[i] = [Gematria.lat_to_run(x) for x in Cribs.get_words(i)]
    return output


class Validator(object):
    """
    Use this test when deciding if decrypted words are "real".

    There are many ways these methods could be made more sophisticated.

    Load in crib words These **MUST** be in consecutive rune length, with no gaps,
    convert cribs to forward Gematria position.

    Then,
    Compare passed word to crib words and get min number of char difference (0 means
    word is a real word).
    or
    find if passed word has <= requested number of char differences.

    These scores provide another way to cut and rank decrypted plaintext,

    The min char difference is designed to allow some wiggle room, e.g. 75% of a correct
    answer might still be worth investigating, as we know there are  potential typos,
    interrupters, and maybe other tricks.

    Tuning this wiggle room is up for experimentation.
    """

    _cribs = _load_cribs_as_runes()

    @classmethod
    def _count_char_overlap(cls, word1: str, word2: str) -> int:
        """Count the character overlap match for 2 words"""
        return sum([let1 == let2 for let1, let2 in zip(word1, word2)])

    @classmethod
    def score_word_runes(cls, word: str, verbose: bool = False) -> (int, int):
        """
        Get a word score match based on the number of overlaps.
        `*` is a wildcard

        :param word: a word, in runes as forward position
        :param verbose:
        :return:
        (or 0 for words longer than we have data for)
        """
        word_len = len(word)
        if word_len == 0:
            return 0, 0
        wildcard_count = word.count("*")
        if verbose:
            print(f"[Validator.score_word_runes] {word=}, {word_len=}, {wildcard_count=}")
        possible_matches = word_len - wildcard_count
        best_score = 0
        for crib in cls._cribs[word_len]:
            score = cls._count_char_overlap(word, crib)
            if score == possible_matches:
                return score, possible_matches
            best_score = max(best_score, score)
        return best_score, possible_matches

    @classmethod
    def score_phrase_runes(cls, phrase: str, verbose: bool = False) -> float:
        """
        Get a phrase score match based on the number of overlaps.
        `*` is a wildcard. word should be separated by spaces

        :param phrase: a word, in runes as forward position
        :param verbose:
        :return:
        (or 0 for words longer than we have data for)
        """
        score = total = 0
        if verbose:
            print(f"[Validator.score_phrase_runes] {phrase=}")
        for word in phrase.split(" "):
            _score, _total = cls.score_word_runes(word, verbose)
            score += _score
            total += _total
        return score / max(1, total)


if __name__ == "__main__":
    from cicada.gematria import Gematria

    word = "abcd"
    print(f"{word}\t{Validator.score_word_runes(Gematria.lat_to_run(word))}")
    print(f"{word}\t{Validator.score_phrase_runes(Gematria.lat_to_run(word))}")

    word = "*anann"
    print(f"{word}\t{Validator.score_word_runes(Gematria.lat_to_run(word))}")
    print(f"{word}\t{Validator.score_phrase_runes(Gematria.lat_to_run(word))}")

    word = "*anann abcd"
    print(f"{word}\t{Validator.score_phrase_runes(Gematria.lat_to_run(word))}")
