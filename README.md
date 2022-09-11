Adventkit -- Advent of Code in Python
=====================================

These are my solutions in Python to some of the [Advent of Code
puzzles](https://adventofcode.com). My goal is to make the code readable
while also making it reasonably fast.

Installation
------------

You can install Adventkit using pip:

    pip install adventkit

Alternatively, after cloning the Adventkit repository, the code can be
run as is.

Requirements
------------

-   Python 3.6.1+
-   Puzzle input files placed in the right locations: the input for day
    1 of Advent of Code 2019 is read from `input/year2019/d01.txt`
    (relative to the current working directory).

Optional, to run `src/run.sh` after cloning the repository:

-   A POSIX-compliant shell (`/bin/sh`)
-   A shell command `python3` to run Python 3.6.1+ (any implementation)
-   If extra speed is desired on selected puzzles: A shell command
    `pypy3` to invoke PyPy 3.6+

How to run
----------

After installing Adventkit, you can run a single day's solver like this:

    adventkit 2019 10

Cloning the repository gives you more options:

-   Run a single day's solver: `src/run.sh 2019 10` (or
    `python3 src/run.py 2019 10`)
-   Run all solvers: `src/run.sh`
-   Run all solvers from one year: `src/run.sh 2019`

When invoked with the optional argument `--time`, `src/run.sh` prints
the execution time for each day. If the command `pypy3` invokes a
suitable version of PyPy, `src/run.sh` uses it for any solvers that are
expected to run faster under PyPy than CPython.
