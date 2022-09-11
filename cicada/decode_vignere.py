
import itertools
from dataclasses import dataclass
from typing import List, Optional

from cicada.cipher_utils import CipherFcns
from cicada.cribbing import CribConfigs, CribConfigsEnding
from cicada.gematria import Gematria
from cicada.validate import FourGramTextScore
from cicada.validate.four_gram_text_score import TextScoreResult


def identity(x: any) -> any:
    return x


def product(a: int, b: int) -> int:
    return a * b


def add(a: int, b: int) -> int:
    return a * b


@dataclass
class PossibleSolution:
    key: str  # The key generated from the method
    guess: str  # The input guess of the words
    score: TextScoreResult
    runes: str = ""
    additional_score: float = 0
    info_str: str = ""  # extra info to print

    def __repr__(self):
        return f"{self.score.score_per_ngram:2.2f}  " \
               f"{self.additional_score:.3f}  " \
               f"{self.key} \t" \
               f"[{self.guess}]\t" \
               f"{self.info_str}"


class VignereSolver:
    """
    Attempt to figure out possible KEYS given an input and output

    Assume the encryption takes the form:
    (mod1(P[i]) * mod2(K[i]) - nth_prime(i) + k) % 29

    mod1, mod2 are in [identity, nth_prime, phi, ??]

    """
    def __init__(self, solution_guess: str = "DIVINITY", runes: str = "ᛋᚻᛖᚩᚷᛗᛡᚠ ᛋᚣᛖᛝᚳ", ending: bool = False):
        self.solution_guess = solution_guess.replace(" ", "")
        self.runes = runes.replace(" ", "")
        self.ending = ending
        if ending:
            self.solution_runes = Gematria.lat_to_run(self.solution_guess[::-1])[::-1]
        else:
            self.solution_runes = Gematria.lat_to_run(self.solution_guess)

        assert len(self.solution_runes) <= len(self.runes), "Need to guess the same amount of runes"

        self.plaintxt_idx = Gematria.run_to_idx(self.solution_runes)
        self.cipher_idx = Gematria.run_to_idx(self.runes)

    def decode_deltas(
            self,
            fcn: callable,
            pt_offset: int = 0,
            pt_offset_direction: int = 1,
            prev_start: int = 0,
    ):
        """
        Some things we suspect about the encryption.
        it is of the form
        (PT[i] - 27) * (K[i] - 27) * something - C[i-1]

        """
        deltas = []
        prev_cipher = prev_start
        for i in range(len(self.plaintxt_idx)):
            answers = [
                (
                    (pt_offset_direction*(p - pt_offset) % 29) *
                    ((self.plaintxt_idx[i] - pt_offset) % 29) *
                    fcn(i, self.plaintxt_idx[i], p, pt_offset, prev_cipher) - prev_cipher) % 29
                for p in range(29)
            ]
            try:
                deltas.append(answers.index(self.cipher_idx[i]))
            except:
                return deltas, False
            prev_cipher = deltas[-1]
        return deltas, True

    def _expand_solutions(self, solutions: List[List[int]]) -> List[List[int]]:
        """
        Takes a list of ints and expands it to all possible combos
        > Ex:
            In:  [[1, 2] , [3], [4]]
            Out: [[1, 3, 4], [2, 3, 4]]
        """
        outputs = []
        for combo in itertools.product(*solutions):
            outputs.append(list(combo))
        return outputs

    def decode_deltas_fast(
            self,
            pt_fcn: callable,
            key_fcn_inverse: callable,
            fcn: callable,
            apply_mult_fcn: callable,
            pt_offset: int = 0,
            key_offset: int = 0,
            prev_cipher: int = 0,
            verbose: bool = False,
    ) -> List[List[int]]:
        """
        Solution:
            K[i] = f_k_inv(C[i] + C[i-1]) / [f_pt(P[i] - pt_offset) * fcn()] + key_offset
        """
        outputs = []
        for i in range(len(self.plaintxt_idx)):
            possible_keys = self._compute_next_key(
                i, pt_fcn, key_fcn_inverse, fcn, apply_mult_fcn, pt_offset, key_offset, prev_cipher, verbose
            )
            if len(possible_keys) == 0:
                # There's no possible key to generate the plaintext
                return []
            outputs.append(possible_keys)
            prev_cipher = self.cipher_idx[i]

        return self._expand_solutions(outputs)

    def _compute_next_key(
            self,
            i: int,
            pt_fcn: callable,
            key_fcn_inverse: callable,
            fcn: callable,
            apply_mult_fcn: callable,
            pt_offset: int = 0,
            key_offset: int = 0,
            prev_cipher: int = 0,
            verbose: bool = False
    ):
        denom = apply_mult_fcn(
            pt_fcn(self.plaintxt_idx[i] - pt_offset),
            fcn(i, self.plaintxt_idx[i], pt_offset, prev_cipher)
        )
        val = CipherFcns.div(self.cipher_idx[i] - prev_cipher, denom)
        # This List can be length 0, 1, 2, or 3. Need to handle all of them
        inverse_output = [CipherFcns.add(inv_out, key_offset) for inv_out in key_fcn_inverse(val)]
        if verbose:
            print(f"  i={i}")
            print(f"    denom ({self.plaintxt_idx[i]} - {pt_offset}) % 29 = {denom}  \t(pt_mult)")
            print(f"    div ({self.cipher_idx[i]} - {prev_cipher}) % 29 / {denom} = {val}\t(key_mult)")
            print(f"    inv({val}) = {inverse_output}")
        return inverse_output

    def get_possible_solutions(self, deltas):
        return [Gematria.idx_to_lat([(x+i) % 29 for x in deltas]) for i in range(29)]

    def get_possible_solutions_with_start_idx(
            self,
            pt_fcn: callable,
            key_fcn_inverse: callable,
            apply_mult_fcn: callable,
            fcn: callable,
            pt_offset: int = 0,
            key_offset: int = 0,
    ):
        sols = []
        for i in range(29):
            sols += self.decode_deltas_fast(pt_fcn, key_fcn_inverse, fcn, apply_mult_fcn, pt_offset, key_offset, i)
        return [Gematria.idx_to_lat(s) for s in sols]

    def print_deltas(self, deltas):
        for i in range(29):
            output = Gematria.idx_to_lat([(x+i) % 29 for x in deltas])
            print(output)


if __name__ == "__main__":
    from cicada.cribbing import TEST_CRIB as test_crib
    offset = [25, 28]
    VERBOSE = False

    def fcn(a, b, c, d):
        return 1
    pt_fcn = CipherFcns.identity
    key_fcn_inv = CipherFcns.un_phi
    guess = test_crib.cribs[0]

    solver = VignereSolver(guess, runes=test_crib.runes)
    possible_sols = solver.decode_deltas_fast(
        pt_fcn, key_fcn_inv, fcn, offset[0], offset[1], test_crib.prev_rune_idx, verbose=VERBOSE
    )
    sols = [Gematria.idx_to_lat(s) for s in possible_sols]
    new_solutions = [
        PossibleSolution(
            key,
            guess,
            score=FourGramTextScore.score_latin(key),
            info_str=f" [{test_crib.section}][{offset}, {pt_fcn.__name__}, "
                     f"{key_fcn_inv.__name__}, {test_crib.prev_rune_idx}]"
        )
        for key in sols
    ]
    print(sols)
    for sol in new_solutions:
        print(sol)

