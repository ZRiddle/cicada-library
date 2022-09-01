"""
Get the 13 and 14 length words.

Assume that at least some of these words map to "CIRCUMFERENCE"


pg|len|idx|word
11 13  273 ᛇᛈᛋᚢᛚᚪᛈᚢᚳᛖᚠᛞᛉ
13 14  261 ᛒᚷᛞᛉᛗᛒᛉᚳᛝᚦᚣᛞᚫᛠ
16 13  0   ᛖᛞᚪᚫᛏᚩᛠᛖᛠᛉᚳᛠᛏ
25 14  58  ᛠᛁᛡᚦᛝᚾᛖᚾᚠᚩᛗᛖᚣᚪ
43 14  45  ᛏᚠᛄᚱᚹᚠᛋᚾᚹᛄᛖᛒᚢᚦ
52 13  99  ᛈᚳᛇᚢᛏᚳᛡᛇᛝᚾᚢᚻᚦ
55 13  30  ᛒᛠᚠᛉᛁᛗᚢᚳᛈᚻᛝᛚᛇ
"""

from typing import List

from cicada.gematria import Gematria
from cicada.utils import phi, FIRST_856_PRIMES, get_dist

CIRCUMFERENCE_RUNES = "ᚳᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖ"

_PAGES = [11, 13, 16, 25, 43, 52, 55, 57]
CIRCUMFERENCE_CODES = [
    "ᛇᛈᛋᚢᛚᚪᛈᚢᚳᛖᚠᛞᛉ",  # page 11
    "ᛒᚷᛞᛉᛗᛒᛉᚳᛝᚦᚣᛞᚫᛠ",  # page 13
    "ᛖᛞᚪᚫᛏᚩᛠᛖᛠᛉᚳᛠᛏ",  # page 16
    "ᛠᛁᛡᚦᛝᚾᛖᚾᚠᚩᛗᛖᚣᚪ",  # page 25
    "ᛏᚠᛄᚱᚹᚠᛋᚾᚹᛄᛖᛒᚢᚦ",  # page 43
    "ᛈᚳᛇᚢᛏᚳᛡᛇᛝᚾᚢᚻᚦ",  # page 52
    "ᛒᛠᚠᛉᛁᛗᚢᚳᛈᚻᛝᛚᛇ",  # page 55
    "ᚳᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖᛋ",  # page 57
]

CIRCUMFERENCE_IDX = Gematria.run_to_idx(CIRCUMFERENCE_RUNES)
CIRCUMFERENCE_CODES_IDX = [Gematria.run_to_idx(code[:13]) for code in CIRCUMFERENCE_CODES]
# The shift is the offset that needs to happen to map to "CIRCUMFERENCE"
# Ex: Code->Circumference = 12->5. shift = 7 OR 29-7
SHIFTS = []
for word in CIRCUMFERENCE_CODES_IDX:
    word_shift = []
    for idx, rune_idx in zip(CIRCUMFERENCE_IDX, word):
        delta = abs(idx - rune_idx)
        #word_shift.append((min(delta, 29-delta), max(delta, 29-delta)))
        word_shift.append((delta, 29 - delta))
    SHIFTS.append(word_shift)


# Get the deltas between keys
DELTAS = []
for word in SHIFTS:
    a = word[0][0]
    b = word[0][1]
    delta = []
    for shift in word[1:]:
        delta.append((
            (shift[0]-a) % 29, (shift[1]-b) % 29
        ))
        a = shift[0]
        b = shift[1]
    DELTAS.append(delta)


class CircumferenceChecker:
    A = 1


def search_match(short_pattern: List[tuple], pattern_list: List[int]):
    """This tries to find the short_pattern inside a bigger list"""
    return


if __name__ == "__main__":
    print("\nCircumference Shifts\n")
    print(f"Page |\t  C\t  I\t  R\t  C\t  U\t  M\t  F\t  E\t  R\t  E\t  N\t  C\t  E")
    print(f"-"*109)
    for page_num, shifts, deltas in zip(_PAGES, SHIFTS, DELTAS):
        output = f"{page_num}   |\t"
        for shf in shifts:
            output += f"{shf[0]:2.0f},{shf[1]:2.0f}\t"
        print(output)
        output = f" Δ   |\t "
        for delt in deltas:
            output += f"   {delt[0]:2.0f},{delt[1]:2.0f}"
        print(output)
        print()
    print()

    # prime_totients_mod29 = [phi(x) % 29 for x in FIRST_856_PRIMES]
    natural_totients_mod29 = [phi(x) % 29 for x in range(2000)]
    from pprint import pprint
    pprint(get_dist(natural_totients_mod29))


    # for shifts in SHIFTS:
    #     first_word = []
    #     second_word = []
    #     for idx in shifts:
    #         first_word.append(idx[0] % 29)
    #         second_word.append(idx[1] % 29)
    #     print(Gematria.idx_to_lat(first_word))
    #     print(Gematria.idx_to_lat(second_word))

