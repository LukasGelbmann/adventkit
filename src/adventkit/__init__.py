"""Solutions to Advent of Code puzzles.

In this project, each puzzle is solved in a module of its own. Each of these
solver modules contains a function called solve(), which takes the puzzle input
as a string argument and prints the solutions to stdout. The word 'solver' can
refer to a solver module or the solve() function inside it.

The solver modules of the same Advent of Code edition are grouped together in
packages. For example, the package `year2019` contains the solvers for Advent
of Code 2019. The solver modules have names starting with the character 'd'
(standing for 'day'), followed by the day of the Advent calendar.

The files containing the puzzle input follow a similar naming scheme. For
example, the input for day 1 of Advent of Code 2019 should be stored in
`input/year2019/d01.txt` (relative to the current working directory).
"""

from ._version import __version__
