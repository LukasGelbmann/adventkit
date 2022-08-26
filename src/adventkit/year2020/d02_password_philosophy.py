from adventkit import parse


def solve(puzzle_input):
    rows = parse.mixed_rows(puzzle_input)

    first_count = 0
    for min_appearances, max_appearances, letter, password in rows:
        if min_appearances <= password.count(letter) <= max_appearances:
            first_count += 1
    print(first_count)

    second_count = 0
    for low, high, letter, password in rows:
        if (password[low - 1] == letter) != (password[high - 1] == letter):
            second_count += 1
    print(second_count)
