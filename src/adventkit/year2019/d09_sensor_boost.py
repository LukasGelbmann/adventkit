from adventkit import parse
from adventkit.year2019.d05_chance_of_asteroids import arg_addr, run_basic


def solve(puzzle_input):
    program = parse.ints(puzzle_input)
    for input_value in 1, 2:
        output = next(run(program, [input_value]))
        print(output)


def run(program, inputs=()):
    def adjust_base(memory, arg_pointer, mode):
        nonlocal relative_base
        addr = arg_addr(memory, arg_pointer, mode, mode_handlers)
        relative_base += memory[addr]
        return arg_pointer + 1

    def relative_arg_addr(memory, pointer):
        return relative_base + memory[pointer]

    relative_base = 0
    opcode_handlers = {9: adjust_base}
    mode_handlers = {2: relative_arg_addr}
    return run_basic(program, inputs, opcode_handlers, mode_handlers)
