
from typing import List

from cicada.gematria import Gematria
from cicada.liberprimus import LiberPrimus, Cribs, ALL_RUNES
from scripts.find_string_by_length import UnsolvedSentences


def has_double(word: str) -> bool:
    for i, letter in enumerate(word[:-1]):
        if word[i] == word[i+1]:
            return True
    return False


if __name__ == "__main__":
    import sys

    try:
        print_cribs = sys.argv[1]
    except:
        print_cribs = False

    lp = UnsolvedSentences()
    letters_only = "".join(lp.sentences).replace(" ", "")

    doubles_idx = []

    for i in range(len(letters_only)-1):
        if letters_only[i] == letters_only[i+1]:
            # print(f"{i}\t{letters_only[i]}{letters_only[i+1]}")
            sent, ind = lp.get_sentence_by_letter_index(i)
            for rune in ALL_RUNES:
                sent = sent.replace(f"{rune}{rune}", f"\33[43m{rune}{rune}\33[0m").replace(f"{rune} {rune}", f"\33[43m{rune} {rune}\33[0m")
            print(sent)
            doubles_idx.append(i)

    deltas = []
    prev_idx = 0
    for i, idx in enumerate(doubles_idx):
        delta = idx - prev_idx
        deltas.append(delta)
        prev_idx = idx

    print(f"\nIdx\tDelta")
    print("----------------")
    for idx, delta in zip(doubles_idx, deltas):
        print(f"{idx:5.0f}\t{delta:3.0f}")

    if print_cribs:
        Cribs.get_cribs_with('ia|io')
