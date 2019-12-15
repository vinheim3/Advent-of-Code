from util import get_fname

fname = get_fname(__file__)


def get_fuel(module):
    fuel = (module // 3) - 2
    if fuel <= 0:
        return 0
    return fuel + get_fuel(fuel)


def solve_pt1():
    with open(fname) as f:
        data = [int(x) for x in f.read().split('\n')]

    print(sum([(r // 3) - 2 for r in data]))


def solve_pt2():
    with open(fname) as f:
        data = [int(x) for x in f.read().split('\n')]

    print(sum([get_fuel(r) for r in data]))
