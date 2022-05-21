"""Tools for working with grids, vectors, and points in space.

This module defines the class Vector2D, which can be used to simplify
operations in two-dimensional space such as vector addition. Instances of
Vector2D can also be used to represent points in 2D space.

Coordinate values of points and vectors can generally be any real number. For
many applications, however, it is natural to use only integral points. In the
context of this module, a *grid* is a mapping from integral points to values
of any type.
"""

import numbers
import typing


class Vector2D(typing.NamedTuple):
    """An immutable vector or point in 2D space.

    A Vector2D instance is fully characterized by its X-value and Y-value, both
    of which are real numbers, at least conventionally. They can be integers,
    floats, fractions, decimals, or any other type of real number.

    When using this class, by convention, the X-axis goes from left to right,
    with small numbers at the left. The Y-axis goes from top to bottom, with
    small numbers at the top.

    A Vector2D instance can represent either a vector or a point in 2D space.
    This is analogous to how a real number can represent a vector or a point in
    one-dimensional space.

    Vector2D is a subclass of the tuple class, and in many cases, the tuple
    (x, y) can be used interchangeably with the value Vector2D(x, y). The two
    behave the same in all comparison operations. In particular, (x, y) is
    equal to Vector2D(x, y). Like (x, y), Vector2D(x, y) is an iterable with
    two items, x and y. Methods of Vector2D that take another vector as an
    argument work with tuples as well.
    """

    x: numbers.Real
    y: numbers.Real

    def __str__(self):
        return f'(x={self.x}, y={self.y})'

    def __add__(self, other):
        """Return self+other, using vector addition."""

        other_x, other_y = other
        return Vector2D(self.x + other_x, self.y + other_y)

    def __radd__(self, other):
        """Return other+self, using vector addition."""

        other_x, other_y = other
        return Vector2D(other_x + self.x, other_y + self.y)

    def __sub__(self, other):
        """Return self-other, using vector subtraction."""

        other_x, other_y = other
        return Vector2D(self.x - other_x, self.y - other_y)

    def __rsub__(self, other):
        """Return other-self, using vector subtraction."""

        other_x, other_y = other
        return Vector2D(other_x - self.x, other_y - self.y)

    def __pos__(self):
        """Return +self."""
        return Vector2D(+self.x, +self.y)

    def __neg__(self):
        """Return -self, a copy of the vector `self` rotated by 180 degrees."""
        return Vector2D(-self.x, -self.y)

    def __mul__(self, value):
        """Return self*value, where `value` is a scalar."""
        return Vector2D(self.x * value, self.y * value)

    def __rmul__(self, value):
        """Return value*self, where `value` is a scalar."""
        return Vector2D(value * self.x, value * self.y)

    def __truediv__(self, value):
        """Return self/value, where `value` is a scalar."""
        return Vector2D(self.x / value, self.y / value)

    def __floordiv__(self, value):
        """Return self//value, where `value` is a scalar."""
        return Vector2D(self.x // value, self.y // value)

    def __mod__(self, value):
        """Return self%value, where `value` is a scalar."""
        return Vector2D(self.x % value, self.y % value)

    def __bool__(self):
        """Return True if this vector is not the zero vector."""
        return bool(self.x) or bool(self.y)

    def manhattan_distance(self, other):
        """Return the Manhattan distance between this point and another one."""

        other_x, other_y = other
        return abs(self.x - other_x) + abs(self.y - other_y)

    def neighbors(self):
        """Return a list of all eight neighbors, orthogonal and diagonal.

        This method assumes a grid spacing of 1.
        """

        x, y = self.x, self.y
        return [
            Vector2D(x - 1, y - 1),
            Vector2D(x - 1, y),
            Vector2D(x - 1, y + 1),
            Vector2D(x, y - 1),
            Vector2D(x, y + 1),
            Vector2D(x + 1, y - 1),
            Vector2D(x + 1, y),
            Vector2D(x + 1, y + 1),
        ]

    def rotate_left(self, times=1):
        """Return a copy of this vector, rotated left a given number of times.

        Each rotation turns the vector by 90 degrees.
        """

        times %= 4
        if times == 1:
            return Vector2D(self.y, -self.x)
        if times == 2:
            return -self
        if times == 3:
            return Vector2D(-self.y, self.x)
        return self

    def rotate_right(self, times=1):
        """Return a copy of this vector, rotated right a given number of times.

        Each rotation turns the vector by 90 degrees.
        """

        times %= 4
        if times == 1:
            return Vector2D(-self.y, self.x)
        if times == 2:
            return -self
        if times == 3:
            return Vector2D(self.y, -self.x)
        return self


ORIGIN_2D = Vector2D(0, 0)
LEFT = WEST = Vector2D(-1, 0)
RIGHT = EAST = Vector2D(+1, 0)
UP = NORTH = Vector2D(0, -1)
DOWN = SOUTH = Vector2D(0, +1)


def select(target, lines):
    """Return a set of the points marked with the target character.

    `lines` can be either a string or an iterable of strings. The return value
    is a set of Vector2D instances.

    Take, for example, a map looking like this:

        X.O
        .XO
        ..X

    Selecting all points marked with an 'O' works as follows:

        select('O', ['X.O', '.XO', '..X'])
        --> {Vector2D(x=2, y=0), Vector2D(x=2, y=1)}

    See also select_and_measure().
    """

    if isinstance(lines, str):
        lines = lines.splitlines()
    return {
        Vector2D(x, y)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char == target
    }


def select_and_measure(target, lines):
    r"""Return a tuple containing a set of selected points and the map's size.

    `lines` can be either a string or an iterable of strings. In the returned
    pair, both the points and the size are Vector2D instances.

    As an example, take a map looking like this:

        .O
        X.O
        X

    The points marked with an 'X' can be selected as follows:

        select_and_measure('X', '.O\nX.O\nX')
        --> ({Vector2D(x=0, y=1), Vector2D(x=0, y=2)}, Vector2D(x=3, y=3))

    If the size of the map isn't needed, select() can be used instead.
    """

    if isinstance(lines, str):
        lines = lines.splitlines()
    width = max((len(line) for line in lines), default=0)
    height = len(lines)
    return select(target, lines), Vector2D(width, height)


def show(grid, symbols):
    """Print a visual representation of a grid.

    `grid` is a mapping from 2D integral points (tuples or Vector2D instances)
    to values of any type. `symbols` is a mapping from values to characters
    visualizing these values.

    Values not present in `symbols` are shown as spaces, or not depicted at all
    if they're out of frame. Points not present in the grid are treated as if
    they had the value None. Neighboring points within each row are separated
    by spaces.

    For example, show({(0, 0): 7, (1, 0): 8, (1, 1): 8}, {7: '>', 8: '|'})
    prints the following to stdout:

        > |
          |
    """

    visible = [point for point, value in grid.items() if value in symbols]
    if not visible:
        return
    visible_x = {x for x, _ in visible}
    visible_y = {y for _, y in visible}
    x_range = range(min(visible_x), max(visible_x) + 1)
    y_range = range(min(visible_y), max(visible_y) + 1)
    for y in y_range:
        row = (grid.get((x, y)) for x in x_range)
        print(' '.join(symbols.get(value, ' ') for value in row))


def move_left(point):
    """Return a copy of `point`, moved left along the X-axis by 1.

    This function returns a tuple, not a Vector2D instance, and should only be
    used if performance is essential. Otherwise, the recommended alternative is
    to write `point + LEFT`.
    """

    x, y = point
    return x - 1, y


def move_right(point):
    """Return a copy of `point`, moved right along the X-axis by 1.

    The caveats for move_left() apply here as well.
    """

    x, y = point
    return x + 1, y


def move_up(point):
    """Return a copy of `point`, moved up along the Y-axis by 1.

    The caveats for move_left() apply here as well.
    """

    x, y = point
    return x, y - 1


def move_down(point):
    """Return a copy of `point`, moved down along the Y-axis by 1.

    The caveats for move_left() apply here as well.
    """

    x, y = point
    return x, y + 1
