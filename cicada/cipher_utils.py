from typing import Union, List

_un_mult = {a: {b: [] for b in range(29)} for a in range(29)}
for i in range(29):
    for j in range(29):
        answer = (i * j) % 29
        _un_mult[i][answer].append(j)

_nth_prime = {
    0: 2,
    1: 3,
    2: 5,
    3: 7,
    4: 11,
    5: 13,
    6: 17,
    7: 19,
    8: 23,
    9: 0,
    10: 2,
    11: 8,
    12: 12,
    13: 14,
    14: 18,
    15: 24,
    16: 1,
    17: 3,
    18: 9,
    19: 13,
    20: 15,
    21: 21,
    22: 25,
    23: 2,
    24: 10,
    25: 14,
    26: 16,
    27: 20,
    28: 22,
}
_phi = {
    0: 1,
    1: 2,
    2: 4,
    3: 6,
    4: 10,
    5: 12,
    6: 16,
    7: 18,
    8: 22,
    9: 28,
    10: 1,
    11: 7,
    12: 11,
    13: 13,
    14: 17,
    15: 23,
    16: 0,
    17: 2,
    18: 8,
    19: 12,
    20: 14,
    21: 20,
    22: 24,
    23: 1,
    24: 9,
    25: 13,
    26: 15,
    27: 19,
    28: 21,
}

_nth_prime_reverse = {
    0: [9],
    1: [16],
    2: [0, 10, 23],
    3: [1, 17],
    5: [2],
    8: [11],
    9: [18],
    7: [3],
    10: [24],
    11: [4],
    12: [12],
    13: [5, 19],
    14: [13, 25],
    15: [20],
    16: [26],
    17: [6],
    18: [14],
    19: [7],
    20: [27],
    21: [21],
    22: [28],
    23: [8],
    24: [15],
    25: [22],
}

_phi_reverse = {
    0: [16],
    1: [0, 10, 23],
    2: [1, 17],
    4: [2],
    6: [3],
    7: [11],
    8: [18],
    9: [24],
    10: [4],
    11: [12],
    12: [5, 19],
    13: [13, 25],
    14: [20],
    15: [26],
    16: [6],
    17: [14],
    18: [7],
    19: [27],
    20: [21],
    21: [28],
    22: [8],
    23: [15],
    24: [22],
    28: [9],
}


class CipherFcns:
    """This will be a class that does a simple lookup to reverse encodings for mod 29"""
    _add = {a: {b: (a + b) % 29 for b in range(29)} for a in range(29)}
    _sub = {a: {b: (a - b) % 29 for b in range(29)} for a in range(29)}
    _mul = {a: {b: (a * b) % 29 for b in range(29)} for a in range(29)}
    _div = {a: {(a * b) % 29: b for b in range(29)} for a in range(29)}
    _div[0] = {a: 0 for a in range(29)}  # Fix 0 even though it's technically unsolvable

    @classmethod
    def iden(cls, a: int):
        return a % 29

    @classmethod
    def one(cls, a: int):
        return 1

    @classmethod
    def add(cls, a: int, b: int) -> int:
        """(a + b) % 29"""
        return cls._add[a % 29][b % 29]

    @classmethod
    def sub(cls, a: int, b: int) -> int:
        """(a - b) % 29"""
        return cls._sub[a % 29][b % 29]

    @classmethod
    def mul(cls, a: int, b: int) -> int:
        """(a * b) % 29"""
        return cls._mul[a % 29][b % 29]

    @classmethod
    def div(cls, a: int, b: int) -> int:
        """returns x for a = (x * b) % 29 --- x = a/b"""
        return cls._div[b % 29][a % 29]

    @classmethod
    def div_sub_1(cls, a: int, b: int) -> int:
        """returns x for a = (x * b) % 29 --- x = a/b"""
        return cls.sub(cls.div(a, b), 1)

    @classmethod
    def xor(cls, a: int, b: int) -> int:
        raise NotImplemented

    @classmethod
    def nth_prime(cls, a: int) -> int:
        return _nth_prime.get((a + 9) % 29)

    @classmethod
    def phi(cls, a: int) -> int:
        return _phi.get((a + 16) % 29)

    @classmethod
    def un_mul(cls, a: int, b: int) -> List[int]:
        return _un_mult[a % 29][b % 29]

    @classmethod
    def un_one(cls, a: int) -> List[int]:
        return [1]

    @classmethod
    def un_iden(cls, a: int) -> List[int]:
        """Returns a list to match the other un_ fcns"""
        return [a % 29]

    @classmethod
    def un_nth_prime(cls, a: int) -> List[int]:
        return [(x - 9) % 29 for x in _nth_prime_reverse.get(a % 29, [])]

    @classmethod
    def un_phi(cls, a: int) -> List[int]:
        return [(x - 16) % 29 for x in _phi_reverse.get(a % 29, [])]


if __name__ == "__main__":
    print("\nPhi")
    for i in range(29):
        output = CipherFcns.un_phi(CipherFcns.phi(i))
        print(f"{i}\t{CipherFcns.phi(i)}\t{i in output}\t{output}")

    _div = {a: {b: [] for b in range(29)} for a in range(29)}
    for i in range(29):
        for j in range(29):
            answer = CipherFcns.mul(i, j)
            _div[i][answer].append(j)
    from pprint import pprint
    pprint(_div)

    # print("\nNth Prime")
    # for i in range(29):
    #     output = CipherFcns.un_nth_prime(CipherFcns.nth_prime(i))
    #     print(f"{i}\t{CipherFcns.nth_prime(i)}\t{i in output}\t{output}")
