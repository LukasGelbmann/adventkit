"""Tests of functionality of puzzle solvers."""

import pathlib
import re
import typing

import pytest

from adventkit.year2017 import (
    d01_inverse_captcha,
    d02_corruption_checksum,
)


class Case(typing.NamedTuple):
    """A test case for a specific puzzle."""

    key: int
    label: str
    data: str
    expected: str


def arg_combinations():
    """Return combinations of argument values for parametrizing the test."""

    values = [
        (d01_inverse_captcha, 2017, 1),
        (d02_corruption_checksum, 2017, 2),
    ]
    for module, year, day in values:
        _, _, puzzle_label = module.__name__.partition("_")
        test_id = f"{year}, day {day}: {puzzle_label}"
        yield pytest.param(module.solve, year, day, puzzle_label, id=test_id)


@pytest.mark.parametrize("solve,year,day,puzzle_label", arg_combinations())
def test(solve, year, day, puzzle_label, capsys, subtests):
    """Test the functionality of a solver."""

    for case in get_cases(year, day, puzzle_label):
        with subtests.test(f"case {case.key}: {case.label}"):
            try:
                solve(case.data)
            finally:
                # Even if an exception occurred, clear the captured output.
                captured = capsys.readouterr()
            result = captured.out
            assert result == case.expected, f"case {case.key} ({case.label})"


def get_cases(year, day, puzzle_label):
    """Return a list of test cases."""

    tests_root = pathlib.Path(__file__).parent
    path = tests_root / f"year{year}" / f"day{day:02}_{puzzle_label}.txt"
    with open(path, encoding="utf-8") as file:
        file_text = file.read()

    # There may optionally be some notes before the cases start.
    sections = re.split(r"^={40}\n\n", file_text, flags=re.MULTILINE)
    cases_section = sections[-1]

    # We expect at least one test case, and re.split() always returns at least
    # one item.
    texts = re.split(r"^-{40}\n\n", cases_section, flags=re.MULTILINE)
    return [parse_case(text, key) for key, text in enumerate(texts, start=1)]


def parse_case(text, key):
    """Parse and return a test case."""

    first_line, _, _ = text.partition("\n")
    prefix = f"CASE {key}: "
    if not first_line.startswith(prefix):
        raise ValueError(f"case {key} has unexpected start {first_line!r}")
    label = first_line[len(prefix) :]

    # There may optionally be a note before the input starts.
    parts = re.split(r"^------INPUT---------\n", text, flags=re.MULTILINE)
    if len(parts) != 2:
        raise ValueError(f"input header missing or repeated for case {key}")
    _, essence = parts

    values = re.split(r"^------ANSWERS-------\n", essence, flags=re.MULTILINE)
    if len(values) != 2:
        raise ValueError(f"answers header missing or repeated for case {key}")
    data, expected = values

    return Case(key, label, data, expected)
