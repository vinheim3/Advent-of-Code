from util import get_fname

fname = get_fname(__file__)


def get_wire_instructions():
    with open(fname) as f:
        data = f.read()
        wire1, wire2 = data.split('\n')
        wire1 = wire1.split(',')
        wire2 = wire2.split(',')

    return wire1, wire2


def get_visited_cells(wire):
    visited = {}  # x -> [ys]
    curr_x = 0
    curr_y = 0

    for instr in wire:
        direction = instr[0]
        amount = int(instr[1:])

        dx, dy = {
            'L': [-1, 0], 'R': [1, 0], 'U': [0, -1], 'D': [0, 1],
        }[direction]

        for i in range(amount):
            curr_x += dx
            curr_y += dy

            visited.setdefault(curr_x, set()).add(curr_y)

    return visited


def get_visited_cells_time(wire):
    visited = {}  # x -> y -> first time getting there
    curr_x = 0
    curr_y = 0
    steps = 0

    for instr in wire:
        direction = instr[0]
        amount = int(instr[1:])

        dx = 0
        dy = 0

        if direction == 'L':
            dx = -1
        elif direction == 'R':
            dx = 1
        elif direction == 'U':
            dy = -1
        elif direction == 'D':
            dy = 1
        else:
            raise Exception(f"Invalid direction: {direction}")

        for i in range(amount):
            steps += 1
            curr_x += dx
            curr_y += dy

            visited.setdefault(curr_x, {}).setdefault(curr_y, steps)

    return visited


def get_similar_cells(vis1, vis2):
    all_similar = []

    for xval, yvals in vis1.items():
        if xval not in vis2:
            continue

        for similar_yval in (yvals & vis2[xval]):
            all_similar.append([xval, similar_yval])

    return all_similar


def get_similar_cells_time(vis1, vis2):
    all_similar = []

    for xval, yvals in vis1.items():
        if xval not in vis2:
            continue

        yvals2 = vis2[xval]

        for yval in yvals:
            if yval in yvals2:
                all_similar.append(yvals[yval] + yvals2[yval])

    return all_similar


def manhattan(cell):
    return abs(cell[0]) + abs(cell[1])


def solve_pt1():
    l, r = get_wire_instructions()
    visl = get_visited_cells(l)
    visr = get_visited_cells(r)
    similar_cells = get_similar_cells(visl, visr)

    min_distance = manhattan(similar_cells[0])
    for similar_cell in similar_cells[1:]:
        dist = manhattan(similar_cell)
        min_distance = min(dist, min_distance)

    print(min_distance)


def solve_pt2():
    l, r = get_wire_instructions()
    visl = get_visited_cells_time(l)
    visr = get_visited_cells_time(r)
    similar_cells = get_similar_cells_time(visl, visr)

    print(min(similar_cells))
