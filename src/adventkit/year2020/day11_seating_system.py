from adventkit import grids


def solve(puzzle_input):
    seats, size = grids.select_and_measure('L', puzzle_input)

    adjacent = {seat: set(seat.neighbors()) & seats for seat in seats}
    print(final_count(seats, adjacent, crowded=4))

    visible = {seat: set(visible_from(seat, seats, size)) for seat in seats}
    print(final_count(seats, visible, crowded=5))


def final_count(seats, neighbors, crowded):
    occupied = set()
    while True:
        new = set()
        for seat in seats:
            count = len(neighbors[seat] & occupied)
            if count == 0 or (seat in occupied and count < crowded):
                new.add(seat)
        if new == occupied:
            return len(occupied)
        occupied = new


def visible_from(seat, seats, size):
    for step in grids.ORIGIN_2D.neighbors():
        other = seat + step
        while 0 <= other.x < size.x and 0 <= other.y < size.y:
            if other in seats:
                yield other
                break
            other += step
