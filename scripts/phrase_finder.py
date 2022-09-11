
from typing import List

from cicada.gematria import Gematria
from cicada.liberprimus import LiberPrimus, AlanWatts
from cicada.utils import is_list_match

from pprint import pprint


class PhraseFinder:
    def __init__(self, corpus: str):
        corpus = LiberPrimus.remove_numbers(corpus.upper().replace("\n", " "))
        self.words = [LiberPrimus.get_only_lat(x) for x in corpus.split(" ") if x]
        self.runes = [Gematria.lat_to_run(x) for x in self.words]
        self.word_lens = [len(x) for x in self.runes]

    def find_phrases(self, phrase_lens: List[int], excludes: List[str] = None, includes: List[str] = None, buffer: int = 1):
        outputs = {}
        print(f"excludes = {excludes}")
        print(f"includes = {includes}")
        for i in range(len(self.word_lens) - len(phrase_lens) + 1):
            if is_list_match(self.word_lens[i:i + len(phrase_lens)], phrase_lens):
                phrase = " ".join(self.words[i - buffer:i + buffer + len(phrase_lens)])
                if not self._has_overlap(phrase.split(" "), excludes):
                    if includes:
                        if self._has_overlap(phrase.split(" "), includes):
                            outputs[phrase] = outputs.get(phrase, 0) + 1
                    else:
                        outputs[phrase] = outputs.get(phrase, 0) + 1

        return {k: v for k, v in sorted(outputs.items(), key=lambda item: item[1], reverse=True)}

    def find_phrases_with(self, phrase_lens: List[int], includes: List[str] = None):
        outputs = {}
        for i in range(len(self.word_lens) - len(phrase_lens) + 1):
            if is_list_match(self.word_lens[i:i + len(phrase_lens)], phrase_lens):
                phrase = " ".join(self.words[i:i + len(phrase_lens)])
                if self._has_overlap(phrase.split(" "), includes):
                    outputs[phrase] = outputs.get(phrase, 0) + 1
        return {k: v for k, v in sorted(outputs.items(), key=lambda item: item[1], reverse=True)}

    def _has_overlap(self, lst1, lst2) -> bool:
        for word in lst1:
            if word in lst2:
                return True
        return False


def print_top_n(phrases: dict, top_n: int = 10):
    ct = 0
    for phrase, count in phrases.items():
        print(f"{count:3}\t{phrase}")
        ct += 1
        if ct > top_n:
            return


if __name__ == "__main__":
    import sys

    try:
        top_n = int(sys.argv[2])
    except:
        top_n = 50

    try:
        excludes = [x for x in sys.argv[3].upper().split(",") if x != '']
    except:
        excludes = [
            "CHRISTIAN", "SURVIVAL", "OTHERWISE",
            "INVOLVES", "MAGNIFYING", "STRICTLY",
            "SPECIFIC", "THEREFORE", "SOMETIME",
            "SEPARATE", "ORIENTAL", "ORDINARY",
            "TRUMPETS", "YOURSELF", "SOMEBODY",
            "JAPANESE", "AMERICAN", "BREAKFAST",
            "TOMORROW", "BUDDHIST",

            "ELSES", "WHERE", "WHICH", "COMES", "PEOPLE",
            "HUMAN", "ABOUT", "WOULD", "RIGHT", "WHATS",
            "BRAND", "WHILE", "AFTER", "WORLD", "THERES",
            "ZAZEN", "MUSIC", "ARENT", "YOURE", "QUITE",
            "POINT", "EITHER", "EVERY", "TAKES", "WHOSE",
            "DOESNT", "YOUVE", "MOMMY", "THEYLL", "COULD",
            "THOUGH",
        ]

    try:
        includes = [x for x in sys.argv[4].upper().split(",") if x != '']
    except:
        includes = []

    try:
        buffer = int(sys.argv[5])
    except:
        buffer = 0

    word_len = [int(x) for x in sys.argv[1].split(",")]

    all_texts = LiberPrimus.tao
    all_texts += " ".join(AlanWatts.body)

    finder = PhraseFinder(all_texts)
    phrases = finder.find_phrases(word_len, excludes, includes, buffer)

    print_top_n(phrases, top_n)
