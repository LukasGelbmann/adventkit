from adventkit import parse


def solve(puzzle_input):
    instructions = parse.mixed_rows(puzzle_input)
    output, _ = run(instructions)
    print(output)
    print(fixed_output(instructions))


def run(instructions):
    pointer = 0
    accumulator = 0
    seen = set()
    while 0 <= pointer < len(instructions) and pointer not in seen:
        seen.add(pointer)
        op, arg = instructions[pointer]
        if op == 'jmp':
            pointer += arg
            continue
        if op == 'acc':
            accumulator += arg
        pointer += 1
    return accumulator, pointer == len(instructions)


def fixed_output(instructions):
    for i, (op, arg) in enumerate(instructions):
        if op == 'acc':
            continue
        new_op = {'jmp': 'nop', 'nop': 'jmp'}[op]
        new_instructions = instructions.copy()
        new_instructions[i] = [new_op, arg]
        output, terminated = run(new_instructions)
        if terminated:
            return output
    raise ValueError("no valid solution exists")
