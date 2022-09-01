
from itertools import count, islice
from cicada import LiberPrimus
from cicada.gematria import Latin, Runes, Gematria

from cicada.pybar import PyBar
import math

# load the lp from file
lp = LiberPrimus()

gm = Gematria()


def is_prime(num):
    return num == 2 or num == 3 or min([num % factor for factor in range(2, int((num+2)/2))]) > 0

def generate_primes():
    yield 2
    for num in count(3, 2):
        if is_prime(num):
            yield num

def nth_prime(n):
    return next(islice(generate_primes(), n, None))


for num in range(2,12):
    rems = [num % factor for factor in range(2, int((num+1)/2))]
    print(f"{num}\t{rems}")



cipher = Runes(lp.strip_delims(lp.pages[-2].text)).text
cipher = cipher.split("\n\n")[0] + cipher.split("\n\n")[2]

cipher_idx = gm.run_to_idx(cipher)

decoded_idx = cipher_idx.copy()


letter_idx = 0
need_to_skip = True
for idx, num in enumerate(decoded_idx):
    if need_to_skip and letter_idx == 57:
        letter_idx -= 1
        need_to_skip = False
    if num >= 0:
        rune_idx = (cipher_idx[idx] - nth_prime(letter_idx) + 1) % 29
        decoded_idx[idx] = rune_idx
        letter_idx += 1


output_runes = gm.idx_to_run(decoded_idx)
output_latin = gm.run_to_lat(output_runes)

print(cipher_idx[:5])
print(decoded_idx[:5])

print(output_latin)




# Useful Prime Lookups
# N    | Prime
# ------------
# 0    | 2
# 173  | 1033
# 1033 | 8237
# 1131 | 9133
# 3301 | 30593


