def solve(puzzle_input):
    binary_input = puzzle_input.translate(str.maketrans('FBLR', '0101'))
    seat_ids = {int(line, base=2) for line in binary_input.splitlines()}
    print(max(seat_ids))
    print(missing(seat_ids))


def missing(seat_ids):
    i = min(seat_ids)
    while i in seat_ids:
        i += 1
    return i
