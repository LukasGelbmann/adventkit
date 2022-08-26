import fractions
import math

from adventkit import grids, helpers


def solve(puzzle_input):
    asteroids = grids.select('#', puzzle_input)

    max_count, station = max(
        (count_detectable(location, asteroids), location)
        for location in asteroids
    )
    print(max_count)

    chosen_target = nth_vaporized(station, asteroids, n=200)
    print(100 * chosen_target.x + chosen_target.y)


def count_detectable(location, asteroids):
    targets = asteroids - {location}
    directions = {normalized_direction(location, target) for target in targets}
    return len(directions)


def normalized_direction(source, destination):
    x = destination.x - source.x
    y = destination.y - source.y
    divisor = math.gcd(x, y)
    return x // divisor, y // divisor


def nth_vaporized(station, asteroids, n):
    targets = asteroids - {station}
    rays = helpers.grouped(
        (angle(station, target), target) for target in targets
    )
    key = {}
    for laser_angle, ray in rays.items():
        ray.sort(key=station.manhattan_distance)
        for rotation, target in enumerate(ray):
            key[target] = rotation, laser_angle
    return sorted(targets, key=key.get)[n - 1]


def angle(source, destination):
    x, y = destination - source
    sector = 0 if x > 0 or (x == 0 and y <= 0) else 1
    slope = fractions.Fraction(y, x) if x != 0 else -math.inf
    return sector, slope
