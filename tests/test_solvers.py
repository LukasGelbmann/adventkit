"""Tests of functionality of puzzle solvers."""

import pathlib
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
        yield pytest.param(module.solve, year, day, id=test_id)


@pytest.mark.parametrize("solve,year,day", arg_combinations())
def test(solve, year, day, capsys, subtests):
    """Test the functionality of a solver."""

    for case in get_cases(year, day):
        with subtests.test(f"case {case.key}: {case.label}"):
            try:
                solve(case.data)
            finally:
                # Even if an exception occurred, clear the captured output.
                captured = capsys.readouterr()
            result = captured.out
            assert result == case.expected, f"case {case.key} ({case.label})"


def get_cases(year, day):
    """Return an iterable of test cases."""

    tests_root = pathlib.Path(__file__).parent
    folder = tests_root / f"year{year}" / f"day{day:02}"
    in_paths = []
    out_paths = []
    for path in sorted(folder.iterdir()):
        in_key = len(in_paths) + 1
        out_key = len(out_paths) + 1
        if path.match(f"case{in_key:02}_*_in.txt"):
            in_paths.append(path)
        elif path.match(f"case{out_key:02}_*_out.txt"):
            out_paths.append(path)
        elif not path.match(".*"):
            raise RuntimeError(f"unexpected filename: {path.name!r}")

    for key, (in_path, out_path) in enumerate(zip(in_paths, out_paths), 1):
        in_case_name, _, _ = in_path.stem.rpartition("_")
        out_case_name, _, _ = out_path.stem.rpartition("_")
        if in_case_name != out_case_name:
            raise RuntimeError(f"filenames are mismatched for case {key}")
        _, _, label = in_case_name.partition("_")
        with open(in_path, encoding="utf-8") as in_file:
            data = in_file.read()
        with open(out_path, encoding="utf-8") as out_file:
            expected = out_file.read()
        yield Case(key, label, data, expected)

    if len(in_paths) != len(out_paths) or not in_paths:
        raise RuntimeError("test cases are incomplete")
