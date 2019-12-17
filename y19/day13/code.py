from IntCode import Machine, get_ints
import time

from util import get_fname

fname = get_fname(__file__)


def draw_screen(screen):
    min_x = min_y = max_x = max_y = 0
    first = True
    for y, xvals in screen.items():
        for x, val in xvals.items():
            if first:
                min_x = max_x = x
                min_y = max_y = y
                first = False
            else:
                min_x = min(x, min_x)
                min_y = min(y, min_y)
                max_x = max(x, max_x)
                max_y = max(y, max_y)

    for y in range(min_y, max_y + 1):
        if y not in screen:
            print('\n')
            continue

        row = screen[y]
        row_str = []

        for x in range(min_x, max_x + 1):
            if x == -1 and y == 0:
                print(row[x])
                row_str.append(' ')
                continue
            if x not in row:
                row_str.append(' ')
            else:
                tile = [
                    ' ', '#', '\u25a8', '_', 'o'
                ]
                row_str.append(tile[row[x]])
        print(''.join(row_str))


def solve_pt1():
    ints = get_ints(fname)
    mach = Machine(ints)

    output_type = 0
    x = None
    y = None
    screen = {}  # y -> x -> int

    res = True
    while res is not False:
        if res is not True:
            if output_type == 0:
                x = res
            elif output_type == 1:
                y = res
            else:
                screen.setdefault(y, {})[x] = res

            output_type = (output_type + 1) % 3
        res = mach.process_opcode()

    total_blocks = 0
    for y, xvals in screen.items():
        total_blocks += len([v for v in xvals.values() if v == 2])
    print(total_blocks)


def solve_pt2():
    ints = get_ints(fname)
    paddle_x = 0
    ball_x = 0

    def paddle_input(input_cnt):
        diff = ball_x - paddle_x
        return diff // abs(diff) if diff != 0 else 0

    mach = Machine(ints, input_func=paddle_input)
    ints[0] = 2

    output_type = 0
    x = None
    y = None
    screen = {}  # y -> x -> int  38x21

    res = True

    try:
        while res is not False:
            if res is not True:
                if output_type == 0:
                    x = res
                elif output_type == 1:
                    y = res
                else:
                    screen.setdefault(y, {})[x] = res
                    if res == 3:
                        paddle_x = x
                        draw_screen(screen)
                        time.sleep(0.02)
                    if res == 4:
                        ball_x = x
                        draw_screen(screen)
                        time.sleep(0.02)

                output_type = (output_type + 1) % 3
            res = mach.process_opcode()
    finally:
        draw_screen(screen)
