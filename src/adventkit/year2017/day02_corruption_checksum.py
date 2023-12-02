import itertools

from adventkit import parse


def solve(data):
    rows = parse.int_rows(data)
    checksum = sum(max(row) - min(row) for row in rows)
    print(checksum)
    print(sum(quotient(row) for row in rows))


def quotient(row):
    for a, b in itertools.permutations(row, 2):
        if b != 0 and a % b == 0:
            return a // b
    raise ValueError("can't evenly divide any two values")
