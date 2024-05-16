# Advent of Code 2023

Notes on programming style

- use of 'let-over-lambda' style programming
- structural pattern matching
- `itertools.starmap` for when instead of 1-to-1 mappings, we get 1-to-n (n > 1)
    mappings, usually handled with lambda functions that take more than one
    variable

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
## Day 4

A spin on the factorial function, where instead of being computed the value of
`fact(n)` is given discretely.

Wrapping the `scratch_fact` function allows us to perform a closure over
`scratch_map`, which allows it to be compiled for any given starting set of
scratch cards (or discrete function `fact(n)`).

```python
def get_scratcher(scratch_map):
    # seed the 'factorial' function with the lookup table scratch_map
    @cache
    def scratch_fact(n):
        acc = 0
        for i in scratch_map.get(n, set()):
            acc = acc + 1 + scratch_fact(i)
        return acc

    return scratch_fact
```

## Day 19

Recursive generators
```python
def walk(part, it):
    cond, dst = next(it)
    while not cond(part):
        cond, dst = next(it)
    yield dst
    yield from walk(part, iter(d[dst]))
```

# Day 20

Decorating functions without `@` syntactic sugar.

I first implemented the pulse broadcasting without trying to count the number of
high and low pulses.  I wanted to see if I could instrument the code with
minimal impact to the core logic.

In the following example, function `foo` is bound to an incrementing counter.
```python
def get_counter():
    count = 0
    def counter():
        nonlocal count
        count = count + 1
        return count
    return counter

def counted(f):
    counter =  get_counter()
    def _(*args, **kwargs):
        counter()  # <----- how can this be accessed
        return f(*args, **kwargs)
    return _

@counted
def foo():
    pass

foo()
foo()
foo()
```

But it is bound to exactly one counter for the duration of the program.  In our
case, we wish to reset the counter at each button press.

```python
foo1 = counted(foo)
foo1()
foo1()
foo1()
foo2 = counted(foo)
foo2()
foo2()
foo2()
```

Now we have two running counts, one for each explicitly (rather than implicitly
as before) wrapped instance of `foo`.

In the code I ended up writing, I "wrapped" the functions inline; this makes it
quite clear that the wrappers are acting on the callable functions, which are
still called with the same arguments as before.  E.g. `counted` modifies the
function `process_pulse` in some way.  See [day 20](20/main.py) for full
implementation.

```python
for dst, pulse in counted(process_pulse, pc)(dst, pulse):
    q.append((dst, pulse))
# ...
lo, hi = count(broadcast_pulse)("broadcaster", False)
```

As to how to retrieve the value from our counter, it depends on whether we want
the return value of our wrapped function and where our wrapped function might be
called from.

```python
# don't return the internal function's return value
def counted(f):
    counter =  get_counter()
    def _(*args, **kwargs):
        counter()
        f(*args, **kwargs)
        return counter
    return _

# return both the counter and the internal function's return value
def counted(f):
    counter =  get_counter()
    def _(*args, **kwargs):
        counter()
        return counter, f(*args, **kwargs)
    return _

# accept the counter as an argument
# caller is responsible for maintaining a reference to counter to later retrieve
# its value
def counted(f, counter):
    def _(*args, **kwargs):
        counter()
        return f(*args, **kwargs)
    return _

```

For example, in this puzzle we still need to perform the whole activity of
propagating pulses, but what we're interested in is the measurement of a
side-effect.

```python
# Don't need the return value of `broadcast_pulse`,
# but it does things that we want to observe,
# and want we want is returned by calling `count(broadcast_pulse(...))`.
lo, hi = count(broadcast_pulse)("broadcaster", False)
```
