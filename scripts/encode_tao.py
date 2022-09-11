
import itertools
from pprint import pprint
import random

# import required libraries
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from cicada.bigrams import *
from cicada.cipher import ComplexCipher, CipherFunctions
from cicada.gematria import Gematria, ALL_RUNES
from cicada.liberprimus import LiberPrimus, UNSOLVED_LP_RUNE_LENGTH, AlanWatts
from cicada.utils import get_dist, is_prime

LP_DOUBLET_PERCENTAGE = 0.006776821746744841


def get_random_section_equal_length(text: str, total_len: int = UNSOLVED_LP_RUNE_LENGTH):
    text_len = len(text)
    rand = random.randint(0, text_len)
    return (text + text)[rand:rand+total_len]


def within_x_perc(a, b, diff=0.01) -> bool:
    return abs(a-b)/b < diff


def get_bigram_lookup_from_matrix(matrix: np.array) -> dict:
    N = len(matrix)
    output = {}
    for i in range(N):
        for j in range(N):
            output[(i, j)] = matrix[i, j]
    return {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)}


if __name__ == "__main__":
    import sys
    try:
        N_SAMPLES = int(sys.argv[1])
    except:
        N_SAMPLES = 0
    try:
        plot_it = sys.argv[2]
    except:
        plot_it = False

    tao = LiberPrimus.tao

    # Ordered by freq
    # offsets = [25, 11, 14, 22, 12, 27, 6, 28, 21]
    offsets = [
        (25, 27), (25, 28), (22, 27), (12, 27), (27, 12), (14, 27), (22, 28),
        (28, 22), (11, 27), (28, 12), (12, 28), (14, 27), (11, 28), (14, 28),
        # Others
        (28, 11), (28, 14), (28, 25),
    ]

    # Get runes only, no spaces
    # tao_text = LiberPrimus.remove_numbers(tao)
    tao_text = AlanWatts.text
    key = get_random_section_equal_length(tao_text, 50).upper()
    tao_runes = AlanWatts.runes[:100000]
    print(f"\nKEY = {key[:500]}")
    print(f"Len Runes = {len(tao_runes)}")

    results = []
    i = 0
    total = len(offsets)**2
    #for off0, off1 in  offsets:
    for off0 in range(29):
        off1 = off0
        # print(f"Computing ({off0}, {off1})...")
        verbose = False
        # if [off0, off1] == [22, 27]:
        #     verbose = True
        cipher = ComplexCipher(
            key,
            offsets=[off0, off1],
            pt_fcn=CipherFunctions.phi,
            key_fcn=CipherFunctions.one,
            mult_fcn=CipherFunctions.primes,
            verbose=verbose,
        )
        tao_runes_encoded = cipher.encode_with_auto_cipher(tao_runes)
        bigram_matrix = get_rune_bigram_matrix(tao_runes_encoded)
        results.append([doublet_percentage(bigram_matrix), [off0, off1]])
        i += 1
        cipher.print_doublet_rate()
        # if (i % int(total/10) == 0):
        #     print(f"{i}/{total} = {i/total*100:.0f}%")

    io_num = len(['' for i in range(1, len(key)) if (key[i-1]=='I' and key[i]=='O')]) + len(['' for i in range(1, len(key)) if (key[i-1] == 'I' and key[i] == 'A')])
    print(f"\n{LP_DOUBLET_PERCENTAGE*100:.3f}%")
    print(f"# Js in KEY = {len([x for x in key if x == 'J'])}")
    print(f"# IO/IAs in KEY = {io_num} ({io_num/len(key)*100:.2f}%)")
    print(f"\nDub %\tOffsets")
    results.sort(key=lambda x: x[0])
    for res in results:
        if res[0]*100 < 100:
            same = ""
            if res[1][0] == res[1][1]:
                same = "*"
            print(f"{res[0]*100:.3f}%\t{res[1][0]:2.0f},{res[1][1]:2.0f}{same}")

    # Plot normal distributions given samples
    print(f"Generating samples")
    offsets_pairs = offsets
    samples = [[] for _ in offsets_pairs]
    for i in range(N_SAMPLES):
        key = get_random_section_equal_length(tao_text, 500).upper()
        tao_runes_subset = get_random_section_equal_length(tao_runes)
        for i, offset in enumerate(offsets_pairs):
            cipher = ComplexCipher(key, offsets=list(offset))
            bigram_mat = get_rune_bigram_matrix(cipher.encode_with_auto_cipher(tao_runes_subset, mult=13))
            samples[i].append(doublet_percentage(bigram_mat)*100)
        if i and i % 10 == 0:
            print(f"{i}/{N_SAMPLES}")

    colors = ["blue", "red"]
    if N_SAMPLES > 0:
        # Visualizing the distribution
        for i, offset in enumerate(offsets_pairs):
            fig, ax = plt.subplots(1, 1)
            ax.hist(
                samples[i], density=True, bins=15, histtype='stepfilled',
                alpha=0.25, label=f"({offset[0]},{offset[1]})"
            )
            # plt.axvline(sum(samples[i])/N_SAMPLES, color=colors[i], alpha=0.4)
            print(f"({offset[0]},{offset[1]}) - {sum(samples[i])/N_SAMPLES*100:.3f}%")
            plt.title(f"({offset[0]},{offset[1]}) Sampled doublet freq, N={N_SAMPLES}")
            plt.xlabel('Doublet proba (%)')
            plt.axvline(LP_DOUBLET_PERCENTAGE*100, color="Black", label="LP Doublet %", lw=3)
            plt.ylabel('Probability Density')
            plt.legend()
        plt.show()

    if plot_it:
        # apply cipher to text
        for i in range(1):
            print(f"Run {i}")
            tao_runes_subset = get_random_section_equal_length(tao_runes)
            cipher = ComplexCipher(
                key,
                offsets=[28, 28],
                pt_fcn=CipherFunctions.shift,
                key_fcn=CipherFunctions.one,
                mult_fcn=CipherFunctions.primes,
                verbose=False,
            )
            tao_runes_encoded = cipher.encode_with_auto_cipher(tao_runes_subset)

            bigram_matrix = get_rune_bigram_matrix(tao_runes_encoded)
            bigram_lookup = get_bigram_lookup_from_matrix(bigram_matrix)
            # for k, v in bigram_lookup.items():
            #     if v > 26 or v < 5:
            #         print(f"{k}  \t{v}")

            print(f"Doublet Perc = {doublet_percentage(bigram_matrix)*100:.3f}% vs LP = {LP_DOUBLET_PERCENTAGE*100:.3f}%")
            counts = get_counts(bigram_matrix.flatten())

            # prime_totients_mod29 = [phi(x) % 29 for x in FIRST_10k_PRIMES]
            # dist = get_dist([x for x in prime_totients_mod29])
            # pprint(dist)

            if plot_it:
                # check bigram dist
                lp_bigram_matrix = get_lp_bigram_matrix()
                lp_counts = get_counts(lp_bigram_matrix.flatten())

                plot_freq(bigram_matrix, title="Tao Te Ching random slice custom cipher")
                plot_2_freq_counts(lp_counts, counts, label2="Tao Te Ching random slice of same len")

    # if False:
    #     ct_primes = 0
    #     for i in range(1, 1222):
    #         if is_prime(i):
    #             ct_primes += 1
    #             doublet_rate_guaranteed = 1/29*ct_primes/(i+1)
    #             doublet_rate = (1/29 - doublet_rate_guaranteed)/29 + doublet_rate_guaranteed
    #             star = ""
    #             if within_x_perc(doublet_rate, LP_DOUBLET_PERCENTAGE):
    #                 star = "*"
    #             print(f"{i}{star}\t{doublet_rate:.6f}\t{LP_DOUBLET_PERCENTAGE:.6f}\t{doublet_rate_guaranteed:.6f}\t{ct_primes/(i+1)}")
    #
    # if False:
    #     totients = []
    #     for i in range(1, 100):
    #         totients.append(phi(i))
    #         print(f"{i}\t{totients[-1]}\t{is_prime(totients[-1])}")

    if plot_it:
        plt.show()