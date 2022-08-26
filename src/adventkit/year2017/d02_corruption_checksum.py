import itertools

from adventkit import parse


def solve(puzzle_input):
    rows = parse.int_rows(puzzle_input)
    checksum = sum(max(row) - min(row) for row in rows)
    print(checksum)
    print(sum(quotient(row) for row in rows))


def quotient(row):
    for a, b in itertools.permutations(row, 2):
        if a % b == 0:
            return a // b
    raise ValueError("can't evenly divide any two values")
