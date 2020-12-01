Advent of Code in Python
========================

These are my solutions in Python to some of the [Advent of Code
puzzles](https://adventofcode.com). My primary aim is to make the code
readable, making it fast is a secondary goal.

Requirements
------------

-   Python 3.6+
-   Puzzle input files placed in the right locations: the input for day
    1 of Advent of Code 2019 is read from `advent2019/input/d01.txt`.

Optional:

-   A POSIX-compliant shell (`/bin/sh`)
-   A shell command `python3` to run Python 3.6+ (any implementation)
-   A shell command `pypy3` to invoke PyPy 3.6+

How to run
----------

-   Run a single day's solver: `python3 run.py 2019 10` (or
    `./run.sh 2019 10`)
-   Run all solvers: `./run.sh`
-   Run all solvers from one year: `./run.sh 2019`

When invoked with the optional argument `--time`, `run.sh` print the
execution time for each day. If the command `pypy3` invokes a suitable
version of PyPy, `run.sh` uses it for any solvers that are expected to
run faster under PyPy than CPython.
