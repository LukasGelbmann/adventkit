from adventkit import parse


def solve(puzzle_input):
    masses = parse.ints(puzzle_input)
    print(sum(fuel_needed(mass) for mass in masses))
    print(sum(total_fuel(mass) for mass in masses))


def fuel_needed(mass):
    return mass // 3 - 2


def total_fuel(mass):
    total = 0
    while True:
        mass = fuel_needed(mass)
        if mass <= 0:
            return total
        total += mass
