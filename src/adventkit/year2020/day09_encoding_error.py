import itertools

from adventkit import parse


def solve(puzzle_input):
    numbers = parse.ints(puzzle_input)
    invalid = find_invalid(numbers)
    print(invalid)
    print(weakness(numbers, invalid))


def find_invalid(numbers):
    for i in range(25, len(numbers)):
        target = numbers[i]
        previous = numbers[i - 25 : i]
        pairs = itertools.combinations(previous, 2)
        if not any(a + b == target and a != b for a, b in pairs):
            return target
    raise ValueError("no invalid number exists")


def weakness(numbers, target):
    for size in range(2, len(numbers) + 1):
        window_sum = sum(numbers[:size])
        for low in itertools.count():
            high = low + size
            if window_sum == target:
                window = numbers[low:high]
                return min(window) + max(window)
            if high == len(numbers):
                break
            window_sum -= numbers[low]
            window_sum += numbers[high]
    raise ValueError("no encryption weakness exists")
