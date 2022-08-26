import collections
import itertools
import string

from adventkit import parse


def solve(puzzle_input):
    lower_limit, upper_limit = parse.strings(puzzle_input)
    min_password = tuple(lower_limit)
    max_password = tuple(upper_limit)

    simple_count = 0
    better_count = 0
    for password in itertools.combinations_with_replacement(string.digits, 6):
        digit_counter = collections.Counter(password)
        if min_password <= password <= max_password and len(digit_counter) < 6:
            simple_count += 1
            if 2 in digit_counter.values():
                better_count += 1

    print(simple_count)
    print(better_count)
