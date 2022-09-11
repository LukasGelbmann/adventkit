"""Tools for running the solver for an Advent of Code puzzle."""

# This import ensures that this program can print a nice error message if
# accidentally run in Python 2.7. For the same purpose, this program shouldn't
# use language features that result in a syntax error in Python 2.7.
from __future__ import print_function

import argparse
import importlib
import os
import pkgutil
import re
import sys


def check_python_version():
    """Exit if this process isn't running in the right Python version."""

    minimal = 3, 6, 1
    if sys.version_info < minimal:
        template = "Error: this is Python {}.{}.{}, need {}.{}.{} or higher"
        values = sys.version_info[:3] + minimal
        message = template.format(*values)
        print(message, file=sys.stderr)
        sys.exit(1)


def import_solver(package, day):
    """Import and return a solver module for a day of the Advent calendar.

    Return None if the module can't be found. No ImportError is raised in this
    situation in order to distinguish it from an error occurring during import.
    """

    prefix = 'd' + day
    for module_info in pkgutil.iter_modules(package.__path__):
        if module_info.name.startswith(prefix):
            name = package.__name__ + '.' + module_info.name
            return importlib.import_module(name)
    return None


def read_input(year, day):
    """Return the input for a day of the Advent calendar.

    Raise an OSError if the input file can't be read.
    """

    filename = 'd' + day + '.txt'
    path = os.path.join('input', 'year' + year, filename)
    with open(path, encoding='ascii') as file:
        return file.read()


def year_arg(value):
    """Validate the 'year' command-line argument."""

    if not re.fullmatch(r'\d{4}', value, re.ASCII):
        raise argparse.ArgumentTypeError("invalid year {!r}".format(value))
    return value


def day_arg(value):
    """Validate and reformat the 'day' command-line argument."""

    if not re.fullmatch(r'\d{1,2}', value, re.ASCII):
        raise argparse.ArgumentTypeError("invalid day {!r}".format(value))
    return value.zfill(2)


def parse_args():
    """Parse and return the command-line arguments.

    On error, print a usage message and exit.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=year_arg, help="e.g., 2019")
    parser.add_argument('day', type=day_arg, help="day of the Advent calendar")
    return parser.parse_args()


def main():
    """Solve a puzzle and return the exit status."""

    check_python_version()
    args = parse_args()

    try:
        package = importlib.import_module('adventkit.year' + args.year)
    except ImportError as exc:
        print("Error:", exc, file=sys.stderr)
        return 1

    module = import_solver(package, args.day)
    if module is None:
        message = "Error: can't find module for year {}, day {}".format(
            args.year, args.day
        )
        print(message, file=sys.stderr)
        return 1

    try:
        puzzle_input = read_input(args.year, args.day)
    except OSError as exc:
        print("Error:", exc, file=sys.stderr)
        return 1

    module.solve(puzzle_input)
    return 0
