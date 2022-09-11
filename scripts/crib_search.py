"""

"""

import time

from cicada.liberprimus import Cribs
from cicada.cribbing import REASONABLE_GUESSES, TEST_CRIB, RED_RUNE_CRIBS, CIRCUMFERENCE_CRIBS
from cicada.decode_vignere import *
from cicada.utils import nth_prime

if __name__ == "__main__":

    MIN_SCORE = -3.3
    PRINT_TOP_N_GUESSES = 400

    nth_prime_starts = [x for x in range(225, 265)] + [x for x in range(3250, 3270)]
    mults = [x for x in range(1, 29)]
    pt_fcns = [CipherFcns.iden, CipherFcns.phi, CipherFcns.nth_prime]
    key_fcns_inverse = [CipherFcns.un_iden, CipherFcns.un_phi, CipherFcns.un_nth_prime]
    apply_mult_fcns = [CipherFcns.mul, CipherFcns.div]

    # PT offset is very likely in [12, 25, 28]
    # 12  13.48%   15.91%
    # 25  0.00%    0.36%
    # 28  79.78%   81.68%
    offsets = [
        (25, 28), (12, 28), (22, 27), (28, 12), (28, 14), (28, 22),
        (12, 27), (28, 11), (12, 28),  # less likely row
    ]
    endings = [True, False]

    all_solutions: List[List[PossibleSolution]] = []

    print(f"-"*99)
    print(f"-"*99)
    print(f" -pt_fcns       = {[fcn.__name__ for fcn in pt_fcns]}")
    print(f" -key_fcns_inv  = {[fcn.__name__ for fcn in key_fcns_inverse]}")
    print(f" -pt_offsets    = {offsets}")
    print(f" -mults         = {mults}")
    print(f"-"*99)
    print(f"-"*99)
    print()

    count = errors = 0
    start_time = time.time()
    # This circumference is on the last page so it might be the easiest one to solve
    for crib in CIRCUMFERENCE_CRIBS[-1:]:
        print("-"*99)
        print(f"Cribbing {crib}")
        print("-"*99)
        crib_output = []
        for guess_raw in Cribs.get_words(13):
            for pt_fcn, key_fcn_inv, apply_mult_fcn, ending, nth_prime_start, offset, mult in itertools.product(
                    pt_fcns, key_fcns_inverse, apply_mult_fcns, endings, nth_prime_starts, offsets, mults
            ):
                count += 1
                if count % 1000000 == 0:
                    print(f"---[{(time.time()-start_time)/60:2.2f}m] checked {count/1000000:.0f} million combos ---")

                # Define function in loop
                def fcn(i, input_idx, pt_offset, prev_cipher):
                    # Must be a sequence of primes or constant
                    return mult * (nth_prime(i + nth_prime_start))

                if ending:
                    guess = guess_raw[::-1]
                    prev_rune = crib.next_rune_idx
                else:
                    guess = guess_raw
                    prev_rune = crib.prev_rune_idx
                solver = VignereSolver(guess, runes=crib.runes, ending=ending)
                try:
                    if prev_rune is not None:
                        possible_sols = solver.decode_deltas_fast(
                            pt_fcn, key_fcn_inv, fcn, apply_mult_fcn, offset[0], offset[1], prev_rune
                        )
                        sols = [Gematria.idx_to_lat(s) for s in possible_sols]
                        new_solutions = [
                            PossibleSolution(
                                key,
                                guess_raw,
                                score=FourGramTextScore.score_latin(key),
                                info_str=f" [{crib.section}][Rv={ending},{offset},{pt_fcn.__name__},"
                                         f"{key_fcn_inv.__name__},{nth_prime_start},{mult}]"
                            )
                            for key in sols
                        ]
                    else:
                        sols = solver.get_possible_solutions_with_start_idx(
                            pt_fcn, key_fcn_inv, fcn, apply_mult_fcn, offset[0], offset[1]
                        )
                        new_solutions = [
                            PossibleSolution(
                                key,
                                guess_raw,
                                score=FourGramTextScore.score_latin(key),
                                info_str=f" [{crib.section}][Rv={ending},{offset},{pt_fcn.__name__}, "
                                         f"{key_fcn_inv.__name__},{nth_prime_start},{mult}]"
                            )
                            for i, key in enumerate(sols)
                        ]
                except:
                    print(f"BROKE: {guess[::-1]}\t[{crib.section}][{ending},nth_prime(i+{nth_prime_start}),{offset},{nth_prime_start},{mult}]")
                    raise ZeroDivisionError

                for sol in new_solutions:
                    if sol.score.score_per_ngram > MIN_SCORE - (len(crib.runes)-4)*0.17:
                        print(sol)
                crib_output += new_solutions
        crib_output.sort(key=lambda x: x.score.score_per_ngram, reverse=True)
        all_solutions.append(crib_output)

    print()
    print("-"*99)
    print("-"*99)
    print("-"*99)
    print(f"Top {PRINT_TOP_N_GUESSES} Guesses:")
    print("-"*99)
    for output in all_solutions:
        print()
        for i in range(PRINT_TOP_N_GUESSES):
            try:
                print(output[i])
            except:
                pass
    print()

    # Sort solutions by score
    # all_solutions.sort(key=lambda x: x.score.score_per_ngram, reverse=True)
    # lines = []
    # for sols in all_solutions:
    #     for sol in sols[:10]:
    #         lines.append(f"{sol}\n")
    # with open("solver_output.txt", "w") as f:
    #     f.writelines(lines)
