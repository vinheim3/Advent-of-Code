from copy import deepcopy
import math

from util import get_fname

fname = get_fname(__file__)


def mark_invisible(asteroid_map, x, y, width, height, dx, dy):
    if dx == 0 and dy == 0:
        return
    gcd = math.gcd(dx, dy)
    new_dx = dx // gcd
    new_dy = dy // gcd
    x += dx + new_dx
    y += dy + new_dy
    while 0 <= x < width and 0 <= y < height:
        asteroid_map[y][x] = '.'
        x += new_dx
        y += new_dy


def get_visible_asteroids(asteroid_map, x, y, width, height):
    """
    aaabbbb
    aaabbbb
    aaa*bbb
    cccdddd
    cccdddd
    cccdddd
    """

    regions = [
        [range(y, -1, -1), range(x, -1, -1)],  # a
        [range(y, -1, -1), range(x, width)],  # b
        [range(y, height), range(x, -1, -1)],  # c
        [range(y, height), range(x, width)],  # d
    ]

    for y_range, x_range in regions:
        for check_y in y_range:
            for check_x in x_range:
                if asteroid_map[check_y][check_x] == '#':
                    mark_invisible(
                        asteroid_map, x, y, width, height,
                        check_x-x, check_y-y)


def sort_asteroids_by_angle(asteroid_map, x, y, width, height):
    asteroids = []
    for check_x in range(width):
        for check_y in range(height):
            if x == check_x and y == check_y:
                continue

            if asteroid_map[check_y][check_x] == '#':
                angle = math.degrees(math.atan2(y-check_y, check_x-x))
                adjusted_angle = angle - 90
                clockwise_angle = adjusted_angle * -1
                positive_angle = (clockwise_angle + 360) % 360
                asteroids.append((check_x, check_y, positive_angle))

    return sorted(asteroids, key=lambda item: item[2])


def solve_pt1():
    asteroid_map = []
    with open(fname) as f:
        for row in f.read().split('\n'):
            asteroid_map.append([*row])

    width = len(asteroid_map[0])
    height = len(asteroid_map)

    max_asteroids_seen = 0
    max_xloc = max_yloc = None
    for x in range(width):
        for y in range(height):
            if asteroid_map[y][x] == '#':
                curr_asteroids = 0
                new_map = deepcopy(asteroid_map)
                get_visible_asteroids(new_map, x, y, width, height)
                for y2 in range(height):
                    curr_asteroids += len([r for r in new_map[y2] if r == '#'])
                if curr_asteroids - 1 > max_asteroids_seen:
                    max_asteroids_seen = curr_asteroids - 1
                    max_xloc = x
                    max_yloc = y

    print(max_asteroids_seen)
    print(max_xloc, max_yloc)


def solve_pt2():  # best firing location is 14, 17
    asteroid_map = []
    with open(fname) as f:
        for row in f.read().split('\n'):
            asteroid_map.append([*row])

    width = len(asteroid_map[0])
    height = len(asteroid_map)

    x, y = 14, 17

    destroy_order = []
    while True:
        to_destroy = deepcopy(asteroid_map)
        get_visible_asteroids(to_destroy, x, y, width, height)
        sorted_asteroids = sort_asteroids_by_angle(to_destroy, x, y, width, height)
        destroy_order.extend(sorted_asteroids)

        for ast_x, ast_y, _ in sorted_asteroids:
            asteroid_map[ast_y][ast_x] = '.'

        has_asteroids = False
        asteroid_count = 0
        for row in asteroid_map:
            for cell in row:
                if cell == '#':
                    asteroid_count += 1
                    if asteroid_count == 2:
                        has_asteroids = True
                        break
            if has_asteroids:
                break

        if not has_asteroids:
            break

    chosen = destroy_order[199]
    print(chosen[0] * 100 + chosen[1])
