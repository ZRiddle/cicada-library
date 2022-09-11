
import re
from typing import List

from cicada.gematria import Gematria
from cicada.liberprimus import LiberPrimus, Cribs, UnsolvedLP, Rune

DOUBLET_WORD_IDX = [
    (2,0), (2,1), (3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (4,3), (5,0), (5,1), (5,2), (5,3), (5,4), (6,0), (6,1),
    (6,2), (6,3), (6,4), (7,2), (7,3), (7,4), (7,5), (7,6), (8,0), (8,1), (8,2), (8,4), (8,5), (8,6), (9,0), (9,8),
    (10,4), (10,6), (10,7), (12,2), (12,5), (12,11),
]


def _build_lookup(lat: str, rune: str):
    rune_words = Cribs.get_cribs_with(lat)
    all_lookups = {}
    for i in range(1, 15):
        words = rune_words[i]
        lookups = {k: [] for k in range(i)}
        for word in words:
            matches = [match.start() for match in re.finditer(rune, Gematria.lat_to_run(word))]
            for match_idx in matches:
                lookups[match_idx] = lookups[match_idx] + [word]

        all_lookups[i] = lookups
    return all_lookups


def build_rune11_lookup():
    all_lookups = _build_lookup('j', "ᛄ")
    # Manually zero out very unlikely words
    for i, j in [
        (4, 1), (4, 2), (5, 1), (5, 3), (5, 4),
        (6, 1), (6, 3), (7, 1), (7, 4), (7, 5),
        (8, 1), (8, 6), (8, 7), (9, 0), (9, 8),
        # (10, 4), (10, 6), (10, 7),
        # (12, 2), (12, 11),
    ]:
        all_lookups[i][j] = []
    return all_lookups


def build_rune12_lookup():
    all_lookups = _build_lookup('eo', "ᛇ")
    for i, j in [
        (2,0), (3,0), (3,1), (4,0), (4,1), (4,3), (5,0), (5,3), (5,4),
        (6,0), (6,4), (6,5), (7,0), (7,4), (7,5), (8,1), (8,2), (8,3), (8,4),
        (9,2), (9,3), (9,4), (9,5), (9,7),
        # (10,1), (10,2), (10,3), (10,4), (10,5), (10,6), (10,7), (10,8),
        (11,1), (11,2), (11,3), (11,4), (11,5), (11,6), (11,7), (11,8), (11,9),
        # (12,1), (12,2), (12,3), (12,4), (12,5), (12,7), (12,8),
        (13,3), (13,4), (14,4), (14,5),
    ]:
        all_lookups[i][j] = []
    return all_lookups


def build_rune14_lookup():
    all_lookups = _build_lookup('x', "ᛉ")
    # Manually zero out very unlikely words
    for i, j in [
        (2, 0), (2, 1), (3, 0), (3, 1),
        (4, 0), (4, 3), (5, 1), (5, 3), (5, 4),
        (6, 0), (6, 3), (7, 0), (7, 3), (7, 4), (7, 5),
        (8, 1), (8, 6), (8, 7), (9, 0), (9, 8),
        # (10, 0), (10, 7), (12, 2), (12, 11),
    ]:
        all_lookups[i][j] = []
    return all_lookups


def build_rune22_lookup():
    all_lookups = _build_lookup('oe', "ᛟ")
    for i, j in [
        (2,1), (3,0), (3,2), (4,0), (4,2), (4,3), (5,0), (5,1), (5,2), (5,4),
        (6,0), (6,4), (6,5), (7,0), (7,2), (8,0), (8,1),
        (9,0), (9,1), (9,2), (9,2), (9,8),
        (11,0), (11,1), (11,4), (11,8), (11,9),
        # (10,1), (10,2), (10,4), (10,7), (10,8), (10,9), (12,1), (12,4), (12,8), (12,9),
        (13,3), (13,4), (14,4), (14,5),
    ]:
        all_lookups[i][j] = []
    return all_lookups


def build_rune25_lookup():
    all_lookups = _build_lookup('ae', "ᚫ")
    for i, j in [
        (3,0), (4,0), (4,1), (4,2), (4,3), (5,0), (5,1), (5,4),
        (6,0), (6,1), (6,2), (6,5), (7,0), (7,1), (7,4), (7,6), (8,1), (8,4), (8,7),
        (9,0), (9,1), (9,2), (9,6), (9,8),
        (11,0), (11,1), (11,9),
        # (10,0), (10,1), (10,2), (10,3), (10,6), (10,8), (10,9), (12,8),
        (13,11), (14,0), (14,11),
    ]:
        all_lookups[i][j] = []
    return all_lookups


def build_rune27_lookup():
    all_lookups = _build_lookup('ia|io', "ᛡ")
    # Manually zero out very unlikely words
    # for i, j in [
    #     (2,1), (3,0), (3,1), (3,2), (4,0), (4,3), (5,0), (5,4), (6,0), (6,2), (6,5),
    #     (7,0), (7,6), (8,0), (8,2), (8,7), (9,0), (9,1), (9,8),
    #     (11,0), (11,1), (11,2), (11,10),
    #     # (10,1), (10,9), (12,0), (12,1), (12,2), (12,3), (12,11),
    #     (13,0), (13,1), (13,2), (13,4), (13,5), (13,12), (14,0), (14,1), (14,2),
    #     (14,3), (14,4), (14,6), (14,13)
    # ]:
    #     all_lookups[i][j] = []
    return all_lookups


def build_rune28_lookup():
    all_lookups = _build_lookup('ea', "ᛠ")
    # Manually zero out very unlikely words
    # for i, j in [
    #     (4,3), (5,4), (6,5), (7,0), (8,0), (8,2), (9,0),
    #     # (10,1), (12,2), (12,5), (12,11),
    # ]:
    #     all_lookups[i][j] = []
    return all_lookups


def get_plaintext_doublet_rate(runes: List[Rune], lookup: dict):
    count_all = count_good = 0
    for rune in runes:
        if rune.is_doublet:
            possibles = lookup[rune.word_len][rune.letter_num]
            if len(possibles) > 0:
                count_good += 1
            count_all += 1
    return count_good, count_all


def get_deltas_and_pt_hit_rate(lookup: dict, runes: List[Rune], reverse: bool = False):
    deltas: List[int] = []
    prev_doublet_idx = -1
    good_count = doublet_count = 0
    for rune in runes:
        if rune.is_doublet:
            doublet_count += 1
            letter_idx = rune.letter_num
            if reverse:
                letter_idx = rune.word_len - rune.letter_num - 1
            possibles = lookup[rune.word_len][letter_idx]
            if len(possibles) > 0:
                good_count += 1
            if prev_doublet_idx != -1:
                deltas.append(rune.rune_num - prev_doublet_idx)
            prev_doublet_idx = rune.rune_num

    return deltas, good_count, doublet_count


def get_key_idx_hit_rate_from_deltas(
    deltas: List[int],
    lookup: dict,
    runes: List[Rune],
    reversed: bool = False,
    N_DELTAS: int = 50,
    N_KEY_LEN: int = 800,
    verbose: bool = False,
):
    delta_checks: List[List[bool]] = []

    _runes = runes.copy()
    if reversed:
        _runes = _runes[::-1]

    for key_start in range(10):
        delta_subset = deltas[key_start*N_DELTAS:(key_start+1)*N_DELTAS]
        # Check all deltas against 27 runes
        for i in range(N_KEY_LEN):
            word_checks: List[bool] = []
            # Check each word and increment by delta
            for j in range(len(delta_subset)):
                word_checks.append(runes[(key_start*N_KEY_LEN)+i+sum(delta_subset[:j])].valid_match(lookup, reversed))
            delta_checks.append(word_checks)

    if verbose:
        print(f"Key Offset = {lookup_to_use}")
    max_count = 0
    for n in range(N_DELTAS):
        n_hits = len([x for x in delta_checks if sum(x) > n])
        if verbose:
            print(f"{n} ({n/N_DELTAS*100:.1f}%)\t{n_hits}")
        if n_hits > 0:
            max_count = n
    return max_count / N_DELTAS


if __name__ == "__main__":
    import sys

    try:
        print_cribs = sys.argv[1]
    except:
        print_cribs = False

    N_DELTAS = 20
    doubles_idx = []

    lookups = {
        11: build_rune11_lookup(),
        12: build_rune12_lookup(),
        14: build_rune14_lookup(),
        22: build_rune22_lookup(),
        25: build_rune25_lookup(),
        27: build_rune27_lookup(),
        28: build_rune28_lookup(),
    }

    lookup_to_use = 27

    if print_cribs:
        print("\n\nPrinting Cribs")
        for i in range(1, 15):
            for j in range(i):
                lookup_len = len(lookups[lookup_to_use][i][j])
                #if (i,j) in DOUBLET_WORD_IDX and lookup_len < 30 and lookup_len > 0:
                print(f"{i}:{j} - {len(lookups[lookup_to_use][i][j])} \t{lookups[lookup_to_use][i][j]}")

    offsets = [
        (25, 27), (25, 28), (22, 27), (12, 27), (27, 12), (14, 27), (22, 28),
        (28, 22), (11, 27), (28, 12), (12, 28), (14, 27), (11, 28), (14, 28),
        # Others
        (28, 11), (28, 14), (28, 25),
    ]

    print(f"\nOffset\t\tPT hits\t Max Key Hits")
    for off0 in lookups:# off0, off1 in offsets:
        off1 = off0
        deltas, pt_hits, total = get_deltas_and_pt_hit_rate(lookups[off0], UnsolvedLP.runes)
        key_hit_rate = get_key_idx_hit_rate_from_deltas(deltas, lookups[off1], UnsolvedLP.runes)
        print(f"({off0}, {off1})\t{pt_hits/total*100:.2f}%\t {key_hit_rate*100:.2f}%")

        # key_hit_rate = get_key_idx_hit_rate_from_deltas(deltas, lookups[off1], UnsolvedLP.runes, reversed=True)
        # print(f"({off0}, {off1})\t[REVERSE]\t{pt_hits/total*100:.2f}%\t {key_hit_rate*100:.2f}%")




    print()
    # for i in range(15):
    #     length = len([x for x in delta_checks if sum(x) >= i])
    #     print(f"{i}\t{length}")

    # offset = 38
    # for i in range(len(delta_subset)):
    #     rune = UnsolvedLP.runes[offset + sum(delta_subset[:i])]
    #     r12_possibles = rune12_lookups[rune.word_len][rune.letter_num]
    #     r22_possibles = rune22_lookups[rune.word_len][rune.letter_num]
    #     print(
    #         f"{rune.rune_num}\t{rune.word_len}:{rune.letter_num}\t{len(r22_possibles)}\t{r22_possibles}"
    #     )

    # print("\n\n")
    # deltas: List[int] = []
    # doublets = []
    # prev_doublet_idx = 0
    # count_all = count_good = 0
    # for rune in UnsolvedLP.runes:
    #     if rune.is_doublet:
    #         doublets.append(f"({rune.word_len},{rune.letter_num})")
    #         possibles = lookups[lookup_to_use][rune.word_len][rune.letter_num]
    #         if len(possibles) > 0:
    #             print(
    #                 f"({rune.word_len},{rune.letter_num})\t{len(possibles)}\t{possibles[:3]}"
    #             )
    #         if prev_doublet_idx != 0:
    #             deltas.append(rune.rune_num - prev_doublet_idx)
    #         prev_doublet_idx = rune.rune_num
    #         if len(possibles) > 0:
    #             count_good += 1
    #         count_all += 1
    #
    # print(f"\nGood % {count_good} / {count_all} = {count_good/count_all*100:.2f}%")
    # # print(sorted(set(doublets)))
    # print()