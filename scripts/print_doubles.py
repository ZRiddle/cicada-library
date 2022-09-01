
from typing import List

from cicada.gematria import Gematria
from cicada.liberprimus import LiberPrimus
from cicada.utils import FIRST_856_PRIMES


def has_double(word: str) -> bool:
    for i, letter in enumerate(word[:-1]):
        if word[i] == word[i+1]:
            return True
    return False


if __name__ == "__main__":
    text_clean = LiberPrimus.get_text_only(LiberPrimus.book).upper()

    deltas = []
    prev_idx = 0
    for i in range(1, len(text_clean)):
        if text_clean[i-1] == text_clean[i]:
            print(f"{i-1}-{i}\t{text_clean[i-1:i+1]}")
            delta = i-1 - prev_idx
            if prev_idx != 0:
                deltas.append(delta)
            prev_idx = i-1

    print(deltas)

    # # Tao Te Ching
    # tao_words = [x.lower() for x in LiberPrimus.TAO.replace("\n", " ").split(" ")]
    # tao_word_lengths = [len(word) for word in tao_words]
    #
    # tao_match_count = 0
    # for i in range(len(tao_word_lengths)):
    #     if has_double(tao_words[i]):
    #         # print(f"found a match @ {i}")
    #         # Found a match
    #         tao_words[i] = "\33[43m" + tao_words[i] + "\33[0m"
    #         tao_match_count += 1

    # print(f"\nTao Te Ching, {tao_match_count} matches")
    # print(" ".join(tao_words))
