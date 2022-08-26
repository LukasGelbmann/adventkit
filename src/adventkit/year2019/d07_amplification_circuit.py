import itertools

from adventkit import helpers, parse
from adventkit.year2019.d05_chance_of_asteroids import run_basic


def solve(puzzle_input):
    program = parse.ints(puzzle_input)

    sequence_setups = itertools.permutations(range(5))
    print(max(sequence_output(program, setup) for setup in sequence_setups))

    loop_setups = itertools.permutations(range(5, 10))
    print(max(loop_output(program, setup) for setup in loop_setups))


def sequence_output(program, setup):
    return next(output_signals(program, setup))


def loop_output(program, setup):
    return helpers.last(output_signals(program, setup))


def output_signals(program, setup):
    amplifiers = [run_basic(program, [setting]) for setting in setup]
    for amplifier in amplifiers:
        next(amplifier, None)
    signal = 0
    while True:
        for amplifier in amplifiers:
            try:
                amplifier.send(signal)
                signal = next(amplifier)
            except StopIteration:
                return
        yield signal
