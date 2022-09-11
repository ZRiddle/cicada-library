
import math
from typing import List

from cicada.utils import is_prime

ALL_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
ALL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DJU_BEI = "ᛞᛄᚢ-ᛒᛖᛁ"

MAP = (
    ("\n", "\n", -999, -999),
    (" ", " ", 0, -1),
    (u"ᚠ", "f", 2, 0),
    (u"ᚢ", "v", 3, 1),
    (u"ᚢ", "u", 3, 1),
    (u"ᚦ", "T", 5, 2),  # th
    (u"ᚩ", "o", 7, 3),
    (u"ᚱ", "r", 11, 4),
    (u"ᚳ", "k", 13, 5),
    (u"ᚳ", "c", 13, 5),
    (u"ᚷ", "g", 17, 6),
    (u"ᚹ", "w", 19, 7),
    (u"ᚻ", "h", 23, 8),
    (u"ᚾ", "n", 29, 9),
    (u"ᛁ", "i", 31, 10),
    (u"ᛄ", "j", 37, 11),
    (u"ᛇ", "E", 41, 12),  # eo
    (u"ᛈ", "p", 43, 13),
    (u"ᛉ", "x", 47, 14),
    (u"ᛋ", "z", 53, 15),
    (u"ᛋ", "s", 53, 15),
    (u"ᛏ", "t", 59, 16),
    (u"ᛒ", "b", 61, 17),
    (u"ᛖ", "e", 67, 18),
    (u"ᛗ", "m", 71, 19),
    (u"ᛚ", "l", 73, 20),
    (u"ᛝ", "G", 79, 21),  # ng
    (u"ᛝ", "G", 79, 21),  # ing
    (u"ᛟ", "O", 83, 22),  # oe
    (u"ᛞ", "d", 89, 23),
    (u"ᚪ", "a", 97, 24),
    (u"ᚫ", "A", 101, 25),  # ae
    (u"ᚣ", "y", 103, 26),
    (u"ᛡ", "I", 107, 27),  # ia
    (u"ᛡ", "I", 107, 27),  # io
    (u"ᛠ", "X", 109, 28),  # ea
)


class Gematria:
    LAT_SIMPLE = (
        ("T", "th"),
        ("E", "eo"),
        ("G", "ing"),
        ("G", "ng"),
        ("O", "oe"),
        ("A", "ae"),
        ("I", "io"),
        ("I", "ia"),
        ("X", "ea"),
    )
    RUNE_INDEXES = [i for i in range(29)]
    _MAPS = {i: {j: {p[i]: p[j] for p in MAP} for j in range(4) if i != j} for i in range(4)}

    @classmethod
    def get_rune_idx(cls, rune: str) -> int:
        return ALL_RUNES.find(rune)

    @classmethod
    def get_idx_from_rune(cls, idx: int) -> str:
        return ALL_RUNES[idx]

    # algorithm taken from here: https://pastebin.com/6v1XC1kV
    @classmethod
    def gem_map(cls, x: any, src: int, dest: int):
        m = cls._MAPS[src][dest]
        return [m[c] if c in m else c for c in x]

    @classmethod
    def lat_to_sim(cls, x: str) -> str:
        x = x.replace("qu", "cw")
        for sim in cls.LAT_SIMPLE:
            x = x.replace(sim[1], sim[0])
        return x

    @classmethod
    def sim_to_lat(cls, x: str) -> str:
        for sim in cls.LAT_SIMPLE:
            x = x.replace(sim[0], sim[1])
        return x

    @classmethod
    def run_to_lat(cls, x: str) -> str:
        return cls.sim_to_lat("".join(cls.gem_map(x, 0, 1)))

    @classmethod
    def run_to_num(cls, x: str) -> List[int]:
        return cls.gem_map(x, 0, 2)

    @classmethod
    def lat_to_run(cls, x: str) -> str:
        x = x.lower().replace("qu", "cw")
        return "".join(cls.gem_map(cls.lat_to_sim(x), 1, 0))

    @classmethod
    def lat_to_num(cls, x: str) -> List[int]:
        # strip non alpha chars when converting to num
        x = "".join([c for c in x if c.isalpha() or c == " "])
        return cls.gem_map(cls.lat_to_sim(x.lower()), 1, 2)

    @classmethod
    def num_to_run(cls, x: List[int]) -> str:
        return "".join(cls.gem_map(x, 2, 0))

    @classmethod
    def num_to_lat(cls, x: List[int]) -> str:
        return cls.sim_to_lat("".join(cls.gem_map(x, 2, 1)))

    @classmethod
    def lat_to_idx(cls, x: str) -> List[int]:
        return cls.gem_map(cls.lat_to_sim(x.lower()), 1, 3)

    @classmethod
    def idx_to_lat(cls, x: List[int]) -> str:
        return cls.sim_to_lat("".join(cls.gem_map(x, 3, 1))).upper()

    @classmethod
    def run_to_idx(cls, x: str) -> List[int]:
        return cls.gem_map(x, 0, 3)

    @classmethod
    def idx_to_run(cls, x: List[int]) -> str:
        return cls.sim_to_lat("".join(cls.gem_map(x, 3, 0)))

    @classmethod
    def sum_lat(cls, x: str) -> int:
        return sum(cls.lat_to_num(x))

    @classmethod
    def sum_run(cls, x: str) -> int:
        return sum(cls.run_to_num(x))

    @classmethod
    def shift_by_previous_rune(cls, runes, start_rune: int = 0) -> str:
        """
        If we assume the LP is shifted by the previous rune to achieve the doublet distribution
        then this will undo that
        """
        output = cls.run_to_idx(runes)
        rune_indexes = output.copy()

        prev_rune = start_rune
        for i in range(len(output)):
            if output[i] in cls.RUNE_INDEXES:
                output[i] = (output[i] + prev_rune) % 29
                prev_rune = rune_indexes[i]
        return cls.idx_to_run(output)


class Cipher:
    def __repr__(self):
        return "<Cipher %s>" % (self.text)

    def __str__(self):
        return self.text

    def __init__(self, text, alpha):
        self.text = text
        self.alpha = alpha
        self.primes = lambda: (  # generates an infinite number of prime numbers
            n
            for n, _ in enumerate(iter(int, 1))  # for every value of n
            if n % 2 != 0  # but only if n is not even
            and all(
                n % p != 0 for p in range(3, int(math.sqrt(n)) + 1, 2)
            )  # not divisable by 3..sqrt(n)+1, skipping even numbers
            and n
            != 1  # 1 doesn't count as prime (we're not counting 2 specific factors, so this has to be hardcoded)
            or n == 2  # bypass the even number skip for 2.
        )

    def to_runes(self):
        return Runes(Gematria.lat_to_run(self.text))

    def to_latin(self):
        return Latin(Gematria.run_to_lat(self.text))

    def to_numbers(self):
        return Gematria.run_to_num(Gematria.lat_to_run(self.text))

    def sub(self, plain, cipher):
        self.text = self.text.upper()
        return Cipher(self.text.translate(str.maketrans(plain, cipher)), self.alpha)

    def shift(self, n):
        return self.sub(self.alpha, self.alpha[n:] + self.alpha[:n])

    def atbash(self):
        return self.sub(self.alpha, self.alpha[::-1])

    def gematria_sum(self):
        return sum([n for n in self.to_numbers() if type(n) is int])

    def gematria_sum_words(self):
        return [Runes(w).gematria_sum() for w in self.text.split()]

    def gematria_sum_lines(self):
        return [Runes(w).gematria_sum() for w in self.text.splitlines()]

    def to_index(self):
        return [self.alpha.index(i.upper()) for i in self.text.upper()]

    def running_shift(self, key, interrupts="", skip_indices=[], decrypt=True):
        if not key:
            return self.text

        # handles modulo
        def key_generator(key):
            while True:
                for k in key:
                    yield k

        key = key_generator(key)
        if type(interrupts) == list:
            interrupts = "".join(interrupts)
        o = ""
        i = 0

        for c in self.text:
            if c not in self.alpha or c in interrupts.upper():
                o += c
                continue
            if i in skip_indices:
                o += c
                i += 1
                continue
            c_index = self.alpha.index(c)
            # grab next key value
            shift = next(key)
            if decrypt:
                # invert the shift to decrypt
                shift = -shift
            # shift c by shift, wrap around if shift is longer than alpha
            o += self.alpha[(c_index + shift) % len(self.alpha)]
            i += 1

        return Cipher(o, self.alpha)

    def vigenere(self, key, interrupts=[], decrypt=True):
        key = [self.alpha.index(k) for k in key.upper() if k in self.alpha]
        return self.running_shift(key, interrupts=interrupts, decrypt=decrypt)

    def totient_stream(self, interrupts="", skip_indices=[], decrypt=True):
        return self.running_shift(
            (p - 1 for p in self.primes()),
            interrupts=interrupts,
            skip_indices=skip_indices,
            decrypt=decrypt,
        )


class Runes(Cipher):
    def __init__(self, text):
        super().__init__(text, ALL_RUNES)


class Latin(Cipher):
    def __init__(self, text):
        super().__init__(text.upper(), ALL_LETTERS)


class Hex(Cipher):
    def __init__(self, text):
        super().__init__(text.upper(), "0123456789ABCDEF")


# for num in range(2,12):
#     rems = [num % factor for factor in range(2, int((num+1)/2))]
#     print(f"{num}\t{rems}")


if __name__ == "__main__":
    import sys

    word = sys.argv[1].upper()
    gem_sum = sum(Gematria.lat_to_num(word))

    print(f'sum( "{word}" ) = {gem_sum}, prime={is_prime(gem_sum)}')



    # txt = "Butter my toast".upper()
    # print(f"text:\t{txt}")
    # txt_run = Gematria.lat_to_run(txt)
    # txt_idx = Gematria.lat_to_idx(txt)
    #
    # txt_run_idx = Gematria.run_to_idx(txt_run)
    # txt_idx_run = Gematria.idx_to_run(txt_idx)
    #
    # print(f"Runes")
    # print(f"{txt_run}")
    # print(f"{txt_idx_run}")
    # print(f"Idx")
    # print(f"{txt_idx}")
    # print(f"{txt_run_idx}")
    # print(f"Text")
    # print(f"{Gematria.run_to_lat(txt_idx_run)}")
    # print(f"{Gematria.idx_to_lat(txt_run_idx)}")
    #
    # print(f"")
