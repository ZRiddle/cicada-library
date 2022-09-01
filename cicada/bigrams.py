
from typing import List, Union

import numpy as np
import matplotlib
import matplotlib.font_manager
import matplotlib.pyplot as plt

from cicada.gematria import Gematria, ALL_RUNES
from cicada.liberprimus import LiberPrimus
from cicada.utils import phi, FIRST_856_PRIMES


def get_rune_bigram_matrix(text: Union[str, List[str]]) -> np.array:
    """Build a matrix count of bigrams from an input text"""
    text_clean = LiberPrimus.get_text_only(text).upper()
    # print(f"Len of unsolved LP runes only = {len(text_clean)}")
    output = np.zeros((len(ALL_RUNES), len(ALL_RUNES)))

    for i in range(len(text_clean)-1):
        idx_i = Gematria.get_rune_idx(text_clean[i])
        idx_i1 = Gematria.get_rune_idx(text_clean[i+1])
        if idx_i >= 0 and idx_i1 >= 0:
            output[idx_i, idx_i1] += 1

    print(f"Doublet Perc: {doublet_percentage(output):.6f}")
    print(f"Doublet Perc delta: {doublet_percentage(output)*29-1/29**2:.6f}")
    return output.astype(int)


def _plot_freq(ax, matrix, title):
    ax.matshow(matrix, cmap=plt.cm.jet)
    ax.set_title(title)

    #sx = ax.secondary_xaxis('bottom')
    #sy = ax.secondary_yaxis('right')

    ax.set_xticks(np.arange(29), np.arange(29), rotation=90)
    ax.set_yticks(np.arange(29))

    runes = ['ᚠ', 'ᚢ', 'ᚦ', 'ᚩ', 'ᚱ', 'v', 'ᚷ', 'ᚹ', 'ᚻ', 'ᚾ', 'ᛁ', 'ᛄ', 'ᛇ', 'ᛈ', 'ᛉ',
             'ᛋ', 'ᛏ', 'ᛒ', 'ᛖ', 'ᛗ', 'ᛚ', 'ᛝ', 'ᛟ', 'ᛞ', 'ᚪ', 'ᚫ', 'ᚣ', 'ᛡ', 'ᛠ ']
    # sx.set_xticklabels(runes)
    # sy.set_yticklabels(runes)

    for i in range(29):
        for j in range(29):
            c = matrix[j, i]
            ax.text(i, j, str(c), va='center', ha='center')
    return ax


def plot_freq(matrix: np.array, title="Unsolved LP"):
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Verdana"
    fig, ax = plt.subplots(figsize=(12, 9))

    ax = _plot_freq(ax, matrix, title)

    fig.tight_layout()
    return ax


def doublet_percentage(matrix: np.array) -> float:
    return matrix.trace() / matrix.sum()


def plot_2_freq_counts(counts_lp: np.array, counts: np.array, label2: str = "Tao Te Ching", plot_normal_dist=False):
    N = max(len(counts), len(counts_lp))
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots(figsize=(12, 7))
    p1 = ax.bar(np.arange(len(counts_lp)) + (0.5-width), counts_lp, width, label="Libra Primus")
    p2 = ax.bar(np.arange(len(counts)) + 0.5, counts, width, label=label2)

    ax.set_ylabel('Count')
    ax.set_title("Bigram frequency counts")
    # ax.set_xticks(ind)
    # ax.set_xticklabels(ind)
    plt.legend()

    # Label with label_type 'center' instead of the default 'edge'
    ax.bar_label(p1)
    ax.bar_label(p2)

    ax.set_xlim(-1, N)

    if plot_normal_dist:
        x = np.linspace(0, N, 101)
        yg = [my_gauss(xi, sigma=4, h=int(counts.max()), mid=N/2) for xi in x]
        ax.plot(x, yg, color="red")

    fig.tight_layout()
    return ax


def plot_counts(counts: np.array, title="Bigram frequency counts", xlabel="", plot_normal=False):
    N = len(counts)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.8  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots(figsize=(12, 7))
    p1 = ax.bar(ind, counts, width)

    ax.set_ylabel('Count')
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    # ax.set_xticks(ind)
    # ax.set_xticklabels(ind)

    # Label with label_type 'center' instead of the default 'edge'
    ax.bar_label(p1)

    # ax.set_xlim(-1, N)

    if plot_normal:
        x = np.linspace(0, N, 101)
        yg = [my_gauss(xi, sigma=4, h=int(counts.max()), mid=N/2) for xi in x]
        ax.plot(x, yg, color="red")

    fig.tight_layout()
    return ax


def get_counts(lst: Union[np.array, List[int]]) -> np.array:
    """Returns a list of integer counts"""

    counts = np.zeros(max(lst)+1)
    for x in lst:
        counts[x] += 1
    return counts


def my_gauss(x, sigma=1, h=1, mid=0):
    from math import exp, pow
    variance = pow(sigma, 2)
    return h * exp(-pow(x-mid, 2)/(2*variance))


def get_lp_bigram_matrix() -> np.array:
    lp = LiberPrimus.book
    return get_rune_bigram_matrix(lp)


if __name__ == "__main__":
    bigram_matrix = get_lp_bigram_matrix()
    counts = get_counts(bigram_matrix.flatten())

    lp = LiberPrimus.book
    plot_freq(bigram_matrix)
    plt.savefig("unsolved_bigram_heatmap.png")

    if False:
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 13))
        print(f"\nPages\tDoublet %")
        for i, ax in enumerate(axes.flat, start=1):
            if i > 8:
                continue
            section = LiberPrimus.BOOK_SECTIONS[i-1]
            bigram_matrix = get_rune_bigram_matrix(lp[section[0]:section[1]])
            print(f"{section[0]}-{section[1]-1}\t{doublet_percentage(bigram_matrix)*100:.2f}%")
            _plot_freq(ax, bigram_matrix, f"Pages {section[0]}-{section[1]-1} bigrams | {doublet_percentage(bigram_matrix)*100:.2f}% doublets")

        axes[-1, -1].axis('off')
        fig.tight_layout()

    # prime_totients_mod29 = [phi(x) % 29 for x in FIRST_856_PRIMES]
    # N = 3000
    # natural_totients_mod29 = [phi(x) % 29 for x in range(N)]
    # plot_counts(get_counts(prime_totients_mod29), f"Prime Numbers up to {FIRST_856_PRIMES[-1]} (totient % 29) distribution")
    # plot_counts(get_counts(natural_totients_mod29), f"Natural Numbers up to {N} (totient % 29) distribution")

    plt.show()
