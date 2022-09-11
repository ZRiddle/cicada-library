
import json
import os
import re
from dataclasses import dataclass
from typing import Optional, List, Union

from cicada.gematria import ALL_RUNES, ALL_LETTERS, Gematria

LIBER_PRIMUS_FILEPATH = "../data/liber_primus.txt"
TAO_FILEPATH = "../data/tao.txt"
UNSOLVED_LP_RUNE_LENGTH = 13170

SEGMENT_RUNE_OFFSETS = {
    0: 0,
    1: 729,
    2: 1874,
    3: 3612,
    4: 5506,
    5: 6527,
    6: 8051,
    7: 9640,
}
PAGE_RUNE_OFFSET = {
    0: 0,
    1: 262,
    2: 528,
    3: 729,
    4: 946,
    5: 1207,
    6: 1470,
    7: 1666,
    8: 1874,
    9: 2129,
    10: 2397,
    11: 2660,
    12: 2933,
    13: 3194,
    14: 3466,
    15: 3603,
    16: 3762,
    17: 4029,
    18: 4302,
    19: 4562,
    20: 4833,
    21: 5102,
    22: 5375,
    23: 5506,
    24: 5719,
    25: 5989,
    26: 6262,
    27: 6527,
    28: 6761,
    29: 7030,
    30: 7307,
    31: 7570,
    32: 7839,
    33: 7960,
    34: 8174,
    35: 8435,
    36: 8706,
    37: 8944,
    38: 9172,
    39: 9400,
    40: 9640,
    41: 9871,
    42: 10144,
    43: 10416,
    44: 10690,
    45: 10963,
    46: 11233,
    47: 11503,
    48: 11777,
    49: 12048,
    50: 12114,
    51: 12114,
    52: 12206,
    53: 12469,
    54: 12648,
    55: 12880,
}


def get_page_num_from_rune_num(rune_num: int) -> int:
    for page, ct in PAGE_RUNE_OFFSET.items():
        if rune_num > ct:
            return page
    return page


def get_segment_num_from_rune_num(rune_num: int) -> int:
    for seg, ct in SEGMENT_RUNE_OFFSETS.items():
        if rune_num > ct:
            return seg
    return seg


@dataclass
class Rune:
    rune: str
    rune_idx: int  # index of rune between 0-29
    rune_num: int  # 0 is the 1st rune, 1 is the 2nd rune, etc.. ignoring spaces
    letter_num: int  # The position of the letter in the word
    word: str
    word_num: int
    word_len: int
    sentence_num: int
    page_num: int
    rune_num_offset_page: int
    segment_num: int
    rune_num_offset_seg: int
    prev_rune: str = None
    is_doublet: bool = False

    def valid_match(self, mapping: dict, reversed: bool = False) -> bool:
        """
        Returns if the plaintext could be the symbol based on the input mapping

        :param mapping:
        :return:
        """
        if reversed:
            return len(mapping[self.word_len][self.letter_num]) > 0
        return len(mapping[self.word_len][self.word_len - self.letter_num - 1]) > 0

    def __repr__(self):
        return f"[Rune {self.rune}]"


class DELIMITERS:
    WORD = "-"
    CLAUSE = "."
    PARAGRAPGH = "&"
    SEGMENT = "$"
    CHAPTER = "§"
    LINE = "/\n"
    PAGE = "%"


class _Watts:
    FILEPATH = "data/watts.json"
    BAD_TEXT = [
        'ç', 'ṭ', '念', 'μ', '&', 'म', 'स', 'ा', 'ὸ', '‚', '悩', 'ś', 'σ', '”', 'ï', '/', '`', 'ō', ';', 'ą', '?',
        'ǎ', '>', 'ê', 'ξ', '爲', '=', 'ǒ', 'û', 'ö', 'ά', 'ḍ', ')', '.', '—', '(', '\xad', 'á', 'τ', 'ς', '_', '$',
        '+', 'æ', '‘', ',', 'े', 'ū', ']', 'अ', 'í', 'ò', ':', 'क', 'ñ', '–', '无', '事', 'ì', '͂', 'ú', '्', 'ἄ', '無',
        'à', 'ṣ', 'व', 'ó', '“', 'ǐ', '̥', 'ε', 'ल', 'ṃ', 'ä', 'श', 'ρ', '[', '…', 'ὁ', 'ṇ', '’', 'ἱ', 'ṛ',
        'ī', '~', '煩', 'ि', 'é', 'ā', '碍', 'ṅ', '-', 'θ', 'त', 'थ', 'ù', '!', 'ñ', 'ç', 'μ', 'û', 'à', 'ς', 'ά',
        'ê', 'τ', 'ṅ', 'é', 'æ', 'ξ', 'σ', 'ì', 'ō', 'ä', 'ā', 'θ', 'ï', 'ὁ', 'ą', 'ρ', 'á', 'ī', 'υ', 'ε', 'ú',
        'ö', 'ἄ', 'ó', 'ṛ', 'ò', 'ǐ', 'í', 'ṃ', 'ǒ', 'ὸ', 'ù', 'ṣ', 'ṭ', 'ṇ', 'ἱ', 'ǎ', 'ū', 'ś', 'ḍ'
    ]

    def __init__(self):
        with open(self.FILEPATH, "r") as f:
            self.data = json.load(f)
        self.titles = [x["title"] for x in self.data]
        self.body = [x["body"] for x in self.data]

    @property
    def text(self):
        clean_text = _LiberPrimus.remove_numbers(" ".join([x.replace("\n", " ") for x in self.body]))
        for bad_char in self.BAD_TEXT:
            clean_text = clean_text.replace(bad_char, "")
        return clean_text.upper()

    @property
    def runes(self):
        return "".join(_LiberPrimus.get_only_runes(Gematria.lat_to_run(self.text)))


class Cribs:
    MAX_CRIBS_LEN = 14

    @classmethod
    def get_words(cls, length: int) -> List[str]:
        with open(f"data/cribs/mycribs{length}.txt", "r") as f:
            data = f.read()
        return data.upper().strip().split(" ")

    @classmethod
    def get_cribs_with(cls, match_str: str):
        output = {}
        for i in range(1, cls.MAX_CRIBS_LEN+1):
            output[i] = [word for word in Cribs.get_words(i) if re.search(match_str.upper(), word)]

        return output


class _LiberPrimus:
    TEXT = None
    TAO = None
    BOOK = None
    BOOK_SECTIONS = [
        [0, 3],
        [3, 8],
        [8, 15],
        [15, 23],
        [23, 27],
        [27, 33],
        [33, 40],
        [40, 56],
    ]

    DEEP_WEB_HASH = "36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4"
    BOOK_OFFSET = 15  # The actual LiberPimus Book starts on page 15 of the `TEXT`
    UNSOLVED_SEGMENT_OFFSET = 5
    DELIM_MAP = {
        "-": " ",
        ".": " ",
        "&": "",
        "$": "",
        "": "",
        "/": "",
        "%": "",
        "\n": "",
    }

    @classmethod
    def print(cls, highlight: Optional[List[str]] = None):
        cls.load_text()
        txt = cls.TEXT
        if highlight:
            for txt_to_highlight in highlight:
                txt = txt.replace(txt_to_highlight, "\33[43m" + txt_to_highlight + "\33[0m")
        pages = txt.split(DELIMITERS.PAGE)[cls.BOOK_OFFSET:]
        for i, page in enumerate(pages):
            print(f"---- PAGE {i} ----\n{page}")

    @classmethod
    def load_text(cls):
        if cls.TEXT:
            return
        with open(os.path.join('data', LIBER_PRIMUS_FILEPATH), "r") as f:
            cls.TEXT = f.read()

        with open(os.path.join('data', TAO_FILEPATH), "r") as f:
            cls.TAO = f.read()

    def __str__(self):
        return self.TEXT

    @classmethod
    def strip_delims(cls, txt):
        for delim, new_delim in cls.DELIM_MAP.items():
            txt = txt.replace(delim, new_delim)
        return txt.strip()

    @classmethod
    def split_by(cls, delim: str) -> str:
        cls.load_text()
        # split by the specified delimiter and remove the rest
        return cls.TEXT.split(delim)

    @property
    def tao(self):
        self.load_text()
        return self.TAO

    @property
    def pages(self):
        return self.split_by(DELIMITERS.PAGE)

    @property
    def book(self):
        return [self.strip_delims(x) for x in self.pages[self.BOOK_OFFSET:-2]]

    @property
    def lines(self):
        return self.split_by(DELIMITERS.LINE)

    @property
    def chapters(self):
        return self.split_by(DELIMITERS.CHAPTER)

    @property
    def segments(self):
        return [self.strip_delims(segm) for segm in self.split_by(DELIMITERS.SEGMENT)]
        # return [segm for segm in self.split_by(DELIMITERS.SEGMENT)]

    @property
    def paragraphs(self):
        return self.split_by(DELIMITERS.PARAGRAPGH)

    @property
    def unsolved_segments(self):
        return [x for x in self.split_by(DELIMITERS.SEGMENT)][self.UNSOLVED_SEGMENT_OFFSET:]

    @property
    def unsolved_runes_with_shift(self):
        return Gematria.shift_by_previous_rune("".join(self.get_only_runes("".join(self.unsolved_segments))))

    @property
    def sentences(self):
        # returns segments split into sentences
        output = []
        for seg in self.unsolved_segments:
            new_segment = []
            for sentence in seg.split(DELIMITERS.CLAUSE):
                cleaned_sentence = self.filter_for(self.strip_delims(sentence), ALL_RUNES+" ").strip()
                if len(cleaned_sentence) > 0:
                    new_segment.append(cleaned_sentence)
            output.append(new_segment)
        return output

    @property
    def clauses(self):
        return self.split_by(DELIMITERS.CLAUSE)

    @property
    def words(self):
        return self.split_by(DELIMITERS.WORD)

    @property
    def runes(self) -> str:
        """Returns the runes only"""
        return self.TEXT

    def get_text_only(self, text: Union[str, List[str]], only_runes=False):
        """Strips delims, numbers, and spaces"""
        if isinstance(text, list):
            text = "".join(text)
        output = self.remove_numbers(self.strip_delims(text).replace(" ", ""))
        if only_runes:
            return "".join(self.get_only_runes(output))
        return output

    @classmethod
    def filter_for(cls, text: str, good_symbols):
        return "".join(cls._get_only(text, good_symbols))

    @staticmethod
    def _get_only(text: str, good_symbols: str) -> List[str]:
        return [x for x in text if x in good_symbols]

    @classmethod
    def get_only_runes(cls, text: str):
        return cls._get_only(text, ALL_RUNES)

    @classmethod
    def get_only_lat(cls, text: str):
        return "".join(cls._get_only(text.upper(), ALL_LETTERS))

    @classmethod
    def remove_numbers(cls, text: str) -> str:
        return re.sub(r"\d+", "", text).replace("\n", " ")

    def __getitem__(self, page):
        return self.book[page]


LiberPrimus = _LiberPrimus()
LiberPrimus.load_text()
AlanWatts = _Watts()


def _build_runes(sentences: List[str]) -> List[Rune]:
    output = []
    sentence_lengths = [[len(word) for word in sent.split(" ")] for sent in sentences]
    word_lengths = [item for sublist in sentence_lengths for item in sublist]

    def get_sentence_num_by_word_num(word_num):
        word_count = 0
        for sent_num, sent_lens in enumerate(sentence_lengths):
            word_count += len(sent_lens)
            if word_num < word_count:
                return sent_num

    all_runes = " ".join(sentences)
    words = all_runes.split(" ")

    idx = 0
    letter_num = 0
    word_num = 0
    sentence_num = 0
    sentence_idx = 0
    prev_rune = ''
    for rune in all_runes:
        if rune == " ":
            word_num += 1
            sentence_num = get_sentence_num_by_word_num(word_num)
            letter_num = 0
        else:
            page_num = get_page_num_from_rune_num(idx)
            seg_num = get_segment_num_from_rune_num(idx)
            output.append(
                Rune(
                    rune=rune,
                    rune_idx=Gematria.run_to_idx(rune)[0],
                    rune_num=idx,
                    letter_num=letter_num,
                    word=words[word_num],
                    word_num=word_num,
                    word_len=word_lengths[word_num],
                    sentence_num=sentence_num,
                    page_num=page_num,
                    rune_num_offset_page=PAGE_RUNE_OFFSET[page_num],
                    segment_num=seg_num,
                    rune_num_offset_seg=PAGE_RUNE_OFFSET[seg_num],
                    prev_rune=prev_rune,
                    is_doublet=rune == prev_rune,
                )
            )
            idx += 1
            letter_num += 1
            prev_rune = rune
    return output


def get_reversed_runes(runes: List[Rune]) -> List[Rune]:
    """Flips all words?"""
    raise NotImplemented


class UnsolvedLP:

    runes: List[Rune] = _build_runes([item for sublist in LiberPrimus.sentences for item in sublist])

    PAGE_40_RUNE_INDEX = 9640
    PAGE_54_RUNE_INDEX = 12648
    N_RUNES = len(runes)

    last_section_runes = runes[PAGE_40_RUNE_INDEX:]
    last_2_pages_runes = runes[PAGE_54_RUNE_INDEX:]

    @classmethod
    def get_string_from_runes(cls, runes: List[Rune]) -> str:
        output = "*" * runes[0].letter_num
        for rune in runes:
            if rune.letter_num == 0:
                output += " {}"
            else:
                output += "{}"
        # Add *s to the last word based on len
        output += "*" * (runes[-1].word_len - runes[-1].letter_num - 1)

        return output


if __name__ == "__main__":
    import sys
    from cicada.utils import sha512

    str_raw = UnsolvedLP.get_string_from_runes(UnsolvedLP.runes[2:12])
    print(str_raw)
    guesses = ['a', 'b', 'ing', 'i', 'i', 'i', 'b', 'b', 'o', 'p']
    print(str_raw.format(*guesses))

    print(UnsolvedLP.last_section_runes[:10])

    for rune in UnsolvedLP.runes:
        if rune.word == "ᛒᛠᚠᛉᛁᛗᚢᚳᛈᚻᛝᛚᛇ":
            print(
                f"{rune.rune_num}\t"
                f"{rune.rune_num - UnsolvedLP.PAGE_40_RUNE_INDEX}\t"
                f"{rune.rune_num - UnsolvedLP.PAGE_54_RUNE_INDEX}\t"
                f"{rune}"
            )

    rune_count = 0
    print("\nPage\tRunes\tStart Idx")
    for i, page in enumerate(LiberPrimus.book):
        runes = LiberPrimus.get_only_runes(page)
        print(f"{i}: {rune_count},")
        rune_count += len(runes)

    rune_count = 0
    print("\nSeg\tRunes\tStart Idx")
    for i, seg in enumerate(LiberPrimus.unsolved_segments):
        runes = LiberPrimus.get_only_runes(seg)
        print(f"{i}: {rune_count},")
        rune_count += len(runes)
