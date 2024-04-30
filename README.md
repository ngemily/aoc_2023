# Advent of Code 2023

## Day 1

Parameterizing function `first_alpha` to achieve `last_alpha`.

```python
DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def first_alpha(s, f=min, i=str.index):
    """Find the first spelled-out digit an alpha-numeric string 's'"""
    # partial application of a member function of a class
    # (in this case, 'index', or 'rindex' of class 'str')
    index = partial(i, s)
    return f(
        map(
            lambda digit: (index(digit), digit),
            filter(lambda digit: digit in s, DIGITS),
        ),
        default=(None, None),
    )[1]

last_alpha = partial(first_alpha, f=max, i=str.rindex)
```

Pattern matching as a control structure to handle all possible scenarios: string
's' contains only numeric, only spelled out, or both numeric and spelled out
digits.

```python
DIGIT_MAP = {
    "one"   : "1",
    "two"   : "2",
    "three" : "3",
    "four"  : "4",
    "five"  : "5",
    "six"   : "6",
    "seven" : "7",
    "eight" : "8",
    "nine"  : "9",
}

match first_alpha(s), first_num(s):
    case (x, None):
        first_digit = DIGIT_MAP.get(x)
    case (None, y):
        first_digit = y
    case (x, y):
        first_digit = DIGIT_MAP.get(x) if s.index(x) < s.index(y) else y

```
## Day 2

Parsing with structural pattern matching.

```python
def parse_draw(draw):
    """Parse draw string for number of red, green, and blue cubes.

    draw (str): e.g. "3 blue, 4 red"
    Returns: (r, g, b) number of red, green, blue cubes
    """
    red, green, blue = (0, 0, 0)
    for draw in map(lambda s: s.split(), draw.split(",")):
        match draw:
            case [n, "red"]:
                red = int(n)
            case [n, "green"]:
                green = int(n)
            case [n, "blue"]:
                blue = int(n)
    return (red, green, blue)

```
## Day 3

Implementing a finite-state-machine using structural pattern matching.

```python
def next_num(grid):
    """Yield next number and its bounding box

    grid [(str)]: [".234*.342..", "@866.644...", ...]
    """
    state = 0  # {0: not in a numeric area; 1: in a numeric area}
    num = ""
    for i, row in enumerate(grid):
        for j, elem in enumerate(row + "."):
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
```
