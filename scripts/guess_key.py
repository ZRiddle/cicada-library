"""
Guess a key, search through the unsolved LP and
"""
from functools import partial
import itertools
import time
from dataclasses import dataclass
from typing import List

from cicada.liberprimus import UnsolvedLP, Rune
from cicada.decode_vignere import *
from cicada.utils import nth_prime, highlight_text
from cicada.validate import TextScoreResult, FourGramTextScore, Validator


@dataclass
class PossiblePlainText:
    key: str  # The key input
    pt: str  # The input guess of the words
    score: TextScoreResult
    info_str: str = ""  # extra info to print

    def __repr__(self):
        return f"{self.score.score_per_ngram:2.2f}  " \
               f"{self.score.min_score_count:2.0f}  " \
               f"{self.pt} \t" \
               f"[{self.key}]\t" \
               f"{self.info_str}"


def is_valid_configuration():
    return True


if __name__ == "__main__":
    import sys

    try:
        keys = [key.upper().replace(" ", "") for key in sys.argv[1].split(",")]
    except:
        keys = [
            # "PATIENCE", "STRUGGLE",
            "CIRCUMFERENCE", "CONSCIOUSNESS", "ENLIGHTENMENT", "INTERCONNECTEDNESS",
            "PROGRAMYOURMIND", "PROGRAMREALITY", "INSTAREMERGENCE", "DISCOVERTRUTH",
        ]

    START_RUNE_INDEX = UnsolvedLP.PAGE_54_RUNE_INDEX
    MIN_SCORE_4GRAM = -3.8
    MIN_SCORE_PHRASE_MATCH = 0.84
    MIN_SCORE_PHRASE_MATCH_HIGHLIGHT = 0.91
    PRINT_TOP_N_GUESSES = 100

    mults = [1, 2, 27, 28]  # [x for x in range(1, 29)]
    pt_fcns_inverse = [CipherFcns.un_iden, CipherFcns.un_phi, CipherFcns.un_nth_prime]
    key_fcns = [CipherFcns.iden, CipherFcns.phi, CipherFcns.nth_prime, CipherFcns.one]

    apply_mult_fcns = [CipherFcns.mul, CipherFcns.div]

    # PT offset is very likely in [12, 25, 28]
    # 12  13.48%   15.91%
    # 25  0.00%    0.36%
    # 28  79.78%   81.68%
    offsets = [
        (12, 27), (22, 27), (25, 27), (28, 25), (27, 22),
        # (25, 28), (22, 28), (28, 22), (28, 12), (12, 28), (28, 11),
    ]

    if key_fcns != [CipherFcns.one]:
        # Only add these if we're using the key fcn. otherwise the key is just the prime function
        offsets += [(25, 28), (22, 28), (28, 22), (28, 12), (12, 28), (28, 11)]
    else:
        # Override mults and check more
        mults = [x for x in range(29)]

    is_reverseds = [False]  # [True, False]
    all_solutions: List[PossibleSolution] = []

    print(f"-" * 88)
    print(f"-" * 88)
    print(f" -keys          = {keys}")
    print(f" -pt_fcns_inv   = {[fcn.__name__ for fcn in pt_fcns_inverse]}")
    print(f" -key_fcns      = {[fcn.__name__ for fcn in key_fcns]}")
    print(f" -mult_fcns     = {[fcn.__name__ for fcn in apply_mult_fcns]}")
    print(f" -pt_offsets    = {offsets}")
    print(f" -mults         = {mults}")
    print(f"-" * 88)
    print(f"-" * 88)

    count = 0
    start_time = time.time()
    for key in keys:
        key_len = len(Gematria.lat_to_run(key.replace(" ", "")))
        print()
        print(f"-" * 88)
        print(f"Cribbing for Key={key} ({key_len})")
        print(f"-" * 88)
        for i in range(START_RUNE_INDEX, len(UnsolvedLP.runes) - key_len - 1):
            runes = UnsolvedLP.runes[i:i+key_len]
            rune_fill_text = UnsolvedLP.get_string_from_runes(runes)
            runes_text = "".join([r.rune for r in runes])

            nth_prime_starts = list(set(
                [i + x for x in range(4)] +
                [runes[0].rune_num_offset_page + x for x in range(5)] +
                [UnsolvedLP.runes[START_RUNE_INDEX].rune_num_offset_page + x for x in range(5)] +
                [runes[0].rune_num_offset_seg + x for x in range(5)]
            ))

            for pt_fcn_inv, key_fcn, apply_mult_fcn, is_reversed, nth_prime_start, offset, mult in itertools.product(
                    pt_fcns_inverse, key_fcns, apply_mult_fcns, is_reverseds, nth_prime_starts, offsets, mults
            ):
                count += 1
                if count % 1000000 == 0:
                    runetime_s = time.time()-start_time
                    print(
                        f"---[Runtime = "
                        f"{int(runetime_s/3600):02d}:{int((runetime_s / 60) % 60):02d}:{int(runetime_s % 60):02d}] "
                        f"checked {count/1000000:.0f} million combos ---"
                    )

                # Define function in loop
                def mul_fcn(j, input_idx, pt_offset, prev_cipher):
                    return mult * nth_prime(j + i - nth_prime_start)

                if is_reversed:
                    guess = key[::-1]
                    prev_rune = UnsolvedLP.runes[i + key_len].rune_idx
                else:
                    guess = key
                    prev_rune = UnsolvedLP.runes[i - 1].rune_idx

                solver = VignereSolver(guess, runes=runes_text, ending=is_reversed)
                possible_sols = solver.decode_deltas_fast(
                    key_fcn, pt_fcn_inv, mul_fcn, apply_mult_fcn, offset[1], offset[0], prev_rune
                )
                sols_text = [rune_fill_text.format(*Gematria.gem_map(s, 3, 1)) for s in possible_sols]
                # except:
                #     print(f"Broke on {i}, {guess=}, {len(runes)=}, {rune_fill_text=}, possible sols = {possible_sols}")
                #     sols_text = [rune_fill_text.format(*Gematria.gem_map(s, 3, 1)) for s in possible_sols]
                new_solutions = [
                    PossibleSolution(
                        pt_hr.upper(),
                        key,
                        runes=rune_fill_text.format(*Gematria.gem_map(sol_idxs, 3, 0)),
                        score=FourGramTextScore.score_latin(Gematria.idx_to_lat(sol_idxs)),
                        info_str=f" [{i}:{i+key_len}][rv={is_reversed},{offset},{pt_fcn_inv.__name__},"
                                 f"{key_fcn.__name__},{apply_mult_fcn.__name__},{nth_prime_start},{mult}]"
                    )
                    for pt_hr, sol_idxs in zip(sols_text, possible_sols)
                ]

                for sol in new_solutions:
                    if sol.score.score_per_ngram >= MIN_SCORE_4GRAM - (key_len - 4) * 0.19:
                        try:
                            sol.additional_score = Validator.score_phrase_runes(sol.runes)
                        except:
                            print(f"Broke on {sol}")
                            sol.additional_score = Validator.score_phrase_runes(sol.runes, verbose=True)
                        if sol.additional_score >= MIN_SCORE_PHRASE_MATCH:
                            all_solutions.append(sol)
                            if sol.additional_score >= MIN_SCORE_PHRASE_MATCH_HIGHLIGHT:
                                print(highlight_text(repr(sol)))
                            else:
                                print(sol)

    all_solutions.sort(key=lambda x: x.additional_score, reverse=True)

    print(f"-" * 88)
    print(f"-" * 88)
    print(f"Top Guesses:")
    print(f"-" * 88)
    for i in range(PRINT_TOP_N_GUESSES):
        try:
            print(all_solutions[i])
        except:
            pass
    print()

