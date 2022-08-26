import itertools

from adventkit import helpers, parse


def solve(puzzle_input):
    entries = parse.ints(puzzle_input)
    print(find_product(entries, count=2))
    print(find_product(entries, count=3))


def find_product(entries, count):
    for combination in itertools.combinations(entries, count):
        if sum(combination) == 2020:
            return helpers.product(combination)
    raise ValueError("no combination of values sums to 2020")
