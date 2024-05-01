ss = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]

times = map(int, ss[0].split(":")[1].split())
dists = map(int, ss[1].split(":")[1].split())


# d: distance boat will travel during race
# T: total time for race
# a: duration button held, positive integer in interval (0, T)
#
# then, distance traveled given by:
#     d = (T - a) a
# 
# we wish to beat the record, i.e. have the boat travel farther than D
# mathematically,
#     d - D > 0
#
# substituting our equation for d
#     ((T - a) a) - D > 0
#     a^2 + aT + D <= 0
#
# => solve for zeroes, get distance between them along x-axis for number of ways
# we can win the race


def pt_1():
    with open("input.txt") as fh:
        times = map(int, fh.readline().split(":")[1].split())
        dists = map(int, fh.readline().split(":")[1].split())

    r = 1
    for time, dist in zip(times, dists):
        f = lambda a: (time - a) * a
        g = lambda d: d > dist
        r = r * sum(map(g, map(f, range(1, time))))
    return r

def pt_2():
    with open("input.txt") as fh:
        times = fh.readline().split(":")[1].split()
        dists = fh.readline().split(":")[1].split()

    time = int("".join(times))
    dist = int("".join(dists))

    f = lambda a: (time - a) * a
    g = lambda d: d > dist
    return sum(map(g, map(f, range(1, time))))

print(pt_1())  # 140220
print(pt_2())  # 39570185
