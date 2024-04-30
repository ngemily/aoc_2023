from functools import cache

import math

ss = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


def pt_1():
    def get_score(game):
        """Return the score of the game, defined as 2 ^ (num_matches - 1)

        game (str): "41 48 83 86 17 | 83 86  6 31 17  9 48 53"
        """
        winning, mine = game.split("|")
        winning = set(winning.split())
        mine = set(mine.split())
        return int(math.pow(2, len(winning & mine) - 1))

    def get_game(line):
        """
        line (str): "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
        """
        _, game = line.split(":")
        return game

    with open("input.txt") as fh:
        return sum(map(get_score, map(get_game, fh.readlines())))


def pt_2():
    def scratch_card(card):
        card_no, game = card.split(":")
        card_no = int(card_no.split()[1])
        winning, mine = game.split("|")
        winning, mine = set(winning.split()), set(mine.split())
        return (card_no, set(range(card_no + 1, card_no + len(winning & mine) + 1)))

    def get_scratcher(scratch_map):
        # seed the 'factorial' function with the lookup table scratch_map
        @cache
        def scratch_fact(n):
            acc = 0
            for i in scratch_map.get(n, set()):
                acc = acc + 1 + scratch_fact(i)
            return acc

        return scratch_fact

    with open("input.txt") as fh:
        scratch_map = dict(map(scratch_card, fh.readlines()))
    scratch_fact = get_scratcher(scratch_map)
    total = 0
    for k in scratch_map.keys():
        total = total + scratch_fact(k)
    return total + len(scratch_map.keys())


print(pt_1())  # 25010
print(pt_2())  # 9924412
