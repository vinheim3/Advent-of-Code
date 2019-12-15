from IntCode import Machine, get_ints
from util import get_fname

fname = get_fname(__file__)


def solve_pt1():
    ints = get_ints(fname)

    ints[1] = 12
    ints[2] = 2

    mach = Machine(ints)
    mach.endless()
    print(mach.data[0])


def solve_pt2():
    ints = get_ints(fname)

    def get_noun_verb():
        for _noun in range(100):
            for _verb in range(100):
                dints = [*ints]
                dints[1] = _noun
                dints[2] = _verb

                mach = Machine(dints)
                mach.endless()
                res = mach.data[0]

                if res == 19690720:
                    return _noun, _verb

    noun, verb = get_noun_verb()

    print(100 * noun + verb)
