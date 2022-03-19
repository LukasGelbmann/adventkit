"""Santa's little helpers: general-purpose helper tools."""

import collections
import itertools


def chunked(iterable, length):
    """Return an iterator over chunks of `iterable` with the given length.

    Each item of the returned iterator is a tuple containing `length` items of
    `iterable`, unless the end of `iterable` is reached. The last tuple may be
    shorter if it can't be filled up to the full length.

    Example: chunked(range(5), 2) --> (0, 1), (2, 3), (4,)
    """

    if length <= 0:
        raise ValueError("length for chunked() must be positive")

    iterator = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(iterator, length))
        if not chunk:
            return
        yield chunk


def grouped(pairs):
    """Return a dictionary mapping each key to a list of associated values.

    `pairs` must be an iterable of (key, value)-pairs. The keys are used to
    group the values. The return value is a `collections.defaultdict` instance
    which produces a new empty list as a value when a key is not present.

    For example, grouped([('A', 1), ('B', 5), ('A', 5)]) returns a dictionary
    mapping 'A' to [1, 5] and 'B' to [5].
    """

    groups = collections.defaultdict(list)
    for key, value in pairs:
        groups[key].append(value)
    return groups


def last(iterable):
    """Return the last item of an iterable.

    Raise a ValueError if `iterable` yields no items.
    """

    tail = collections.deque(iterable, maxlen=1)
    if not tail:
        raise ValueError("last() argument is an empty iterable")
    return tail[0]


def product(iterable):
    """Return the product of an iterable's items.

    An empty iterable has a product of 1, the multiplicative identity.

    Example: product([1, 2, 3, 4]) --> 24
    """

    result = 1
    for item in iterable:
        result *= item
    return result


def repeatedly_call(func, *args):
    """Return an infinite iterator that calls `func` to produce items."""
    return itertools.starmap(func, itertools.repeat(args))


def transpose(matrix):
    """Return the transpose of an iterable of iterables.

    The return value is a list of tuples. If the items of `matrix` aren't
    equally long, gaps are filled with None.

    Example: transpose(['AB', 'CDE']) --> [('A', 'C'), ('B', 'D'), (None, 'E')]
    """

    return list(itertools.zip_longest(*matrix))
