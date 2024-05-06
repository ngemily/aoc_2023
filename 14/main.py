from itertools import batched, starmap
from functools import partial, reduce
from enum import StrEnum

from toolz.recipes import partitionby

ss = [
    "############",
    "#O....#....#",
    "#O.OO#....##",
    "#.....##...#",
    "#OO.#O....O#",
    "#.O.....O#.#",
    "#O.#..O.#.##",
    "#..O..#O..O#",
    "#.......O..#",
    "##....###..#",
    "##OO..#....#",
    "############",
]


class Rock(StrEnum):
    ROUND = "O"
    SQUARE = "#"
    BLANK = "."


class Grid:
    _grid = []

    def __init__(self, g):
        _ = map(partial(map, Rock), g)
        self._grid = list(map(list, _))
        self.rotate_90()
        self.rotate_90()
        self.rotate_90()

    def __repr__(self):
        return "\n".join(map("".join, self._grid))

    def __hash__(self):
        return hash(repr(self))

    def tilt(self):
        def _(row):
            return reduce(
                lambda acc, l: acc + l,
                starmap(
                    lambda anchor, rest=[]: [*anchor]
                    + [Rock.ROUND] * rest.count(Rock.ROUND)
                    + [Rock.BLANK] * rest.count(Rock.BLANK),
                    batched(partitionby(lambda elem: elem == Rock.SQUARE, row), 2),
                ),
                [],
            )

        self._grid = list(map(_, self._grid))

    def rotate_90(self):
        self._grid = list(map(list, map(reversed, zip(*self._grid))))

    def cycle(self):
        """Tilt the board in a cycle of the cardinal directions: N, W, S, E"""
        for _ in range(4):
            self.tilt()
            self.rotate_90()

    def calculate_load(self):
        def _(row):
            return sum(
                starmap(
                    lambda i, elem: i if elem == Rock.ROUND else 0,
                    enumerate(reversed(row)),
                ),
            )

        return sum(map(_, self._grid))


def pt_1():
    with open("input.txt") as fh:
        g = Grid(map(lambda s: s.strip(), fh))
        g.tilt()
        print(g.calculate_load())


def pt_2():
    N = 1_000_000_000
    with open("input.txt") as fh:
        g = Grid(map(lambda s: s.strip(), fh))
        # At some point, the rock pattern starts to cycle in a loop.
        seen = []
        idx = []
        # Find the first instance we enter the loop, and its length.
        for i in range(N):
            gid = hash(g)
            if gid in seen:
                x = seen.index(gid)
                print(f"{i}: Found at {seen.index(gid)}")
                if x in idx:
                    break
                else:
                    idx.append(x)
            else:
                seen.append(gid)
            g.cycle()
        print(idx)
        # Advance the board to the state it would be after N iterations.
        # (alt. keep track of load for each state in the cycle)
        for _ in range((N - idx[0]) % len(idx)):
            g.cycle()
        # Find the load on the north beam.
        print(g.calculate_load())


pt_1()  # 109665
pt_2()  # 96061
