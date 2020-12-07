import string


def solve(puzzle_input):
    groups = [group.splitlines() for group in puzzle_input.split('\n\n')]
    print(sum(count_any_yes(responses) for responses in groups))
    print(sum(count_all_yes(responses) for responses in groups))


def count_any_yes(responses):
    questions = set().union(*responses)
    return len(questions)


def count_all_yes(responses):
    questions = set(string.ascii_lowercase).intersection(*responses)
    return len(questions)
