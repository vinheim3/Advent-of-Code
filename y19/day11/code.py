from IntCode import Machine, get_ints
from util import get_fname

fname = get_fname(__file__)


def get_paint(paint_map: dict, x, y):
    paint = paint_map.setdefault(x, {}).setdefault(y, None)
    if paint == 1:
        return 1
    else:
        return 0


def get_painted(initial=None):
    ints = get_ints(fname)

    painted = initial or {}  # x -> y -> paint(null-black, 1-white, 0-black)
    robot_dir = 0  # 0-up, 1-right, 2-down, 3-left
    curr_x = 0
    curr_y = 0
    output_type = 0  # 0-paint current, 1-turn+move

    mach = Machine(
        ints, input_func=lambda input_cnt: get_paint(painted, curr_x, curr_y))

    res = True
    while res is not False:
        if res is not True:
            if res not in [0, 1]:
                raise Exception(f"Invalid output sent: {res}")

            if output_type == 0:  # paint current
                painted.setdefault(curr_x, {})[curr_y] = res
            else:  # turn+move
                if res == 0:
                    robot_dir = (robot_dir + 3) % 4
                else:
                    robot_dir = (robot_dir + 1) % 4
                dx, dy = [[0, -1], [1, 0], [0, 1], [-1, 0]][robot_dir]
                curr_x += dx
                curr_y += dy
            output_type = 1 - output_type
        res = mach.process_opcode(stop_on_output=True)

    return painted


def solve_pt1():
    painted = get_painted()

    total_painted = 0
    for xval, yvals in painted.items():
        total_painted += len([v for v in yvals.values() if v is not None])
    print(total_painted)


def solve_pt2():
    painted = get_painted({0: {0: 1}})
    min_x = min_y = max_x = max_y = 0
    for xval, yvals in painted.items():
        min_x = min(xval, min_x)
        max_x = max(xval, max_x)
        min_y = min(*yvals.keys(), min_y)
        max_y = max(*yvals.keys(), max_y)
    for y in range(min_y, max_y+1):
        row = [painted.setdefault(x, {}).setdefault(y, None)
               for x in range(min_x, max_x+1)]
        mapp = {None: ' ', 1: '*', 0: '.'}
        row = [mapp[cell] for cell in row]
        print(" ".join(row))
