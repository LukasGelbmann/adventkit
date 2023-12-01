import itertools

from adventkit import grids


def solve(puzzle_input):
    number = int(puzzle_input)
    square = locate_square(square_id=number)
    print(square.manhattan_distance(grids.ORIGIN_2D))
    print(first_value_above(threshold=number))


def locate_square(square_id):
    square = grids.ORIGIN_2D
    steps_left = square_id - 1
    for step, length in spiral_segments():
        if steps_left <= length:
            square += step * steps_left
            break
        square += step * length
        steps_left -= length
    return square


def first_value_above(threshold):
    memory = {}
    square = grids.ORIGIN_2D
    value = 1
    steps = spiral_steps()
    while value <= threshold:
        memory[square] = value
        square += next(steps)
        value = sum(memory.get(neighbor, 0) for neighbor in square.neighbors())
    return value


def spiral_segments():
    step = grids.RIGHT
    for length in itertools.count(1):
        for _ in range(2):
            yield step, length
            step = step.rotate_left()


def spiral_steps():
    for step, length in spiral_segments():
        for _ in range(length):
            yield step
