from typing import List, Tuple

from cicada.gematria import Gematria
from cicada.liberprimus import LiberPrimus
from cicada.utils import get_dist


def is_list_match(list1: Tuple[int], list2: Tuple[int]) -> bool:
    for a,b in zip(list1, list2):
        if a != b:
            return False
    return True


class UnsolvedSentences:
    def __init__(self):
        self.segments = LiberPrimus.sentences
        self._segment_lengths = [len(segment) for segment in self.segments]
        self.sentences = [item for sublist in self.segments for item in sublist]
        self.sentence_lengths = [tuple([len(word) for word in sent.split(" ")]) for sent in self.sentences]

    def find_phrase(self, phrase: str):
        """
        returns a list of sentence nums and start indexes.

        :param phrase:
        :return:
        """
        runes = Gematria.lat_to_run(phrase)
        phrase_lens = tuple([len(word) for word in runes.split(" ")])

        matches = []
        for sentence_idx, sentence_lens in enumerate(self.sentence_lengths):
            if len(phrase_lens) > len(sentence_lens):
                continue
            for i in range(len(sentence_lens) - len(phrase_lens) - 1):
                if is_list_match(sentence_lens[i:i + len(sentence_lens)], phrase_lens):
                    matches.append([sentence_idx, i])
                    self.print_match(sentence_idx, i, i + len(phrase_lens) - 1)
        return matches

    def print_match(self, sentence_idx: int, start: int, end: int):
        matching_sentence = self.sentences[sentence_idx].split(" ")
        matching_sentence[start] = "\33[43m" + matching_sentence[start]
        matching_sentence[end] = matching_sentence[end] + "\33[0m"
        segment_num, sentence_num = self.get_segment_and_sentence_num_from_idx(sentence_idx)
        print(f"\nMatch found @ Segment {segment_num}, Sentence {sentence_num}, Word {start}")
        print(f"{' '.join(matching_sentence)}")

    def get_segment_and_sentence_num_from_idx(self, sentence_idx):
        sentence_count = 0
        for segment_idx, n_sentences in enumerate(self._segment_lengths):
            if sentence_idx < sentence_count + n_sentences:
                return segment_idx, sentence_idx - sentence_count
            sentence_count += n_sentences


if __name__ == "__main__":
    import sys
    phrase = sys.argv[1]

    phrase_finder = UnsolvedSentences()
    matches = phrase_finder.find_phrase(phrase)

    if not matches:
        print(f"\nNo matches found\n")
    print()

    # tao_words = [x.lower() for x in LiberPrimus.TAO.replace("\n", " ").split(" ")]
    #
    # tao_words_dict = {}
    # for word in tao_words:
    #     if len(Gematria.lat_to_run(word)) == 9:
    #         tao_words_dict[word] = tao_words_dict.get(word, 0) + 1
    #
    # from pprint import pprint
    # pprint(tao_words_dict)

