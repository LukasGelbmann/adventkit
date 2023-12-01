from adventkit import grids, parse


def solve(puzzle_input):
    path_a, path_b = parse.mixed_tables(puzzle_input, row_sep=',')
    visits_a = visits(path_a)
    visits_b = visits(path_b)
    intersections = {square for square in visits_a if square in visits_b}

    distances = (
        grids.ORIGIN_2D.manhattan_distance(square) for square in intersections
    )
    print(min(distances))

    delays = (visits_a[square] + visits_b[square] for square in intersections)
    print(min(delays))


def visits(path):
    first_visit = {}
    for time, square in enumerate(squares(path), 1):
        if square not in first_visit:
            first_visit[square] = time
    return first_visit


def squares(path):
    square = 0, 0
    for direction, num_steps in path:
        move = {
            'L': grids.move_left,
            'R': grids.move_right,
            'U': grids.move_up,
            'D': grids.move_down,
        }[direction]
        for _ in range(num_steps):
            square = move(square)
            yield square
