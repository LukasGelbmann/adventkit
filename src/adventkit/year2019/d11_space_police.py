from adventkit import grids, helpers, parse
from adventkit.year2019.d09_sensor_boost import run


BLACK = 0
WHITE = 1

LEFT = 0


def solve(puzzle_input):
    program = parse.ints(puzzle_input)
    print(len(painted_panels(program)))

    identifier = painted_panels(program, start_on_white=True)
    grids.show(identifier, {WHITE: '#'})


def painted_panels(program, start_on_white=False):
    hull = {}
    position = grids.ORIGIN_2D
    step = grids.UP
    if start_on_white:
        hull[position] = WHITE

    robot = run_with_input_func(program, lambda: hull.get(position, BLACK))
    for color, turn in helpers.chunked(robot, 2):
        hull[position] = color
        step = step.rotate_left() if turn == LEFT else step.rotate_right()
        position += step

    return hull


def run_with_input_func(program, func):
    inputs = helpers.repeatedly_call(func)
    return run(program, inputs)
