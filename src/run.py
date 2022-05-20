#!/usr/bin/env python3

"""A program that runs the solver for an Advent of Code puzzle.

In this project, each puzzle is solved in a module of its own. Each of these
solver modules contains a function called solve(), which takes the puzzle input
as a string argument and prints the solutions to stdout. The word 'solver' can
refer to a solver module or the solve() function inside it.

The solver modules of the same Advent of Code edition are grouped together in
packages. For example, the package `year2019` contains the solvers for Advent
of Code 2019. The solver modules have names starting with the character 'd'
(standing for 'day'), followed by the day of the advent calendar.

The files containing the puzzle input follow a similar naming scheme. For
example, the input for day 1 of Advent of Code 2019 should be stored in
`year2019/input/d01.txt`.
"""

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

    minimal = 3, 6
    if sys.version_info < minimal:
        message = "Error: this is Python {}.{}, need {}.{} or higher".format(
            sys.version_info.major, sys.version_info.minor, *minimal
        )
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


def read_input(year, day, base_path):
    """Return the input for a day of the Advent calender.

    Raise an OSError if the input file can't be read.
    """

    filename = 'd' + day + '.txt'
    path = os.path.join(base_path, 'year' + year, 'input', filename)
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
    base_path = os.path.dirname(os.path.realpath(__file__))

    try:
        package = importlib.import_module('year' + args.year)
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
        puzzle_input = read_input(args.year, args.day, base_path)
    except OSError as exc:
        print("Error:", exc, file=sys.stderr)
        return 1

    module.solve(puzzle_input)
    return 0


if __name__ == '__main__':
    sys.exit(main())
