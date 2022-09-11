from typing import List, Tuple

from cicada.gematria import Gematria
from cicada.liberprimus import LiberPrimus
from cicada.utils import is_list_match


class UnsolvedSentences:
    def __init__(self):
        self.segments = LiberPrimus.sentences
        self._segment_lengths = [len(segment) for segment in self.segments]
        self.sentences = [item for sublist in self.segments for item in sublist]
        self.sentence_lengths = [tuple([len(word) for word in sent.split(" ")]) for sent in self.sentences]

    def get_sentence_by_letter_index(self, letter_index: int):
        total_letters = 0
        for sentence, sentence_lens in zip(self.sentences, self.sentence_lengths):
            if letter_index < total_letters + sum(sentence_lens):
                return sentence, letter_index - total_letters
            total_letters += sum(sentence_lens)
        print(f"Broke for letter_index = {letter_index}")

    def get_phrase_by_sentence_and_word_index(self, sentence_idx: int, word_idx: int, length: int = 1):
        words = self.sentences[sentence_idx].split(" ")
        if word_idx == 0:
            prev_rune_idx = self.sentences[sentence_idx-1][-1][-1]
        else:
            prev_rune_idx = words[word_idx-1][-1]
        return " ".join(words[word_idx:word_idx+length]), prev_rune_idx, sentence_idx

    def find_phrase(self, phrase: str):
        """
        returns a list of sentence nums and start indexes.

        :param phrase:
        :return:
        """
        runes = Gematria.lat_to_run(phrase)
        phrase_lens = tuple([len(word) for word in runes.split(" ")])
        print(f"Searching for {phrase} = {runes} = {phrase_lens}")

        matches = []
        for sentence_idx, sentence_lens in enumerate(self.sentence_lengths):
            if len(phrase_lens) > len(sentence_lens):
                continue
            for i in range(len(sentence_lens) - len(phrase_lens) + 1):
                if is_list_match(sentence_lens[i:i + len(sentence_lens)], phrase_lens):
                    matches.append([sentence_idx, i])
                    self.print_match(sentence_idx, i, i + len(phrase_lens) - 1)
        return matches

    def print_match(self, sentence_idx: int, start: int, end: int, buffer: int = 2):
        matching_sentence = self.sentences[sentence_idx].split(" ")
        buffer_start = max(0, start - buffer)
        buffer_end = min(end + buffer + 1, len(matching_sentence))
        word_lens = [len(word) for word in matching_sentence[buffer_start:buffer_end]]
        matching_sentence[start] = "\33[43m" + matching_sentence[start]
        matching_sentence[end] = matching_sentence[end] + "\33[0m"
        segment_num, sentence_num = self.get_segment_and_sentence_num_from_idx(sentence_idx)
        print(f"\nMatch found @ Segment {segment_num}, Sentence {sentence_num}, Word {start}")
        print(f"{' '.join(matching_sentence)}")
        print(f"Surrounding word lens: {word_lens}")

    def get_segment_and_sentence_num_from_idx(self, sentence_idx):
        sentence_count = 0
        for segment_idx, n_sentences in enumerate(self._segment_lengths):
            if sentence_idx < sentence_count + n_sentences:
                return segment_idx, sentence_idx - sentence_count
            sentence_count += n_sentences


if __name__ == "__main__":
    import sys
    phrase = sys.argv[1]

    try:
        print_output = sys.argv[2]
    except:
        print_output = False

    phrase_len = len(phrase.split(" "))

    phrase_finder = UnsolvedSentences()
    matches = phrase_finder.find_phrase(phrase)
    output = [phrase_finder.get_phrase_by_sentence_and_word_index(m[0], m[1], phrase_len) for m in matches]

    if print_output:
        print(f"\nPhrase Len = {len(phrase.replace(' ', ''))}\nCribSetups\n")
        for out in output:
            print(f'CribSetup({out[2]}, \"{out[0].replace(" ", "")}\", [\"{phrase.upper().replace(" ", "")}\"], '
                  f'prev_rune_idx={Gematria.run_to_idx(out[1])[0]})')

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

