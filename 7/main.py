from enum import Enum
from functools import reduce
from typing import ClassVar
from itertools import starmap
from dataclasses import dataclass


@dataclass
class Card:
    card_value: ClassVar[dict] = {
        "A": 1,
        "K": 2,
        "Q": 3,
        "J": 4,
        "T": 5,
        "9": 6,
        "8": 7,
        "7": 8,
        "6": 9,
        "5": 10,
        "4": 11,
        "3": 12,
        "2": 13,
    }

    value: str

    def __lt__(self, other):
        return self.card_value[self.value] < self.card_value[other.value]


@dataclass
class Hand:
    class Type(Enum):
        FIVE_OF_A_KIND = 1
        FOUR_OF_A_KIND = 2
        FULL_HOUSE = 3
        THREE_OF_A_KIND = 4
        TWO_PAIR = 5
        ONE_PAIR = 6
        HIGH_CARD = 7

    cards: str
    type: Type
    bid: int

    def __init__(self, cards: str, bid: int):
        """Determine the type of the hand by looking at the cards"""

        wildcards = cards.count("J")
        cards = cards.replace("J", "")

        counts = list(map(lambda c: cards.count(c), set(cards)))
        frequencies = {elem: counts.count(elem) for elem in counts}

        match frequencies:
            case {5: 1}:
                hand_type = Hand.Type.FIVE_OF_A_KIND
            case {4: 1}:
                hand_type = Hand.Type.FOUR_OF_A_KIND
            case {3: 1, 2: 1}:
                hand_type = Hand.Type.FULL_HOUSE
            case {3: 1}:
                hand_type = Hand.Type.THREE_OF_A_KIND
            case {2: 2}:
                hand_type = Hand.Type.TWO_PAIR
            case {2: 1}:
                hand_type = Hand.Type.ONE_PAIR
            case _:
                hand_type = Hand.Type.HIGH_CARD

        self.cards = cards
        self.bid = bid
        self.type = hand_type

    def __lt__(self, other):
        match (self, other):
            case (self, other) if self.type.value != other.type.value:
                return self.type.value > other.type.value
            case (self, other) if self.type.value == other.type.value:
                # compare cards where
                # A > K > Q > J > T > 9 > ... > 2
                for x, y in zip(self.cards, other.cards):
                    if x != y:
                        return Card(x) > Card(y)


ss = [
    "AAAAA 765",  # 5-of-a-kind
    "AAAA2 765",  # 4-of-a-kind
    "AAA22 765",  # full house
    "AAKK2 765",  # two pair
    "AA432 765",  # one pair
    "A5432 765",  # high card
]
ss = [
    "AAAAA 0",  # test card ordering
    "KKKKK 0",
    "QQQQQ 0",
    "JJJJJ 0",
    "TTTTT 0",
    "99999 0",
    "22222 0",
]
ss = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28 ",
    "KTJJT 220",
    "QQQJA 483",
]

def pt_1():
    with open("input.txt") as fh:
        hands = starmap(
            lambda cards, bid: Hand(cards, int(bid)), map(lambda s: s.split(), fh)
        )
        winnings = reduce(
            # t = (rank, hand)
            lambda acc, t: acc + (t[0] + 1) * t[1].bid, enumerate(sorted(hands)), 0
        )
    print(winnings)

pt_1()  # 256448566
