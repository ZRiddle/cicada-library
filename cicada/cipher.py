
from typing import List

from cicada.gematria import Gematria, ALL_RUNES
from cicada.liberprimus import LiberPrimus
from cicada.utils import phi, nth_prime, is_prime
from cicada.cipher_utils import CipherFcns


class CipherFunctions:
    @classmethod
    def shift(cls, idx: int, offset: int = 0) -> int:
        """simple offset shift"""
        return (idx - offset) % 29

    @classmethod
    def nth_prime(cls, idx: int, offset: int = 0) -> int:
        """get nth_prime % 29. Apply a shift of 9 to reset to 0"""
        return nth_prime((idx - offset + 9) % 29) % 29

    @classmethod
    def phi(cls, idx: int, offset: int = 0) -> int:
        """get nth_prime % 29. Apply a shift of 16 to reset to 0"""
        return (nth_prime((idx - offset + 16) % 29) - 1) % 29

    @classmethod
    def primes(cls, i: int, k: int = 1) -> int:
        """get nth_prime % 29. Apply a shift of 16 to reset to 0"""
        return (nth_prime(i % 13000)) * k % 29

    @classmethod
    def totients(cls, i: int, k: int = 1) -> int:
        """get nth_prime % 29. Apply a shift of 16 to reset to 0"""
        return (nth_prime(i % 13000) - 1) * k % 29

    @classmethod
    def constant(cls, i: int, k: int = 1) -> int:
        """get nth_prime % 29. Apply a shift of 16 to reset to 0"""
        return k % 29

    @classmethod
    def one(cls, i: int, k: int = 1) -> int:
        """get nth_prime % 29. Apply a shift of 16 to reset to 0"""
        return 1


class ComplexCipher:
    """"""

    def __init__(
            self,
            key0: str,
            key1: str = "YO",
            offsets: List[int] = None,
            pt_fcn: callable = None,
            key_fcn: callable = None,
            mult_fcn: callable = None,
            apply_mult_fcn: callable = None,
            verbose: bool = False
    ):
        self._keys = [
            Gematria.lat_to_idx(LiberPrimus.get_only_lat(key0)),
            Gematria.lat_to_idx(LiberPrimus.get_only_lat(key1)),
        ]
        self.verbose = verbose
        self._key_idx = [0, 0]
        self._current_key = 0
        self._previous_rune_idx = 0

        self._offsets = offsets
        self._pt_fcn = pt_fcn
        self._key_fcn = key_fcn
        self._mult_fcn = mult_fcn
        self._apply_mult_fcn = apply_mult_fcn
        if not offsets:
            self._offsets = [0, 0, 0]
        if not pt_fcn:
            self._pt_fcn = CipherFunctions.shift
        if not key_fcn:
            self._key_fcn = CipherFunctions.shift
        if not mult_fcn:
            self._mult_fcn = CipherFunctions.constant
        if not apply_mult_fcn:
            self._apply_mult_fcn = CipherFcns.mul
        self.doublet_count = 0
        self.doublet_from_mult = 0
        self.doublet_from_pt = 0
        self.doublet_from_key = 0

    def encode_runes(self, text: str) -> str:
        text_indexes: List[int] = Gematria.run_to_idx(text)
        output_indexes = [0 for _ in text_indexes]

        encoded_idx_prev = 0
        for i in range(len(text_indexes)):
            idx_current = text_indexes[i]
            output_indexes[i] = self._encode_one(idx_current, encoded_idx_prev)
            encoded_idx_prev = idx_current

        return Gematria.idx_to_run(output_indexes)

    def encode_with_auto_cipher(self, text, mult: int = 1, encoded_idx_prev: int = 0, verbose: bool = False) -> str:
        # print(f"Encoding with Auto-chiper")
        text_indexes: List[int] = Gematria.run_to_idx(text)
        output_indexes = [0 for _ in text_indexes]

        self.doublet_count = 0
        self.doublet_from_pt = 0
        self.doublet_from_key = 0

        if self.verbose:
            print(f"\ni\tPT\tKey\tC[i]\tC[i-1]\tinc")
            print("-"*22)

        # Start with key 0
        key = self._keys[0]
        key_idx_prev = 0
        for i in range(len(text_indexes)):
            output_indexes[i] = self._encode_one_vigenere(i, text_indexes[i], encoded_idx_prev, key[i], key_idx_prev, verbose, mult)
            encoded_idx_prev = output_indexes[i]
            key.append(text_indexes[i])
            key_idx_prev = key[i]

        return Gematria.idx_to_run(output_indexes)

    def _encode_one_vigenere(self, i, pt, encoded_idx_prev, key_idx, key_idx_prev, verbose, mult: int = 1) -> int:
        """
        nth_prime(9)      % 29 = 0
        nth_prime(16) - 1 % 29 = 0
        """
        pt_mult = self._pt_fcn(pt, self._offsets[0])
        key_mult = self._key_fcn(key_idx, self._offsets[1])
        mult = self._mult_fcn(i, mult)
        inc = self._apply_mult_fcn(pt_mult * key_mult, mult)  # phi(i)
        output = (inc + encoded_idx_prev) % 29
        if verbose:
            print(f"{i}\t{pt=}\t{pt_mult=}\t{key_idx=}\t{key_mult=}\t{output=}")
        if output == encoded_idx_prev:
            self.doublet_count += 1
            pt_text = f"PT={pt}"
            key_text = f"K={key_idx}"
            if pt_mult == 0:
                self.doublet_from_pt += 1
                pt_text = f"\33[43m{pt_text}\33[0m"
            if key_mult == 0:
                self.doublet_from_key += 1
                key_text = f"\33[43m{key_text}\33[0m"
            if mult == 0:
                self.doublet_from_mult += 1

            if self.verbose:
                print(f"{i}\t{pt_text}\t{key_text}\tC[i]={output}\tC[i-1]={encoded_idx_prev}\tinc={inc}, {inc%29}")
        return output

    def print_doublet_rate(self):
        print(
            f"({self._offsets[0]}, {self._offsets[1]})\t"
            f"PT={self.doublet_from_pt/self.doublet_count*100:.2f}%\t"
            f"Key={self.doublet_from_key/self.doublet_count*100:.2f}%\t"
            f"Mul={self.doublet_from_mult/self.doublet_count*100:.2f}%\t"
        )

    # -----------------------------
    # ------------ Old ------------
    def _encode_one(self, idx: int, encoded_idx_prev: int, force: bool = False) -> int:
        """Apply an encoding given the current rune index value and previous rune encoded value"""
        inc = idx * nth_prime(self._get_key_value_and_increment()) + encoded_idx_prev
        output = (inc + self._offsets[0]) % 29

        if not force and output == encoded_idx_prev:
            # switch keys are re-run
            self._switch_key()
            return self._encode_one(idx, encoded_idx_prev, True)

        return output

    def _get_key_value_and_increment(self) -> int:
        current_key_value = self._keys[self._current_key][self._key_idx[self._current_key]]
        self._key_idx[self._current_key] = (self._key_idx[self._current_key] + 1) % len(self._keys[self._current_key])
        return current_key_value

    def _switch_key(self):
        if self._current_key == 0:
            self._current_key = 1
        else:
            self._current_key = 0


if __name__ == "__main__":
    PT = "COSMICCONSCIOUSNESS"
    KEY = "BUTTER MY TOAST"
    offsets = [25, 28]
    pt_fcn = CipherFunctions.shift
    key_fcn = CipherFunctions.phi

    cipher = ComplexCipher(KEY, KEY, offsets, pt_fcn, key_fcn)
    output = cipher.encode_with_auto_cipher(Gematria.lat_to_run(PT), verbose=True)

    print(f"Complex Cipher")
    print(f"plaintext = {PT}")
    print(f"key       = {KEY}")
    print(f"offsets   = {offsets}")
    print(f"pt_fcn    = {pt_fcn.__name__}")
    print(f"key_fcn   = {key_fcn.__name__}")
    print(f"message   = {output}")

    # for i in range(29):
    #     print(f"{(nth_prime(i) - 1) % 29}: {i},")

