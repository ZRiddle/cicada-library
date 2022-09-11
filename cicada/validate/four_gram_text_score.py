import csv
import os
from typing import List
from dataclasses import dataclass

from cicada.gematria import Gematria
from collections import namedtuple


@dataclass
class TextScoreResult:
    phrase: str
    total_score: float
    score_per_ngram: float
    min_score_count: float
    ngram_count: int
    rejected: bool

    def __repr__(self):
        return f"[TextScoreResult]" \
               f"[{'REJECTED' if self.rejected else 'ACCEPTED'}]" \
               f" Score= {self.score_per_ngram:.4f}\t" \
               f"Invalid 4grams= {self.min_score_count}\t" \
               f"Phrase= {self.phrase}"


class FourGramTextScore(object):
    """
        FourGramTextScore can take a passed list of numbers and return the 4gram log prob score
        the 4 gram log prob scores are held in a dict four_gram_probability_runes
        four_gram_probability_runes returns two values (count, score)
        the count is the number of occurrences of teh 4gram in project Guttenburg
        the score is the log probability of that count
        The results can be cropped (cropping helps reduce noise, but may crop the correct
        answer!
        counts are cropped, a min_count can be specified, and results with less counts are scored
        as min_score.
        The scores for a phrase can also be cropped. this is achieved by comparing the total
        phrase, with a straight line defining score per n-gram + offset.
        In offline tests a linear model for  "score pre n-gram " has looked reasonable
    """

    four_gram_probabilty_runes = {}
    with open(os.path.join('data', "4GramProbabilityData.csv"), 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for k, v1, v2 in reader:
            four_gram_probabilty_runes[k] = tuple(
                [int(v1), float(v2)])  # print(  # four_gram_probabilty_runes[k])

    four_gram_probabilty_pos = {}
    for key, value in four_gram_probabilty_runes.items():
        positions = tuple(Gematria.run_to_idx(key))
        four_gram_probabilty_pos[positions] = value
        # print(four_gram_probabilty_pos[   # positions ])

    def __init__(self):
        pass

    @classmethod
    def get_4gram_log_prob_pos(cls, pos_tuple, min_counts, min_score) -> float:
        """
        get 4gram log probability score for a passed tuple of runes as normal gematria positions
        :param pos_tuple: tuple, in positions, to get log prob score
        :param min_counts: the min counts the entry must have to return real core
        :param min_score: score to return if counts i < min_counts
        :return: score
        """
        # print("get_4gram_log_prob_pos, pos_tuple = ", pos_tuple)
        # print("get_4gram_log_prob_pos, min_counts = ", min_counts)
        # print("get_4gram_log_prob_pos, min_score = ", min_score)
        ans = cls.four_gram_probabilty_pos.get(pos_tuple, [0, min_score])
        # print("ans = ", ans)
        # print("get_4gram_log_prob_pos ", ans)
        if ans[0] < min_counts:
            return min_score
        # print(" ans[0] !<  ", min_counts)
        return ans[1]

    @classmethod
    def score_runes(
            cls,
            runes: str,
            min_counts: int = 100,
            min_score: float = -10,
            min_score_per_4gram_gradient: float = -10,
            min_score_per_4gram_offset: float = 0,
    ) -> TextScoreResult:
        return cls._get_pos_phrase_log_prob_with_min_count(
            Gematria.run_to_lat(runes.replace(" ", "")),
            min_counts,
            min_score,
            min_score_per_4gram_gradient,
            min_score_per_4gram_offset,
        )

    @classmethod
    def score_latin(
            cls,
            phrase: str,
            min_counts: int = 100,
            min_score: float = -8,
            min_score_per_4gram_gradient: float = -8,
            min_score_per_4gram_offset: float = 0,
    ) -> TextScoreResult:
        return cls._get_pos_phrase_log_prob_with_min_count(
            phrase.replace(" ", ""),
            min_counts,
            min_score,
            min_score_per_4gram_gradient,
            min_score_per_4gram_offset,
        )

    @classmethod
    def _get_pos_phrase_log_prob_with_min_count(
            cls,
            phrase: str,
            min_counts: int = 100,
            min_score: float = -10,
            min_score_per_4gram_gradient: float = -10,
            min_score_per_4gram_offset: float = 0,
    ) -> TextScoreResult:
        """
            score the passed phrase, with a cut on the amount of counts
        :param phrase: phrase string in lat
        :param min_counts: min counts in data to be accepted, otherwise min_score returned
        :param min_score: min_score to return if phrase does not exist or has counts below
        :param min_score_per_4gram_gradient:
        :param min_score_per_4gram_offset:
        :return: log probability score for phrase
        """
        runes_indexes = Gematria.lat_to_idx(phrase)
        score = 0.0
        min_score_count = 0
        num_ngrams = len(runes_indexes) - 3
        for i in range(0, num_ngrams):
            new_score = cls.get_4gram_log_prob_pos(
                tuple(runes_indexes[i:i + 4]),
                min_counts,
                min_score
            )
            if new_score == min_score:
                min_score_count += 1
            score += new_score
        # is rejected
        rejected = False
        # print("score ", score)
        # print("min_score_per_4gram_gradient ", min_score_per_4gram_gradient)
        # print("min_score_per_4gram_offset ", min_score_per_4gram_offset)
        # print("num_ngrams ", num_ngrams)
        # print(
        #     "min_score_per_4gram_gradient * num_ngrams + min_score_per_4gram_offset ",
        #     min_score_per_4gram_gradient * num_ngrams + min_score_per_4gram_offset
        # )
        if score < min_score_per_4gram_gradient * num_ngrams + min_score_per_4gram_offset:
            rejected = True

        return TextScoreResult(phrase, score, score / num_ngrams, min_score_count, num_ngrams, rejected)


if __name__ == "__main__":
    from cicada.gematria import Gematria

    words = [
        "DIVINITYWITHIN",
        "CIRCUMFERENCES",
        "FIRFUMFERENCES",
        "ENLIGHTENMENTNOW",
        "PTHEIOERHDEAEXZJP",
        "HFATHEORSJTHEOTHES",
        "JUTHEATHEATIOELTHG",
        "ONEDAYIWASWALKINGTHROUGHTHEWOODS",
    ]

    for word in words:
        print(f"{FourGramTextScore.score_latin(word)}")
