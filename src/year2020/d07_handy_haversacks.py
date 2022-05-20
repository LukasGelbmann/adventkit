import functools
import re


def solve(puzzle_input):
    rules = parse_rules(puzzle_input)
    print(count_containers_of('shiny gold', rules))

    @functools.lru_cache(maxsize=None)
    def count_bags_in(color):
        contents = rules[color]
        return sum(n * (1 + count_bags_in(inner)) for n, inner in contents)

    print(count_bags_in('shiny gold'))


def parse_rules(puzzle_input):
    rules = {}
    for line in puzzle_input.splitlines():
        color, contents_text = line.split(' bags contain ')
        items = re.findall(r'(\d+) ([^,]+) bag', contents_text)
        rules[color] = [(int(n), inner) for n, inner in items]
    return rules


def count_containers_of(target, rules):
    @functools.lru_cache(maxsize=None)
    def contains_target(color):
        contents = rules[color]
        return any(
            inner == target or contains_target(inner) for _, inner in contents
        )

    count = 0
    for color in rules:
        if contains_target(color):
            count += 1
    return count
