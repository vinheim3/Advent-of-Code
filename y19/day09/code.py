from IntCode import Machine, get_ints
from util import get_fname

fname = get_fname(__file__)


def solve_pt1():
    ints = get_ints(fname)
    print(Machine(ints, lambda input_cnt: 1).endless())


def solve_pt2():
    ints = get_ints(fname)
    print(Machine(ints, lambda input_cnt: 2).endless())
