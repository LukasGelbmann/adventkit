"""Tests of functionality of puzzle solvers."""

import pathlib
import re
import typing

import pytest

from adventkit.year2017 import (
    day01_inverse_captcha,
    day02_corruption_checksum,
    day03_spiral_memory,
    day04_passphrases,
)


INDENT_WIDTH = 4
INDENT = " " * INDENT_WIDTH


class Case(typing.NamedTuple):
    """A test case for a specific puzzle."""

    key: int
    label: str
    data: str
    expected: str


def arg_combinations():
    """Return combinations of argument values for parametrizing the test."""

    values = [
        (day01_inverse_captcha, 2017, 1),
        (day02_corruption_checksum, 2017, 2),
        (day03_spiral_memory, 2017, 3),
        (day04_passphrases, 2017, 4),
    ]
    for module, year, day in values:
        _, _, puzzle_label = module.__name__.partition("_")
        test_id = f"{year}, day {day}: {puzzle_label}"
        yield pytest.param(module.solve, year, day, puzzle_label, id=test_id)


@pytest.mark.parametrize("solve,year,day,puzzle_label", arg_combinations())
def test(solve, year, day, puzzle_label, capsys, subtests):
    """Test the functionality of a solver."""

    for case in get_cases(year, day, puzzle_label):
        with subtests.test(f"Case {case.key}: {case.label}"):
            try:
                solve(case.data)
            finally:
                # Even if an exception occurred, clear the captured output.
                captured = capsys.readouterr()
            result = captured.out
            assert result == case.expected, f"case {case.key} ({case.label})"


def get_cases(year, day, puzzle_label):
    """Return a list of test cases."""

    # The test cases are parsed from Markdown (CommonMark) format, with each
    # case forming an item in a numbered list.  Each case starts with a label,
    # which is bold text.  The label is followed by a code block containing the
    # input data.  Finally, each test case ends with a paragraph stating the
    # expected answers, each in a code span.
    #
    # The parsing routine aims to ensure that the file containing the test
    # cases will be understood by Markdown parsers in the intended way.  The
    # parsing routine rejects input where this can't be easily verified.

    tests_root = pathlib.Path(__file__).parent
    path = tests_root / f"year{year}" / f"day{day:02}_{puzzle_label}.md"
    with open(path, encoding="utf-8") as file:
        file_text = file.read()

    # There may optionally be a note before the cases start.
    separator_width = 72
    separator = "\n\n" + "-" * separator_width + "\n\n"
    note, _, cases_section = file_text.rpartition(separator)

    if "```" in note or "~~~" in note or "<" in note or "$$" in note:
        raise RuntimeError("can't rule out unclosed Markdown block in note")

    # We expect at least one test case, and re.split() always returns at least
    # one item.
    texts = re.split(r"\n\n\b", cases_section.strip("\n"))
    return [parse_case(text, key) for key, text in enumerate(texts, start=1)]


def parse_case(text, key):
    """Parse and return a test case."""

    head, _, body = text.strip("\n").partition("\n\n")

    prefix = f"{key}.".ljust(INDENT_WIDTH)
    if not prefix.endswith(" "):
        raise ValueError(f"test case key is too large: {key}")
    if not head.startswith(prefix):
        raise ValueError(f"test case {key} doesn't start with {prefix!r}")
    raw_label = head[len(prefix) :]
    label = parse_label(raw_label)

    data_block, _, answers_text = body.rpartition(f"\n\n{INDENT}Answers: ")
    data = parse_data(data_block)
    answers = parse_answers(answers_text)
    expected = "".join(answer + "\n" for answer in answers)

    return Case(key, label, data, expected)


def parse_label(raw_label):
    """Extract and return the label of a test case."""

    if not re.fullmatch(r"[*][*][ a-zA-Z0-9',-]+[*][*]", raw_label):
        raise ValueError(f"can't parse strong emphasis: {raw_label!r}")
    label = raw_label.strip("*")

    if label.startswith(" ") or label.endswith(" "):
        raise ValueError(f"test case label with invalid whitespace: {label!r}")

    return label


def parse_data(data_block):
    """Extract and return the input data of a test case."""

    if "\r" in data_block:
        raise ValueError("can't handle carriage return in code block")

    # We can't use splitlines() because it considers more characters to be line
    # endings than CommonMark does.
    raw_lines = data_block.strip("\n").split("\n")

    # In the rare case that the input data contains a tab character, we expect
    # an indented code block.  This is so that the content of the code block
    # starts after eight spaces, making it look nice when the tab width is
    # eight columns.  Otherwise, we expect a fenced code block.
    if "\t" in data_block:
        if not raw_lines[0].strip() or not raw_lines[-1].strip():
            raise ValueError("can't parse code block next to whitespace")
        inner_lines = raw_lines
        data_indent = INDENT * 2
    else:
        if len(raw_lines) < 2:
            raise ValueError(f"too few lines for code fences: {raw_lines}")
        first, *inner_lines, last = raw_lines
        data_indent = INDENT
        if not first == last == f"{INDENT}```":
            raise ValueError(f"unexpected code fences: {first!r}, {last!r}")
        for raw_line in inner_lines:
            if "```" in raw_line:
                raise ValueError(f"can't rule out code fence: {raw_line!r}")

    lines = []
    for raw_line in inner_lines:
        if raw_line and not raw_line.startswith(data_indent):
            raise ValueError(f"line without proper indent: {raw_line!r}")
        line = raw_line[len(data_indent) :]
        lines.append(line + "\n")
    return "".join(lines)


def parse_answers(answers_text):
    """Extract and return the answers of a test case."""

    answers = []
    for raw_answer in answers_text.split(", "):
        if not re.fullmatch(r"`[\w-]+`", raw_answer):
            raise ValueError(f"can't parse code span: {raw_answer!r}")
        answers.append(raw_answer.strip("`"))
    return answers
