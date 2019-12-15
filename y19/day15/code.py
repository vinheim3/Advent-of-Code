import time

from IntCode import Machine, get_ints
from util import get_fname

fname = get_fname(__file__)

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


def reconstruct_path(came_from, current):
    # current to be goal node
    # came_from to be a mapping of node -> which tile reached it
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        if current is None:
            break
        total_path = [current, *total_path]
    return total_path


def shortest_path(grid):
    came_from, _ = expand(grid, '*')

    goal_x = goal_y = None
    found = False
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'G':
                goal_x = x
                goal_y = y
                found = True
            if found:
                break
        if found:
            break
    return reconstruct_path(came_from, (goal_x, goal_y))


def convert_grid(grid, curr=None):
    min_x = min_y = 999
    max_x = max_y = -999
    for y, xvals in grid.items():
        min_y = min(y, min_y)
        max_y = max(y, max_y)
        for x, val in xvals.items():
            min_x = min(x, min_x)
            max_x = max(x, max_x)

    all_rows = []
    for y in range(min_y, max_y+1):
        row_string = []
        row = grid[y]
        for x in range(min_x, max_x+1):
            if curr and x == curr[0] and y == curr[1]:
                row_string.append('@')
            elif x == 0 and y == 0:
                row_string.append('*')
            elif x not in row:
                row_string.append(' ')
            else:
                tile = row[x]
                row_string.append(['#', '.', 'G'][tile])
        all_rows.append(row_string)

    return all_rows


def draw_grid(grid_rows, direction):
    print('--------------------')
    player_char = {NORTH: '^', SOUTH: 'v', WEST: '<', EAST: '>'}[direction]
    for row in grid_rows:
        print(''.join(row).replace('@', player_char))


def grid_done(grid, x, y):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x = x+dx
        new_y = y+dy
        if new_y not in grid or new_x not in grid[new_y]:
            return False
    return True


def mark_grid(grid, x, y, to_explore):
    # called when a new tile is filled in
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x = x+dx
        new_y = y+dy
        if new_y in to_explore and new_x in to_explore[new_y]:
            if grid_done(grid, new_x, new_y):
                del to_explore[new_y][new_x]


def get_grid_rows(draw=False):
    ints = get_ints(fname)

    curr_x = 0
    curr_y = 0
    grid = {curr_y: {curr_x: 1}}  # y -> x -> 0(wall), 1(space), 2(goal)
    dir_map = {NORTH: [0, -1], SOUTH: [0, 1], WEST: [-1, 0], EAST: [1, 0]}
    next_dir = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}
    prev_dir = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
    variables = {
        'just_hit_wall': False,
        'direction': NORTH,
    }

    to_explore = {0: {0: None}}

    # need to alternate between hitting wall, and going next direction
    def input_func(input_cnt):
        if input_cnt == 0:
            return NORTH

        if variables['just_hit_wall']:
            variables['just_hit_wall'] = False
            variables['direction'] = next_dir[variables['direction']]
        else:
            variables['direction'] = prev_dir[variables['direction']]

        return variables['direction']

    mach = Machine(ints, input_func=input_func)

    while any(to_explore.values()):
        res = mach.process_opcode(stop_on_output=True)
        if res is True:
            continue

        if res in [1, 2]:
            dx, dy = dir_map[variables['direction']]
            curr_x += dx
            curr_y += dy
            grid.setdefault(curr_y, {})[curr_x] = res

            mark_grid(grid, curr_x, curr_y, to_explore)
            if not grid_done(grid, curr_x, curr_y):
                to_explore.setdefault(curr_y, {})[curr_x] = None

        if res == 0:
            dx, dy = dir_map[variables['direction']]
            wall_x = curr_x + dx
            wall_y = curr_y + dy

            grid.setdefault(wall_y, {})[wall_x] = 0
            mark_grid(grid, wall_x, wall_y, to_explore)

            variables['just_hit_wall'] = True

        if draw:
            time.sleep(0.05)
            draw_grid(convert_grid(grid, curr=(curr_x, curr_y)),
                      variables['direction'])

    list_rows = convert_grid(grid)
    return list_rows


def expand(grid, start_char):
    start_x = start_y = None
    found = False
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == start_char:
                start_x = x
                start_y = y
                found = True
            if found:
                break
        if found:
            break

    width = len(grid[0])
    height = len(grid)

    open_set = {(start_x, start_y)}
    new_open_set = set()
    came_from = {(start_x, start_y): None}

    cnt = -1

    while open_set:
        for node in open_set:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x = node[0] + dx
                new_y = node[1] + dy
                if new_x < 0 or new_y < 0 or new_x >= width or new_y >= height:
                    continue
                if (new_x, new_y) in came_from or grid[new_y][new_x] == '#':
                    continue
                new_open_set.add((new_x, new_y))
                came_from[(new_x, new_y)] = node

        open_set = new_open_set
        new_open_set = set()

        cnt += 1

    return came_from, cnt


def solve_pt1():
    grid_rows = get_grid_rows()
    shortest = shortest_path(grid_rows)
    print(len(shortest) - 1)


def solve_pt2():
    grid_rows = get_grid_rows()
    _, cnt = expand(grid_rows, 'G')
    print(cnt)
