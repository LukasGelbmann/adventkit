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


def int_rows(text, *, row_sep=None):
    """Parse a table and return a list of lists of extracted integers.

    `row_sep` is a string that separates rows in `text`. If `row_sep` is None,
    each line in `text` represents a row.

    See ints() for details on the handling of hyphen-minus characters.
    """

    raw_rows = _split(text, row_sep)
    return [ints(row) for row in raw_rows]


def string_rows(text, *, row_sep=None):
    """Parse a table and return a list of lists of alphanumeric strings.

    `row_sep` is a string that separates rows in `text`. If `row_sep` is None,
    each line in `text` represents a row.
    """

    raw_rows = _split(text, row_sep)
    return [strings(row) for row in raw_rows]


def mixed_rows(text, *, row_sep=None):
    """Parse a table and return a list of lists of integers and strings.

    `row_sep` is a string that separates rows in `text`. If `row_sep` is None,
    each line in `text` represents a row.

    See mixed_values() for details on the extraction of values from `text`.
    """

    raw_rows = _split(text, row_sep)
    return [mixed_values(row) for row in raw_rows]


def mixed_tables(text, *, table_sep=None, row_sep=None):
    """Return a list of tables of parsed values.

    That is a list of lists of lists. The elements of the innermost lists are
    integers and strings, extracted by the mixed_values() function.

    At least one of `table_sep` and `row_sep` must be given and not None.

    `table_sep` is a string that separates tables in `text`. If `table_sep` is
    None, each line in `text` represents a table.

    `row_sep` is a string that separates rows in `text`. If `row_sep` is None,
    each line in `text` represents a table row.
    """

    if table_sep is None and row_sep is None:
        raise ValueError("mixed_tables() needs table_sep or row_sep")

    raw_tables = _split(text, table_sep)
    return [mixed_rows(line, row_sep=row_sep) for line in raw_tables]


def _split(text, sep=None):
    """Split a string by delimiter or into lines and return a list of parts."""

    if sep is None:
        return text.splitlines()
    return text.split(sep)
