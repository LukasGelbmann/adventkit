"""Tools for parsing puzzle input."""

import re


def ints(text):
    """Return a list of extracted integers.

    A hyphen-minus character '-' directly preceding a number is treated as a
    minus sign, unless it directly follows another number, in which case it's
    treated as a separator.

    Example: ints('-3 T-4,5-10') --> [-3, -4, 5, 10]
    """

    pattern = r'(?<!\d)-?\d+'
    return [int(match) for match in re.findall(pattern, text, re.ASCII)]


def strings(text):
    """Return a list of extracted alphanumeric strings.

    Example: strings('53_7A,a735') --> ['53', '7A', 'a735']
    """

    return re.findall(r'[A-Za-z\d]+', text, re.ASCII)


def mixed_values(text):
    """Return a list of extracted integers and alphabetic strings.

    A hyphen-minus character '-' directly preceding a digit is treated as a
    minus sign, unless it directly follows a digit or letter, in which case
    it's treated as a separator.

    Example: mixed_values('-1-99 A7: Q-8,-9') --> [-1, 99, 'A', 7, 'Q', 8, -9]
    """

    pattern = r'(?:(?<![A-Za-z\d])-)?\d+|[A-Za-z]+'
    return [
        int(match) if match[0] in '0123456789-' else match
        for match in re.findall(pattern, text, re.ASCII)
    ]


def int_table(text):
    """Return a table (a list of lists) of integers, one row per line.

    See ints() for details on the handling of hyphen-minus characters."""

    return [ints(line) for line in text.splitlines()]


def string_table(text):
    """Return a table of extracted alphanumeric strings, one row per line."""
    return [strings(line) for line in text.splitlines()]


def mixed_table(text):
    """Return a table of integers and alphabetic strings, one row per line.

    See mixed_values() for details on the handling of hyphen-minus characters.
    """

    return [mixed_values(line) for line in text.splitlines()]


def compact_mixed_table(line):
    """Return a table (lists of lists) of parsed values.

    The table is parsed from a single line, with rows separated by commas.

    See mixed_values() for details on the handling of hyphen-minus characters.
    """

    return [mixed_values(row) for row in line.split(',')]


def compact_mixed_tables(text):
    """Return a list of tables of parsed values.

    That is a list of lists of lists.  Each table (list of lists) is parsed
    from a single line of the input string.

    See mixed_values() for details on the handling of hyphen-minus characters.
    """

    return [compact_mixed_table(line) for line in text.splitlines()]
