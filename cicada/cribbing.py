
import itertools
from dataclasses import dataclass
from typing import List, Dict

from cicada.liberprimus import LiberPrimus, Cribs


@dataclass
class CribSetup:
    section: int
    runes: str
    cribs: List[str]
    prev_rune_idx: int = None
    next_rune_idx: int = None  # For using a key in reverse

    def __repr__(self):
        return f"[CribSetup] section={self.section},runes={self.runes[:15]}, cribs({len(self.cribs)})={self.cribs[:2]}"


section_1_2words = ["the", "to"]  # "as at be by do go in is it my no of on the to up we".split(" ")


"""
Page 0	[8, 5]
Page 3	[2, 11, 3]
Page 4	[3]
Page 6	[4, 1, 4, 2]
Page 7	[2, 4, 3, 2, 3]
Page 8	[4, 8]
Page 15	[4, 5]
Page 16	[4, 2, 5]
Page 23	[2, 6, 3, 5]
Page 27	[3, 12, 4]
Page 33	[2, 8]
Page 34	[3, 5]
Page 39	[3]
Page 40	[3, 5]
Page 53	[5, 4, 4, 11, 2, 3, 2, 6, 5, 5, 2, 2]
Page 54	[1, 8]

12: SEPARATENESS,CONSCIOUSNESS,SEPARATENESS,NONEXISTENCE,MATERIALISTIC,IMPERMANENCE

"""
RED_RUNES = {
    0: ["ᛋᚻᛖᚩᚷᛗᛡᚠ", "ᛋᚣᛖᛝᚳ"],
    3: ["ᛚᛂ", "ᛇᚻᛝᚳᚦᛏᚫᛂᛏᛉᚻ", "ᛏᚢᛟ"],
    4: ["ᛈᛞᚦ"],
    6: ["ᚪᛏᛉᛒ", "ᛗ", "ᚷᛡᛋᛒ", "ᛉᛇ"],
    7: ["ᛞᚩ", "ᛟᛏᚦᚫ", "ᚳᚹᛂ", "ᛉᛠ", "ᚷᛠᛗ"],
    8: ["ᛉᛁᛉᛗ", "ᚢᛉᛗᚳᚦᛈᚩᛒ"],
    15: ["ᚠᚢᛚᛗ", "ᚪᛠᚣᛟᚪ"],
    16: ["ᛚᚢᛝᚾ", "ᚳᚢ", "ᛒᚾᛏᚠᛝ"],  # Page 15 - 2nd half
    23: ["ᚢᚪ", "ᚹᛝᚷᛉᛞᚷ", "ᛁᛒᛁ", "ᛇᛏᛒᛁᚣ"],
    27: ["ᛗᛈᚣ", "ᛚᛋᚩᚪᚫᚻᛚᛖᛇᛁᛗᛚ", "ᛚᛋᚳᛈ"],
    33: ["ᛞᛇ", "ᛉᚳᚠᛁᚪᚹᚻᚷ"],
    34: ["ᛝᚦᛇ", "ᛁᚠᚳᛟᛇ"],  # Page 33 - 2nd half
    39: ["ᛡᚳᛋ"],
    40: ["ᚠᚾᛗ", "ᚣᚷᛞᚫᚻ"],
    53: ["ᛏᛈᚹᛇᛋ", "ᚹᛒᛇᚦ", "ᚾᚻᚷᛂ", "ᚱᛡᛞᛡᚦᚪᛁᛇᚫᛉᛚ", "ᛇᛠ", "ᛡᚪᛂ", "ᚻᚱ", "ᚦᛈᛞᛂᛝᚩ", "ᚷᚠᛇᛗᚳ", "ᚻᛞᚩᛏᚳ", "ᚢᚱ", "ᛈᚾ"],
    54: ["ᚪ", "ᛗᛝᛞᛡᚦᛉᛁᛗ"],
}

# Key is "BUTTER MY TOAST"
TEST_CRIB = CribSetup(0, "ᛝᛗᚷᚱᚫᚦᛗᛟᚹᛇᚪᚹᛠᛚᛠᛋᚾᛟ", ["COSMICCONSCIOUSNESS"], prev_rune_idx=0, next_rune_idx=0)

WITHINTHEDECEPTION_CRIBS: List[CribSetup] = [
    # Is an illusion
    CribSetup(2, "ᛝᛗᚠᚱᛡᚪᛋᛠᛗᛝᛉᛉᛇᛞᛒ", ["WITHINTHEDECEPTION"], prev_rune_idx=9, next_rune_idx=22),
    CribSetup(136, "ᚷᛚᚣᚹᛟᚠᚢᛉᚠᚫᛞᚠᛡᛄᚾ", ["WITHINTHEDECEPTION"], prev_rune_idx=27, next_rune_idx=8),
    CribSetup(145, "ᛗᚩᚷᛞᚷᛚᚳᛒᚣᛋᚣᚠᛞᚣᛝ", ["WITHINTHEDECEPTION"], prev_rune_idx=5, next_rune_idx=28),
]

ISANILLUSION_CRIBS: List[CribSetup] = [
    # Is an illusion
    CribSetup(7, "ᚹᛋᚾᛞᚳᛈᚦᛉᛈᛠᛠ", ["ISANILLUSION"], prev_rune_idx=6, next_rune_idx=7),
    CribSetup(57, "ᚫᛈᛏᚠᛖᛏᚷᚾᚠᛁᚠ", ["ISANILLUSION"], prev_rune_idx=24, next_rune_idx=4),
    CribSetup(91, "ᛖᚳᛖᛇᚷᚻᛗᛞᚪᛈᛖ", ["ISANILLUSION"], prev_rune_idx=19, next_rune_idx=19),
    CribSetup(138, "ᚠᛟᛇᚷᛄᛟᛇᚫᛋᚫᚣ", ["ISANILLUSION"], prev_rune_idx=4, next_rune_idx=17),
    CribSetup(147, "ᚹᚩᛝᛖᛒᚪᛗᛏᚪᚷᛒ", ["ISANILLUSION"], prev_rune_idx=26, next_rune_idx=13),
]

BECAUSEWEBELIEVE_CRIBS: List[CribSetup] = [
    # Because we believe
    CribSetup(2, "ᚫᛋᚣᚢᚻᚱᛏᚻᚳᛋᛟᛏᛟᛝᚢᚱ", ["BECAUSEWEBELIEVE"], prev_rune_idx=16, next_rune_idx=15),
    CribSetup(8, "ᛞᛒᛄᛡᛟᛗᛁᚠᛏᛄᛞᛁᚦᚱᛚᛋ", ["BECAUSEWEBELIEVE"], prev_rune_idx=4, next_rune_idx=18),
]

THEDIVINITYWITHIN_CRIBS: List[CribSetup] = [
    # The Divinity Within
    CribSetup(21, "ᚪᚢᛞᚻᚳᚹᛚᛡᛞᛇᛟᚩᛡᛚᚳ", ["THEDIVINITYWITHIN"], prev_rune_idx=20, next_rune_idx=27),
    CribSetup(32, "ᛖᚾᚾᚹᚷᚢᛚᚪᚩᚣᚢᛏᚠᛄᛏ", ["THEDIVINITYWITHIN"], prev_rune_idx=22, next_rune_idx=24),
    CribSetup(35, "ᚦᚦᛁᚫᛚᛋᛝᛄᛄᛡᛟᚻᛇᚢᛚ", ["THEDIVINITYWITHIN"], prev_rune_idx=17, next_rune_idx=10),
]

CIRCUMFERENCE_CRIBS: List[CribSetup] = [
    # Circumference / Enlightenment
    CribSetup(167, "ᚹᚱᛒᛠᚠᛉᛁᛗᚢᚳᛈᚻᛝᛚᛇ", ["THECIRCUMFERENCE"], prev_rune_idx=1, next_rune_idx=19),
    CribSetup(15, "ᛉᛗᛒᚩᛠᛈᛖᛞᚪᚫᛏᚩᛠᛖᛠᛉᚳᛠᛏ", ["ATTAINENLIGHTENMENT"], prev_rune_idx=21, next_rune_idx=3),
    CribSetup(11, "ᛇᛈᛋᚢᛚᚪᛈᚢᚳᛖᚠᛞᛉ", ["CIRCUMFERENCE", "ENLIGHTENMENT"], prev_rune_idx=7, next_rune_idx=2),
    CribSetup(13, "ᛒᚷᛞᛉᛗᛒᛉᚳᛝᚦᚣᛞᚫᛠ", ["CIRCUMFERENCES", "RESPONSIBILITY", "INDESTRUCTIBLE", "ACCOMPLISHMENT"], prev_rune_idx=4, next_rune_idx=15),
    CribSetup(16, "ᛖᛞᚪᚫᛏᚩᛠᛖᛠᛉᚳᛠᛏ", ["CIRCUMFERENCE"], prev_rune_idx=13, next_rune_idx=3),
    CribSetup(25, "ᛠᛁᛡᚦᛝᚾᛖᚾᚠᚩᛗᛖᚣᚪ", ["CIRCUMFERENCES", "RESPONSIBILITY", "INDESTRUCTIBLE", "ACCOMPLISHMENT"], prev_rune_idx=0, next_rune_idx=5),
    CribSetup(43, "ᛏᚠᛄᚱᚹᚠᛋᚾᚹᛄᛖᛒᚢᚦ", ["CIRCUMFERENCES", "RESPONSIBILITY", "INDESTRUCTIBLE", "ACCOMPLISHMENT"], prev_rune_idx=0, next_rune_idx=3),
    CribSetup(52, "ᛈᚳᛇᚢᛏᚳᛡᛇᛝᚾᚢᚻᚦ", ["CIRCUMFERENCE", "ENLIGHTENMENT"], prev_rune_idx=21, next_rune_idx=26),
    # last page. 13 letters. offsets from start, section start, page 54 start = 12903	3263	255
    CribSetup(55, "ᛒᛠᚠᛉᛁᛗᚢᚳᛈᚻᛝᛚᛇ", ["CIRCUMFERENCE", "ENLIGHTENMENT"], prev_rune_idx=4, next_rune_idx=19),

]

CONSCIOUSNESS_CRIBS: List[CribSetup] = [
    # doublet - 12,5 CONSCIOUSNESS [4, 6, 12, 1, 9]
    # ᛡᛠᛡᛁ ᚩᛒᚱᚾᛚᛠ ᚱᛚᛚᛖᛒᚹᚾᚻᛗᚠᛟᛒ ᛝ ᚱᚪᛡᚷᛟᛇᛏᛗᛉ
    CribSetup(1, "ᚱᛚᛚᛖᛒᚹᚾᚻᛗᚠᛟᛒ", ["CONSCIOUSNESS"], prev_rune_idx=28, next_rune_idx=21),
    CribSetup(1, "ᚩᛒᚱᚾᛚᛠᚱᛚᛚᛖᛒᚹᚾᚻᛗᚠᛟᛒ", ["COSMICCONSCIOUSNESS", "NORMALCONSCIOUSNESS"], prev_rune_idx=10, next_rune_idx=21),
]


RED_RUNE_CRIBS: List[CribSetup] = [
    # Red Runes
    CribSetup(33, "".join(RED_RUNES[33]), [
        "THEUNIVERSE", "THEDECEPTION", "THEDIRECTION",
        "THEGUIDANCE", "THEPHYSICAL",
        "THESITUATION", "THEPROBLEMS",
    ]),
    CribSetup(54, "".join(RED_RUNES[54]), [
        "ACONDITION", "ADECEPTION", "AREMINDER",
        "ADIRECTION", "ADIVINITY", "AGUIDANCE",
        "APRACTICE", "ASTRATEGY", "ACHALLENGE",
        "ASENSATION", "AVIBRATION"
    ]),
]

REASONABLE_GUESSES: List[CribSetup] = \
    CONSCIOUSNESS_CRIBS + CIRCUMFERENCE_CRIBS + ISANILLUSION_CRIBS + BECAUSEWEBELIEVE_CRIBS + THEDIVINITYWITHIN_CRIBS


_CRIB_GUESSES = {
    # Starts with 8-5:
    0: Cribs.get_words(8),
    # 2-11-3:
    1: [x.upper() + y for x, y in itertools.product(section_1_2words, Cribs.get_words(11))],
    # 4-8-3-2-3-
    2: [],
    # 4-5. ::: 4-2-5:
    3: [],
    # 3-6-3-5:
    4: [],
    # 2-6-3-5
    5: [],
    # 3-12-4:
    6: [],
    # 3-5-5-4-3-5-4:
    7: [],
}


_CRIB_GUESSES_END = {
    # Ends with :9-2-10-2-2 (reverse order, last word is 9)
    0: [x[::-1] for x in Cribs.get_words(9)],
    #
    1: [],
    #
    2: [],
    #
    3: [],
    #
    4: [],
    #
    5: [],
    #
    6: [],
    #
    7: [],
}

# Because the cipher has a memory we have to crib from the start of a section
CribConfigs: Dict[int, CribSetup] = {
    0: CribSetup(0, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[0])), _CRIB_GUESSES[0]),
    1: CribSetup(1, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[1])), _CRIB_GUESSES[1]),
    2: CribSetup(2, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[2])), _CRIB_GUESSES[2]),
    3: CribSetup(3, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[3])), _CRIB_GUESSES[3]),
    4: CribSetup(4, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[4])), _CRIB_GUESSES[4]),
    5: CribSetup(5, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[5])), _CRIB_GUESSES[5]),
    6: CribSetup(6, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[6])), _CRIB_GUESSES[6]),
    7: CribSetup(7, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[7])), _CRIB_GUESSES[7]),
}

CribConfigsEnding: Dict[int, CribSetup] = {
    0: CribSetup(0, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[0]))[::-1], _CRIB_GUESSES_END[0]),
    1: CribSetup(1, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[1]))[::-1], _CRIB_GUESSES_END[1]),
    2: CribSetup(2, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[2]))[::-1], _CRIB_GUESSES_END[2]),
    3: CribSetup(3, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[3]))[::-1], _CRIB_GUESSES_END[3]),
    4: CribSetup(4, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[4]))[::-1], _CRIB_GUESSES_END[4]),
    5: CribSetup(5, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[5]))[::-1], _CRIB_GUESSES_END[5]),
    6: CribSetup(6, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[6]))[::-1], _CRIB_GUESSES_END[6]),
    7: CribSetup(7, "".join(LiberPrimus.get_only_runes(LiberPrimus.unsolved_segments[7]))[::-1], _CRIB_GUESSES_END[7]),
}

if __name__ == "__main__":
    for k, v in RED_RUNES.items():
        print(f"Page {k}\t{[len(word) for word in v]}")
