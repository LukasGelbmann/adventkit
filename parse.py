"""Tools for parsing puzzle input."""

import re


def ints(string):
    """Return a list of extracted integers."""
    return [int(match) for match in re.findall(r'-?\d+', string, re.ASCII)]


def strings(string):
    """Return a list of extracted alphanumeric strings."""
    return re.findall(r'[A-Za-z\d]+', string, re.ASCII)


def mixed_values(string):
    """Return a list of extracted integers and alphabetic strings."""

    matches = re.finditer(r'(-?\d+)|([A-Za-z]+)', string, re.ASCII)
    return [
        int(match[1]) if match[1] is not None else match[2]
        for match in matches
    ]


def int_table(string):
    """Return a table (a list of lists) of integers, one row per line."""
    return [ints(line) for line in string.splitlines()]


def string_table(string):
    """Return a table of extracted alphanumeric strings, one row per line."""
    return [strings(line) for line in string.splitlines()]


def mixed_table(string):
    """Return a table of integers and alphabetic strings, one row per line."""
    return [mixed_values(line) for line in string.splitlines()]


def compact_mixed_table(line):
    """Return a table (lists of lists) of parsed values.

    The table is parsed from a single line, with rows separated by commas."""

    return [mixed_values(row) for row in line.split(',')]


def compact_mixed_tables(string):
    """Return a list of tables of parsed values.

    That is a list of lists of lists.  Each table (list of lists) is parsed
    from a single line of the input string."""

    return [compact_mixed_table(line) for line in string.splitlines()]
