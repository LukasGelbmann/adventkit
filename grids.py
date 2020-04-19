"""Tools for working with grids, vectors, and points in space.

This module defines the class Vector2D, which can be used to simplify
operations in two-dimensional space such as vector addition.  Instances of
Vector2D can also be used to represent points in 2D space.

In the context of this module, a grid is a mapping from points to values (of
any type)."""

import numbers
import typing


class Vector2D(typing.NamedTuple):
    """An immutable vector or point in 2D space.

    A Vector2D instance is fully characterized by its X-value and Y-value, both
    of which are real numbers, at least conventionally.  They can be integers,
    floats, fractions, decimals, or any other type of real number.

    When using this class, by convention, the X-axis goes from left to right,
    with small numbers at the left.  The Y-axis goes from top to bottom, with
    small numbers at the top.

    A Vector2D instance can represent either a vector or a point in 2D space.
    This is analogous to how a real number can represent a vector or a point in
    one-dimensional space.

    Vector2D is a subclass of the tuple class, and in many cases, the tuple
    (x, y) can be used interchangeably with the value Vector2D(x, y).  The two
    behave the same in all comparison operations.  In particular, (x, y) is
    equal to Vector2D(x, y).  Like (x, y), Vector2D(x, y) is an iterable with
    two items, x and y.  Methods of Vector2D that take another vector as an
    argument work with tuples as well."""

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
        """Return self*value, where value is a scalar."""
        return Vector2D(self.x * value, self.y * value)

    def __rmul__(self, value):
        """Return value*self, where value is a scalar."""
        return Vector2D(value * self.x, value * self.y)

    def __truediv__(self, value):
        """Return self/value, where value is a scalar."""
        return Vector2D(self.x / value, self.y / value)

    def __floordiv__(self, value):
        """Return self//value, where value is a scalar."""
        return Vector2D(self.x // value, self.y // value)

    def __mod__(self, value):
        """Return self%value, where value is a scalar."""
        return Vector2D(self.x % value, self.y % value)

    def __bool__(self):
        """Return True if this vector is not the zero vector."""
        return bool(self.x) or bool(self.y)

    def manhattan_distance(self, other):
        """Return the Manhattan distance between this point and another one."""

        other_x, other_y = other
        return abs(self.x - other_x) + abs(self.y - other_y)

    def rotate_left(self):
        """Return a copy of this vector, rotated left by 90 degrees."""
        return Vector2D(self.y, -self.x)

    def rotate_right(self):
        """Return a copy of this vector, rotated right by 90 degrees."""
        return Vector2D(-self.y, self.x)


ORIGIN_2D = Vector2D(0, 0)
LEFT = Vector2D(-1, 0)
RIGHT = Vector2D(+1, 0)
UP = Vector2D(0, -1)
DOWN = Vector2D(0, +1)


def select(target, map_string):
    r"""Return a set of the points marked with the target character.

    Take, for example, a map looking like this:

        X.O
        .XO
        ..X

    Here, select('O', 'X.O\n.XO\n..X') returns the set {Vector2D(x=2, y=0),
    Vector2D(x=2, y=1)}."""

    lines = map_string.splitlines()
    return {
        Vector2D(x, y)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char == target
    }


def show(grid, symbols):
    """Print a visual representation of a grid.

    `grid` is a mapping from 2D points to values (of any type).  `symbols` is a
    mapping from values to characters visualizing these values.

    Values not present in `symbols` are shown as spaces.  Points not present in
    the grid are treated as if they had the value None.  Neighboring points
    within each row are separated by spaces.

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
    used if performance is essential.  Otherwise, the recommended alternative
    is to write `point + LEFT`."""

    x, y = point
    return x - 1, y


def move_right(point):
    """Return a copy of `point`, moved right along the X-axis by 1.

    The caveats for move_left() apply here as well."""

    x, y = point
    return x + 1, y


def move_up(point):
    """Return a copy of `point`, moved up along the Y-axis by 1.

    The caveats for move_left() apply here as well."""

    x, y = point
    return x, y - 1


def move_down(point):
    """Return a copy of `point`, moved down along the Y-axis by 1.

    The caveats for move_left() apply here as well."""

    x, y = point
    return x, y + 1
