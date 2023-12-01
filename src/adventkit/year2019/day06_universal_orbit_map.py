from adventkit import helpers, parse


def solve(puzzle_input):
    direct_orbits = parse.string_rows(puzzle_input)
    print(count_orbits(direct_orbits))

    parent_by_child = {child: parent for parent, child in direct_orbits}
    you_ancestors = ancestors('YOU', parent_by_child)
    santa_ancestors = ancestors('SAN', parent_by_child)
    transfers = set(you_ancestors) ^ set(santa_ancestors)
    print(len(transfers))


def count_orbits(direct_orbits):
    children = helpers.grouped(direct_orbits)
    total = 0
    num_ancestors = 0
    frontier = ['COM']
    while frontier:
        total += len(frontier) * num_ancestors
        frontier = [child for node in frontier for child in children[node]]
        num_ancestors += 1
    return total


def ancestors(node, parent_by_child):
    while node in parent_by_child:
        node = parent_by_child[node]
        yield node
