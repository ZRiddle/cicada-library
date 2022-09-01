

from cicada.bigrams import *
from cicada.gematria import Gematria
from cicada.liberprimus import LiberPrimus
from cicada.utils import get_dist


if __name__ == "__main__":
    runes_index = Gematria.run_to_idx(LiberPrimus.get_text_only(LiberPrimus.book, only_runes=True))

    delta_stream = [(runes_index[i]+runes_index[i-1]) for i in range(1, len(runes_index))]
    delta_stream_dist = get_dist(delta_stream)
    delta = []
    count = []
    for x in sorted(delta_stream_dist):
        delta.append(x)
        count.append(delta_stream_dist[x])

    N = len(sorted(delta_stream))
    ind = np.arange(N)  # the x locations for the groups
    width = 0.8  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots(figsize=(12, 7))
    p1 = ax.bar(delta, count, width)

    ax.set_ylabel('Count')
    ax.set_xlabel("Rune Delta sum")
    ax.set_title(f"LP Delta Stream distribution")
    # ax.set_xticks(ind)
    # ax.set_xticklabels(ind)

    # Label with label_type 'center' instead of the default 'edge'
    ax.bar_label(p1)

    fig.tight_layout()
    plt.show()
