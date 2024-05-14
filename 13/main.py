from itertools import starmap, chain
from functools import partial

import operator


def is_symmetric_pt1(l):
    """Returns index at which `l` is symmetric, `None` if not symmetric"""

    def is_symmetric_about(l, i):
        lh = iter(reversed(l[:i]))
        rh = iter(l[i:])
        # special case of pt2 where num_sumdges is 0
        return all(starmap(operator.eq, zip(lh, rh)))

    for i in range(1, len(l)):
        if is_symmetric_about(l, i):
            return i
    return None


def is_symmetric_pt2(l, num_smudges=0):
    """Returns index at which `l` is symmetric, `None` if not symmetric

    Specifying `num_smudges` allows exactly that number of mismatches when
    considering symmetry.
    """

    def is_symmetric_about(l, i):
        lh = iter(reversed(l[:i]))
        rh = iter(l[i:])

        return (
            list(
                starmap(
                    operator.eq,
                    zip(chain.from_iterable(lh), chain.from_iterable(rh)),
                )
            ).count(False)
            == num_smudges
        )

    for i in range(1, len(l)):
        if is_symmetric_about(l, i):
            return i
    return None


def check_symmetry(g, is_symmetric):
    if x := is_symmetric(g):
        return x * 100
    elif x := is_symmetric(list(zip(*g))):
        return x
    else:
        return 0


def chunker(it):
    chunk = list()
    for line in map(lambda s: s.strip(), it):
        if line == "":
            yield chunk
            chunk.clear()
        else:
            chunk.append(line)


def pt_1():
    with open("input.txt") as fh:
        return sum(
            map(partial(check_symmetry, is_symmetric=is_symmetric_pt1), chunker(fh))
        )


def pt_2():
    with open("input.txt") as fh:
        return sum(
            map(
                partial(
                    check_symmetry,
                    is_symmetric=partial(is_symmetric_pt2, num_smudges=1),
                ),
                chunker(fh),
            )
        )


print(pt_1())  # 27300
print(pt_2())  # 29276
