import re


def solve(puzzle_input):
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    simple_count = 0
    better_count = 0
    for passport in puzzle_input.split('\n\n'):
        pairs = (item.split(':') for item in passport.split())
        fields = {key: value for key, value in pairs if key in required}
        if fields.keys() == required:
            simple_count += 1
            if all_valid(**fields):
                better_count += 1
    print(simple_count)
    print(better_count)


def all_valid(byr, iyr, eyr, hgt, hcl, ecl, pid):
    return bool(
        all(re.fullmatch(r'[0-9]{4}', value) for value in [byr, iyr, eyr])
        and 1920 <= int(byr) <= 2002
        and 2010 <= int(iyr) <= 2020
        and 2020 <= int(eyr) <= 2030
        and is_valid_height(hgt)
        and re.fullmatch(r'#[0-9a-f]{6}', hcl)
        and ecl in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
        and re.fullmatch(r'[0-9]{9}', pid)
    )


def is_valid_height(hgt):
    unitless_height = hgt[:-2]
    if not unitless_height.isdecimal():
        return False
    if hgt.endswith('in'):
        return 59 <= int(unitless_height) <= 76
    if hgt.endswith('cm'):
        return 150 <= int(unitless_height) <= 193
    return False
