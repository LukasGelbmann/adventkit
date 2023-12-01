import collections

from adventkit import helpers, parse


def solve(puzzle_input):
    program = parse.ints(puzzle_input)

    first_outputs = run_basic(program, inputs=[1])
    print(helpers.last(first_outputs))

    second_outputs = run_basic(program, inputs=[5])
    print(next(second_outputs))


def run_basic(program, inputs=(), opcode_handlers=None, mode_handlers=None):
    if opcode_handlers is None:
        opcode_handlers = {}
    if mode_handlers is None:
        mode_handlers = {}

    memory = collections.defaultdict(int, enumerate(program))
    pointer = 0
    inputs_iter = iter(inputs)
    next_input = None

    while True:
        instruction_value = memory[pointer]
        if instruction_value < 0:
            raise ValueError(f"negative instruction value {instruction_value}")
        opcode = instruction_value % 100
        modes = instruction_value // 100
        pointer += 1

        if opcode in opcode_handlers:
            pointer = opcode_handlers[opcode](memory, pointer, modes)
            continue

        if opcode == 99:
            return

        a_addr = arg_addr(memory, pointer, modes % 10, mode_handlers)
        a = memory[a_addr]
        pointer += 1

        if opcode == 3:
            if next_input is not None:
                memory[a_addr] = next_input
                next_input = yield None
                continue

            current_input = next(inputs_iter, None)
            if current_input is not None:
                memory[a_addr] = current_input
                continue

            current_input = yield None
            if current_input is not None:
                memory[a_addr] = current_input
                next_input = yield None
                continue

            raise ValueError("got None as input")

        if opcode == 4:
            if next_input is not None:
                raise ValueError("trying to output but just got input")
            next_input = yield a
            continue

        b_addr = arg_addr(memory, pointer, modes // 10 % 10, mode_handlers)
        b = memory[b_addr]
        pointer += 1

        if opcode == 5:
            if a != 0:
                pointer = b
            continue

        if opcode == 6:
            if a == 0:
                pointer = b
            continue

        c_addr = arg_addr(memory, pointer, modes // 100, mode_handlers)
        pointer += 1

        if opcode == 1:
            memory[c_addr] = a + b
        elif opcode == 2:
            memory[c_addr] = a * b
        elif opcode == 7:
            memory[c_addr] = int(a < b)
        elif opcode == 8:
            memory[c_addr] = int(a == b)
        else:
            raise NotImplementedError(f"opcode {opcode}")


def arg_addr(memory, pointer, mode, mode_handlers):
    if mode in mode_handlers:
        return mode_handlers[mode](memory, pointer)
    if mode == 0:
        return memory[pointer]
    if mode == 1:
        return pointer
    raise NotImplementedError(f"parameter mode {mode}")
