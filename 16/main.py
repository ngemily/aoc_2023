from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum
from functools import partial
from multiprocessing import Pool

import sys


class TileType(StrEnum):
    MIRROR_L = "/"
    MIRROR_R = "\\"
    SPLIT_H = "-"
    SPLIT_V = "|"
    NONE = "."


@dataclass
class Tile:
    _type: str
    energized: bool = False


class Board:
    _board = []

    def __init__(self, stream):
        _ = map(partial(map, Tile), stream)
        self._board = list(map(list, _))

    def __repr__(self):
        _ = lambda row: map(lambda tile: "#" if tile.energized else tile._type, row)
        return "\n".join(map("".join, map(_, self._board)))

    def energized(self):
        _ = lambda row: sum(map(lambda tile: tile.energized, row))
        return sum(map(_, self._board))

    def __len__(self):
        return len(self._board)

    def __getitem__(self, index):
        return self._board.__getitem__(index)


def get_game(board):
    visited = set()
    N = len(board)

    def adv_beam(x, y, d="E"):
        nonlocal visited

        if x < 0 or y < 0:
            return
        if x >= N or y >= N:
            return
        if (x, y, d) in visited:
            return

        tile = board[x][y]

        tile.energized = True
        visited.add((x, y, d))

        match tile._type, d:
            case "\\", _:
                d = {
                    "E": "S",
                    "S": "E",
                    "N": "W",
                    "W": "N",
                }.get(d)
            case "/", _:
                d = {
                    "E": "N",
                    "N": "E",
                    "S": "W",
                    "W": "S",
                }.get(d)
            case "|", _ if d in {"E", "W"}:
                adv_beam(x - 1, y, "N")
                adv_beam(x + 1, y, "S")
                return
            case "-", _ if d in {"N", "S"}:
                adv_beam(x, y + 1, "E")
                adv_beam(x, y - 1, "W")
                return
            case "|", _ if d in {"N", "S"}:
                pass
            case "-", _ if d in {"E", "W"}:
                pass
            case _:
                pass

        match d:
            case "N":
                adv_beam(x - 1, y, d)
            case "E":
                adv_beam(x, y + 1, d)
            case "S":
                adv_beam(x + 1, y, d)
            case "W":
                adv_beam(x, y - 1, d)

    return adv_beam


def pt_1():
    with open("input.txt") as fh:
        board = Board(map(lambda s: s.strip(), fh))
    play = get_game(board)
    play(0, 0, "E")
    return board.energized()


def pt_2():
    with open("input.txt") as fh:
        board = Board(map(lambda s: s.strip(), fh))

    N = len(board)
    boards = [deepcopy(board) for _ in range(4 * N)]
    games = list(map(get_game, boards))
    # fmt: off
    args = (
          [(  i,   0, "E") for i in range(N)]
        + [(  0,   i, "S") for i in range(N)]
        + [(  i, N-1, "W") for i in range(N)]
        + [(N-1,   i, "N") for i in range(N)]
    )
    # fmt: on
    # can't pickle for parallel...
    for game, args in zip(games, args):
        game(*args)
    return max(map(lambda board: board.energized(), boards))


sys.setrecursionlimit(10000)
print(pt_1())  # 7472
print(pt_2())  # 7716
