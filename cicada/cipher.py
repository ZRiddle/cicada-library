
from typing import List

from cicada.gematria import Gematria, ALL_RUNES
from cicada.liberprimus import LiberPrimus
from cicada.utils import phi, FIRST_856_PRIMES, nth_prime, is_prime


class ComplexCipher:
    """"""

    def __init__(self, key0: str, key1: str, offset: int = 11):
        self._keys = [
            Gematria.lat_to_idx(key0.replace(" ", "")),
            Gematria.lat_to_idx(key1.replace(" ", ""))
        ]
        self._key_idx = [0, 0]
        self._current_key = 0
        self._previous_rune_idx = 0
        self._offset = offset

    def encode_runes(self, text: str) -> str:
        text_indexes: List[int] = Gematria.run_to_idx(text)
        output_indexes = [0 for _ in text_indexes]

        encoded_idx_prev = 0
        for i in range(len(text_indexes)):
            idx_current = text_indexes[i]
            output_indexes[i] = self._encode_one(idx_current, encoded_idx_prev)
            encoded_idx_prev = idx_current

        return Gematria.idx_to_run(output_indexes)

    def encode_with_auto_cipher(self, text) -> str:
        print(f"Encoding with Auto-chiper")
        text_indexes: List[int] = Gematria.run_to_idx(text)
        output_indexes = [0 for _ in text_indexes]

        # Start with key 0
        key = self._keys[0]
        encoded_idx_prev = 0
        key_idx_prev = 0
        for i in range(len(text_indexes)):
            output_indexes[i] = self._encode_one_vigenere(i, text_indexes[i], encoded_idx_prev, key[i], key_idx_prev)
            encoded_idx_prev = output_indexes[i]
            key.append(encoded_idx_prev)
            key_idx_prev = key[i]

        return Gematria.idx_to_run(output_indexes)

    def _encode_one_vigenere(self, i, idx, encoded_idx_prev, key_idx, key_idx_prev) -> int:
        inc = idx * nth_prime(key_idx) + i
        output = (inc + encoded_idx_prev + self._offset) % 29
        if output == encoded_idx_prev and not is_prime(i % 1033):
            inc = idx * nth_prime(key_idx_prev) + i
            output = (inc + self._offset) % 29
        return output

    def _encode_one(self, idx: int, encoded_idx_prev: int, force: bool = False) -> int:
        """Apply an encoding given the current rune index value and previous rune encoded value"""
        inc = idx * nth_prime(self._get_key_value_and_increment()) + encoded_idx_prev
        output = (inc + self._offset) % 29

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


