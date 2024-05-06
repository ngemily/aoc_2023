from collections import defaultdict
from functools import reduce
from itertools import starmap
import pudb

s = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def HASH(s, init=0):
    def _(init, c):
        # Determine the ASCII code for the current character of the string.
        # Increase the current value by the ASCII code you just determined.
        # Set the current value to itself multiplied by 17.
        # Set the current value to the remainder of dividing itself by 256.
        r = init
        r = r + ord(c)
        r = r * 17
        r = r % 256

        return r

    return reduce(_, s, init)


class HASHMAP:
    d = defaultdict(list)

    def reset(self, key):
        bucket = HASH(key)

        self.d[bucket] = list(filter(lambda t: t[0] != key, self.d[bucket]))

    def set(self, key, val):
        bucket = HASH(key)

        if key in map(lambda t: t[0], self.d[bucket]):
            self.d[bucket] = list(
                map(lambda t: (key, val) if t[0] == key else t, self.d[bucket])
            )
        else:
            self.d[bucket].append((key, val))

    def verify(self):
        def _(bucket, items):
            return sum(
                starmap(
                    lambda i, value: (bucket + 1) * (i + 1) * value,
                    enumerate(map(lambda t: t[1], items)),
                )
            )

        return sum(starmap(_, self.d.items()))


def pt_1():
    with open("input.txt") as fh:
        print(sum(map(HASH, fh.readline().strip().split(","))))


def pt_2():
    with open("input.txt") as fh:
        s = fh.readline().strip()

    h = HASHMAP()
    for elem in s.split(","):
        if "=" in elem:
            key, val = elem.split("=")
            h.set(key, int(val))
        elif elem[-1] == "-":
            key = elem[:-1]
            h.reset(key)
        else:
            raise ValueError
    print(h.verify())


pt_1()  # 509784
pt_2()  # 230197
