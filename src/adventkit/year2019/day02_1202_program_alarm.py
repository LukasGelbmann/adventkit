from adventkit import parse


def solve(puzzle_input):
    program = parse.ints(puzzle_input)
    print(output(program, noun=12, verb=2))
    print(find_input(program))


def output(program, noun, verb):
    memory = list(program)
    memory[1] = noun
    memory[2] = verb

    pointer = 0
    while memory[pointer] != 99:
        opcode, a_addr, b_addr, result_addr = memory[pointer : pointer + 4]
        a = memory[a_addr]
        b = memory[b_addr]
        if opcode == 1:
            memory[result_addr] = a + b
        elif opcode == 2:
            memory[result_addr] = a * b
        else:
            raise NotImplementedError(f"opcode {opcode}")
        pointer += 4

    return memory[0]


def find_input(program):
    for noun in range(100):
        for verb in range(100):
            if output(program, noun, verb) == 19690720:
                return 100 * noun + verb
    raise ValueError("no valid input exists")
