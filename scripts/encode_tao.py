
from pprint import pprint
import random

from cicada.bigrams import *
from cicada.cipher import ComplexCipher
from cicada.gematria import Gematria, ALL_RUNES
from cicada.liberprimus import LiberPrimus, UNSOLVED_LP_RUNE_LENGTH
from cicada.utils import get_dist, is_prime

LP_DOUBLET_PERCENTAGE = 0.006776821746744841


def encode(text: str) -> str:
    key0 = "ULTIMATE TRUTH IS THE ULTIMATE ILLUSION KNOW YOURSELF BEFORE YOU WRECK YOURSELF"
    key1 = "THE TOTIENT FUNCTION IS SACRED ALL THINGS SHOULD BE ENCRYPTED"

    cipher = ComplexCipher(key0, key1)

    return cipher.encode_with_auto_cipher(text)


def get_random_section_equal_length(text: str):
    text_len = len(text)
    rand = random.randint(0, text_len)
    return (text + text)[rand:rand+UNSOLVED_LP_RUNE_LENGTH]


def within_x_perc(a, b, diff=0.01) -> bool:
    return abs(a-b)/b < diff


if __name__ == "__main__":
    import sys
    try:
        plot_it = sys.argv[1]
    except:
        plot_it = False
    tao = LiberPrimus.tao

    perc_delta = 0.184613

    # Get runes only, no spaces
    tao_runes = Gematria.lat_to_run(LiberPrimus.remove_numbers(tao)).replace("-", " ").replace(" ", "")

    # apply cipher to text
    for i in range(3):
        print(f"Run {i}")
        tao_runes_subset = get_random_section_equal_length(tao_runes)
        tao_encoded_runes = encode(tao_runes_subset)

        bigram_matrix = get_rune_bigram_matrix(tao_encoded_runes)
        print(f"Doublet Perc = {doublet_percentage(bigram_matrix)*100:.3f}% vs LP = {LP_DOUBLET_PERCENTAGE*100:.3f}%")
        counts = get_counts(bigram_matrix.flatten())

        # prime_totients_mod29 = [phi(x) % 29 for x in FIRST_856_PRIMES]
        # dist = get_dist([x for x in prime_totients_mod29])
        # pprint(dist)

        if plot_it:
            # check bigram dist
            lp_bigram_matrix = get_lp_bigram_matrix()
            lp_counts = get_counts(lp_bigram_matrix.flatten())

            plot_freq(bigram_matrix, title="Tao Te Ching random slice custom cipher")
            plot_2_freq_counts(lp_counts, counts, label2="Tao Te Ching random slice of same len")

    if False:
        ct_primes = 0
        for i in range(1, 1222):
            if is_prime(i):
                ct_primes += 1
                doublet_rate_guaranteed = 1/29*ct_primes/(i+1)
                doublet_rate = (1/29 - doublet_rate_guaranteed)/29 + doublet_rate_guaranteed
                star = ""
                if within_x_perc(doublet_rate, LP_DOUBLET_PERCENTAGE):
                    star = "*"
                print(f"{i}{star}\t{doublet_rate:.6f}\t{LP_DOUBLET_PERCENTAGE:.6f}\t{doublet_rate_guaranteed:.6f}\t{ct_primes/(i+1)}")

    if True:
        totients = []
        for i in range(1, 100):
            totients.append(phi(i))
            print(f"{i}\t{totients[-1]}\t{is_prime(totients[-1])}")

    if plot_it:
        plt.show()