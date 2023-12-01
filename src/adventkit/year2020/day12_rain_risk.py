from adventkit import grids, parse


def solve(puzzle_input):
    instructions = parse.mixed_rows(puzzle_input)
    print(final_distance(instructions, step=grids.EAST))

    waypoint = grids.EAST * 10 + grids.NORTH
    print(final_distance(instructions, step=waypoint, waypoint_mode=True))


def final_distance(instructions, step, waypoint_mode=False):
    pos = grids.ORIGIN_2D
    for action, value in instructions:
        if action == 'L':
            step = step.rotate_left(value // 90)
        elif action == 'R':
            step = step.rotate_right(value // 90)
        elif action == 'F':
            pos += step * value
        else:
            direction = {
                'N': grids.NORTH,
                'S': grids.SOUTH,
                'E': grids.EAST,
                'W': grids.WEST,
            }[action]
            if waypoint_mode:
                step += direction * value
            else:
                pos += direction * value
    return pos.manhattan_distance(grids.ORIGIN_2D)
