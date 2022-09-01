
import os
import re
from typing import Optional, List, Union

from cicada.gematria import ALL_RUNES, ALL_LETTERS

LIBER_PRIMUS_FILEPATH = "liber_primus.txt"
TAO_FILEPATH = "tao.txt"
UNSOLVED_LP_RUNE_LENGTH = 13170


class DELIMITERS:
    WORD = "-"
    CLAUSE = "."
    PARAGRAPGH = "&"
    SEGMENT = "$"
    CHAPTER = "§"
    LINE = "/\n"
    PAGE = "%"


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
        with open(os.path.join(os.path.dirname(__file__), LIBER_PRIMUS_FILEPATH), "r") as f:
            cls.TEXT = f.read()

        with open(os.path.join(os.path.dirname(__file__), TAO_FILEPATH), "r") as f:
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
        return [x for x in self.split_by(DELIMITERS.SEGMENT)][5:]

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
            return self.get_only_runes(output)
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
        return cls._get_only(text, ALL_LETTERS)

    @classmethod
    def remove_numbers(cls, text: str) -> str:
        return re.sub(r"\d+", "", text).replace("\n", " ")

    def __getitem__(self, page):
        return self.book[page]


LiberPrimus = _LiberPrimus()
LiberPrimus.load_text()

if __name__ == "__main__":
    import sys
    from cicada.utils import sha512

    path = sys.argv[1]
    hash = sha512(path)
    print(f"{hash == LiberPrimus.DEEP_WEB_HASH}\t{hash}")