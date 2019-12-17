from IntCode import Machine, get_ints
from util import get_fname

fname = get_fname(__file__)


def load_grid(mach, draw=False):
    grid = []
    last_grid = None
    curr_row = []
    res = mach.process_opcode()
    while res is not False:
        res = mach.process_opcode()
        if res is True:
            continue
        if res == 10:
            if not curr_row:
                last_grid = [*grid]
                grid = []
                if draw:
                    print('-'*47)
                    for row in last_grid:
                        print("".join(row))
            else:
                grid.append(curr_row)
            curr_row = []
        else:
            curr_row.append(chr(res))

    return last_grid


def solve_pt1():
    ints = get_ints(fname)
    mach = Machine(ints)

    grid = load_grid(mach)

    total = 0
    height = len(grid)
    width = len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                if not (1 <= x < width-1) or not (1 <= y < height-1):
                    continue
                sum_squares = 0
                for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                    if grid[y+dy][x+dx] == '#':
                        sum_squares += 1
                if sum_squares > 2:
                    total += x*y
    print(total)


def solve_pt2():
    ints = get_ints(fname)
    ints[0] = 2

    inputs = """A,B,B,C,B,C,B,C,A,A
L,6,R,8,L,4,R,8,L,12
L,12,R,10,L,4
L,12,L,6,L,4,L,4
Y
"""

    def input_func(input_cnt):
        return ord(inputs[input_cnt])

    mach = Machine(ints, input_func)

    load_grid(mach, draw=True)

    print(mach.last_output)
