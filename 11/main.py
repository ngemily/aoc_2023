from itertools import combinations, pairwise, starmap
from collections import UserDict
from dataclasses import dataclass


class RangeDict(UserDict):
    """Dictionary of range object to value."""

    def get(self, key, default=None):
        if not any(map(lambda rng: key in rng, self.keys())):
            return default
        for rng, v in self.items():
            if key in rng:
                return v
        return default


@dataclass
class Point:
    x: int
    y: int


ss = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]


def explore(universe, expansion_factor=1):
    """Return total distance between each pair of galaxies in universe where
    each row or column with no galaxy is expanded by factor e.

    universe: [str]
    """
    N = len(universe[0])
    exp_rows = [i for i, row in enumerate(universe) if "#" not in row]
    exp_cols = [i for i, col in enumerate(zip(*universe)) if "#" not in col]

    row_exp_map = RangeDict(
        {
            range(r1, r2): i * (expansion_factor - 1)
            for i, (r1, r2) in enumerate(pairwise([0] + exp_rows + [N]))
        }
    )
    col_exp_map = RangeDict(
        {
            range(c1, c2): i * (expansion_factor - 1)
            for i, (c1, c2) in enumerate(pairwise([0] + exp_cols + [N]))
        }
    )

    galaxies = [
        Point(i + row_exp_map.get(i), j + col_exp_map.get(j))
        for i, row in enumerate(universe)
        for j, elem in enumerate(row)
        if elem == "#"
    ]

    return sum(
        starmap(
            lambda p1, p2: abs(p1.x - p2.x) + abs(p1.y - p2.y),
            combinations(galaxies, 2),
        )
    )


def pt_1():
    with open("input.txt") as fh:
        universe = list(map(lambda s: s.strip(), fh))
    print(explore(universe, expansion_factor=2))


def pt_2():
    with open("input.txt") as fh:
        universe = list(map(lambda s: s.strip(), fh))
    print(explore(universe, expansion_factor=1_000_000))



print(explore(universe=ss, expansion_factor=2))
print(explore(universe=ss, expansion_factor=10))
print(explore(universe=ss, expansion_factor=100))
pt_1()  # 9623138
pt_2()  # 726820169514
