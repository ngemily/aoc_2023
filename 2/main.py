from functools import reduce

import re

s = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
ss = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]

# 12 red cubes, 13 green cubes, and 14 blue cubes
RED = 12
GREEN = 13
BLUE = 14


def get_game(game):
    """Get game from (game_id, game)"""
    (_, game) = game
    return game


def parse_game(s):
    """Parse the game string input returning Game ID and the game itself.

    s (str): e.g. "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    Returns: (game_id, game)
    """
    game_id, game = s.split(":")
    game_id = re.match(r"Game (\d+)", game_id).group(1)
    return (game_id, game)


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


def check_draws(draw):
    """Check if the draw itself is valid, i.e. does not contain any draws that
    exceed the number of available cubes.

    draw (str): e.g. "3 blue, 4 red"
    Returns: (bool) draw is valid
    """
    (red, green, blue) = parse_draw(draw)
    return not (red > RED or green > GREEN or blue > BLUE)


def sum_if_valid(acc, game):
    """Check if the game is valid and if so, add its id to the given accumulator.

    acc (int): running sum
    game (game_id, game_str): e.g. ("4", "3 blue, 4 red; 1 red, 2 green, 6 # blue; 2 green")

    Returns: (bool) Updated value of accumulator.
    """
    game_id, game = game
    if all(map(lambda draw: check_draws(draw), game.split(";"))):
        return acc + int(game_id)
    else:
        return acc


def minimal_set(acc, draw):
    """Return the minimal set of cubes required to allow game of {acc, draw} to
    be valid.

    { acc, draw } (int, int, int)
    """
    return (max(draw[0], acc[0]), max(draw[1], acc[1]), max(draw[2], acc[2]))


def min_power(game):
    """Return the min power of a game, defined as (r * g * b) of the minimum set
    of cubes that permit 'game' to be valid.
    """
    (min_r, min_g, min_b) = reduce(
        minimal_set, map(parse_draw, game.split(";")), (0, 0, 0)
    )
    return min_r * min_g * min_b


def pt_1():
    with open("input.txt") as fh:
        print(reduce(sum_if_valid, map(parse_game, fh.readlines()), 0))


def pt_2():
    with open("input.txt") as fh:
        print(sum(map(min_power, map(get_game, map(parse_game, fh.readlines())))))


pt_1()  # 2679
pt_2()  # 77607
