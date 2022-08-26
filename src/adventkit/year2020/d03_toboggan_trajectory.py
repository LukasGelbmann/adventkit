from adventkit import grids, helpers


def solve(puzzle_input):
    trees, size = grids.select_and_measure('#', puzzle_input)
    slopes = (3, 1), (1, 1), (5, 1), (7, 1), (1, 2)
    counts = [count_encounters(slope, trees, size) for slope in slopes]
    print(counts[0])
    print(helpers.product(counts))


def count_encounters(slope, trees, size):
    position = grids.ORIGIN_2D
    count = 0
    while position.y < size.y:
        position += slope
        if (position.x % size.x, position.y) in trees:
            count += 1
    return count
