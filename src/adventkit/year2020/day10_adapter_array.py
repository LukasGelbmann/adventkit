import collections

from adventkit import parse


def solve(puzzle_input):
    adapters = parse.ints(puzzle_input)
    joltages = sorted(adapters) + [max(adapters) + 3]

    diffs = [b - a for a, b in zip([0] + joltages, joltages)]
    print(diffs.count(1) * diffs.count(3))

    print(count_arrangements(joltages))


def count_arrangements(joltages):
    counts = collections.Counter()
    counts[0] = last = 1
    for n in joltages:
        counts[n] = last = counts[n - 1] + counts[n - 2] + counts[n - 3]
    return last
