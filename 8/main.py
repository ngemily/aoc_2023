from itertools import cycle
from functools import partial

import re
import math


def cycler(cycle_map, cycle_pattern):
    """Return a `find_cycle_length` function initialized with a cycle map and
    cycle pattern
    """

    def find_cycle_length(start="AAA", end="ZZZ"):
        """Find the cycle length; the number of steps it takes to get from
        `start` to `end`.  `end` may also be a condition to be evaluated on a
        symbol, passed as a lambda of signature (str) -> (bool)

        start (str): start symbol
        end (str | lambda str -> bool): end symbol or condition

        Returns (int) number of steps from start to end given cycle map and pattern
        """
        curr = start
        for i, c in enumerate(cycle(cycle_pattern)):
            curr = cycle_map[curr][c]
            if isinstance(end, str):
                if curr == end:
                    break
            else:
                if end(curr):
                    break
        return i + 1

    return find_cycle_length


with open("input.txt") as fh:
    cycle_pattern = fh.readline().strip()
    next(fh)

    cycle_map = {}
    for line in fh:
        curr, left, right = re.findall(r"\w+", line)
        cycle_map[curr] = {"L": left, "R": right}


def pt_1():
    return cycler(cycle_map, cycle_pattern)()


def pt_2():
    start_syms = [elem for elem in cycle_map.keys() if elem[-1] == "A"]
    cycle_lens = list(
        map(
            partial(cycler(cycle_map, cycle_pattern), end=lambda s: s[-1] == "Z"),
            start_syms,
        )
    )
    return math.lcm(*cycle_lens)


print(pt_1())  # 19951
print(pt_2())  # 16342438708751
