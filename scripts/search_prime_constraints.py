"""
The idea here is that a lot of their sentences sum to primes when using the Gematria.
We can feed in word lengths then search cribbed words for possible sentences

# Red runes on page 23: 2,6,3,5

This is kind of useless

"""
import sys
import itertools

from cicada.gematria import Gematria
from cicada.liberprimus import Cribs
from cicada.utils import is_prime

word_lens = [int(x) for x in sys.argv[1].split(",")]

print(f"Searching for sentences with word lens: {word_lens}")

cribs = [Cribs.get_words(x) for x in word_lens]


for words in itertools.product(*cribs):
    sentence = " ".join(words)
    gem_sum = sum(Gematria.lat_to_num(sentence))
    sentence_is_prime = is_prime(gem_sum)
    if sentence_is_prime:
        print(f"{sentence_is_prime}\t{gem_sum}\t{sentence}")
