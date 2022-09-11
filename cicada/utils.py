from functools import lru_cache
import hashlib
from itertools import count, islice
import os
from typing import List, Tuple, Union

_HIGHLIGHTS = {
    "blue": "\33[44m",
    "green": "\33[42m",
    "end": "\033[0m",
}


with open(os.path.join(os.path.dirname(__file__), 'primes.txt')) as f:
    FIRST_10k_PRIMES = [int(x) for x in f.read().replace("\n", " ").split(" ") if x]

PRIME_LOOKUP = {p: True for p in FIRST_10k_PRIMES}


def is_list_match(list1: Union[List[int], Tuple[int]], list2: Union[List[int], Tuple[int]]) -> bool:
    for a, b in zip(list1, list2):
        if a != b:
            return False
    return True


def get_dist(input_list: list) -> dict:
    output = {}
    for item in input_list:
        output[item] = output.get(item, 0) + 1
    return output


def highlight_text(txt: str, color: str = "blue"):
    return _HIGHLIGHTS[color] + txt + _HIGHLIGHTS["end"]


def sha512(text: str) -> str:
    return hashlib.sha512(str.encode(text)).hexdigest()


@lru_cache
def is_prime(num: int) -> bool:
    if num <= FIRST_10k_PRIMES[-1]:
        return PRIME_LOOKUP.get(num, False)
    print(f"is_prime({num})")
    return num == 2 or num == 3 or min([num % factor for factor in range(2, int((num+2)/2))]) > 0


def generate_primes():
    yield 2
    for num in count(3, 2):
        if is_prime(num):
            yield num


def nth_prime(n: int) -> int:
    if n < len(FIRST_10k_PRIMES):
        return FIRST_10k_PRIMES[n]
    raise NotImplemented


@lru_cache
def gcd(a: int, b: int) -> int:
    """Function to return gcd of a and b"""
    if a == 0:
        return b
    return gcd(b % a, a)


@lru_cache
def phi(n: int) -> int:
    """A simple method to evaluate Euler Totient Function"""
    result = 1
    for i in range(2, n):
        if gcd(i, n) == 1:
            result += 1
    return result


if __name__ == "__main__":
    print(len(FIRST_10k_PRIMES))
    print(FIRST_10k_PRIMES[:10])
    print(FIRST_10k_PRIMES[-10:])

