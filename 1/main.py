from functools import partial


def pt_1():
    def get_calibration_value(s):
        """
        s = "pqr3stu8vwx"
        >>> 38
        """

        def first_digit(s):
            """Find the first numeric digit an alpha-numeric string 's'"""
            for c in s:
                if c.isdigit():
                    return c

            return ""

        return int(first_digit(s) + first_digit(reversed(s)))

    with open("input.txt") as fh:
        print(sum(map(get_calibration_value, map(lambda s: s.strip(), fh.readlines()))))


DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

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

def pt_2():
    def get_calibration_value(s):
        def first_num(s):
            """Find the first numeric digit an alpha-numeric string 's'"""
            for c in s:
                if c.isdigit():
                    return c

            return None

        def last_num(s):
            return first_num(reversed(s))

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

        match first_alpha(s), first_num(s):
            case (x, None):
                first_digit = DIGIT_MAP.get(x)
            case (None, y):
                first_digit = y
            case (x, y):
                first_digit = DIGIT_MAP.get(x) if s.index(x) < s.index(y) else y

        match last_alpha(s), last_num(s):
            case (x, None):
                last_digit = DIGIT_MAP.get(x)
            case (None, y):
                last_digit = y
            case (x, y):
                last_digit = DIGIT_MAP.get(x) if s.rindex(x) > s.rindex(y) else y

        return int(first_digit + last_digit)

    with open("input.txt") as fh:
        print(sum(map(get_calibration_value, map(lambda s: s.strip(), fh.readlines()))))


pt_1()  # 56108
pt_2()  # 55652
