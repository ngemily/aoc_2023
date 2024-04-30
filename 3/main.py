g = [
    "467..114.\n",
    "...*.....\n",
    "..35..633\n",
    "......#..\n",
    "617*.....\n",
    ".....+.58\n",
    "..592....\n",
    "......755\n",
    "...$.*...\n",
    ".664.598.\n",
]


def get_sym_locs(grid):
    """Return set of all points where there exists a 'symbol' in the grid.  A
    'symbol' is any non-digit character than is not a '.'.
    """
    sym_locs = set()  # of Point(x, y)
    for i, row in enumerate(grid):
        for j, elem in enumerate(row):
            if elem != "." and not elem.isdigit():
                sym_locs.add((i, j))
    return sym_locs


def get_num_map(grid):
    num_map = dict()  # (x, y) to (id, i)
    num_id = 0
    for num in next_num(grid):
        num, (x, y1, y2) = num
        for i in range(y1, y2 + 1):
            num_map[(x, i)] = (num_id, num)
        num_id = num_id + 1
    return num_map


def next_num(grid):
    """Yield next number and its bounding box

    grid [(str)]: [".234*.342..", "@866.644...", ...]
    """
    state = 0  # {0: not in a numeric area; 1: in a numeric area}
    num = ""
    for i, row in enumerate(grid):
        for j, elem in enumerate(row):
            match (state, elem):
                case (0, x) if x.isdigit():
                    num = num + elem
                    state = 1
                case (0, x) if not x.isdigit():
                    pass
                case (1, x) if x.isdigit():
                    num = num + elem
                case (1, x) if not x.isdigit():
                    yield (int(num), (i, j - len(num), j - 1))
                    num = ""
                    state = 0
        state = 0
        num = ""


def walk_enclosing_box(x, y1, y2):
    """Yield points along boundary enclosing line defined by (x, y1, y2)

    +-------+
    |p1   p2|
    +-------+
    """
    for i in range(y1 - 1, y2 + 1 + 1):
        yield (x - 1, i)  # top row
    for i in range(y1 - 1, y2 + 1 + 1):
        yield (x + 1, i)  # bottom row
    yield (x, y1 - 1)  # left edge
    yield (x, y2 + 1)  # right edge


def pt_1():
    # one pass to get symbol locations
    # second to compute total
    #
    # can optimize by doing a "parallel" look-ahead process
    # where we scan for symbols one line ahead of current line
    # (maximum distance ahead where a symbol might be that affects current outcome)
    with open("input.txt") as fh:
        sym_locs = get_sym_locs(map(lambda s: s.strip(), fh.readlines()))

    with open("input.txt") as fh:
        total = 0
        for num in next_num(fh.readlines()):
            num, (x, y1, y2) = num
            if any(map(lambda point: point in sym_locs, walk_enclosing_box(x, y1, y2))):
                total = total + num
        print(total)  # 539433


def pt_2():
    # alt. solution
    # one-pass, sliding window iterator

    with open("input.txt") as fh:
        num_map = get_num_map(fh.readlines())

    with open("input.txt") as fh:
        total = 0
        for i, row in enumerate(fh.readlines()):
            for j, elem in enumerate(row):
                if elem == "*":
                    unique_surrounding_nums = set(
                        map(
                            lambda p: num_map.get(p),
                            filter(lambda p: p in num_map, walk_enclosing_box(i, j, j)),
                        )
                    )
                    if len(unique_surrounding_nums) == 2:
                        ((_, x), (_, y)) = unique_surrounding_nums
                        total = total + x * y
        print(total)


pt_1()  # 539433
pt_2()  # 75847567
