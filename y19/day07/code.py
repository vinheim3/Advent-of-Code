import itertools

from IntCode import Machine, get_ints
from util import get_fname

fname = get_fname(__file__)


def run_amps(ints, a, b, c, d, e):
    thrust = 0

    def func_wrap(phase):
        def input_func(input_cnt):
            if input_cnt == 0:
                return phase
            if input_cnt == 1:
                return thrust
            raise Exception('Too many input commands')
        return input_func

    thrust = Machine([*ints], func_wrap(a)).endless()
    thrust = Machine([*ints], func_wrap(b)).endless()
    thrust = Machine([*ints], func_wrap(c)).endless()
    thrust = Machine([*ints], func_wrap(d)).endless()
    thrust = Machine([*ints], func_wrap(e)).endless()

    return thrust


def loop_run_amps(ints, a, b, c, d, e):
    last_signal = 0

    def func_wrap(phase):
        def input_func(input_cnt):
            # phase value
            if input_cnt == 0:
                return phase
            else:
                return last_signal
        return input_func

    a_mach = Machine([*ints], func_wrap(a))
    b_mach = Machine([*ints], func_wrap(b))
    c_mach = Machine([*ints], func_wrap(c))
    d_mach = Machine([*ints], func_wrap(d))
    e_mach = Machine([*ints], func_wrap(e))

    while True:
        for i, mach in enumerate([a_mach, b_mach, c_mach, d_mach, e_mach]):
            res = mach.process_opcode(stop_on_output=True)
            while res is True:
                res = mach.process_opcode(stop_on_output=True)
            if res is not False:
                last_signal = res
            elif i == 4:
                return e_mach.last_output


def solve_pt1():
    ints = get_ints(fname)

    max_thrusters = 0
    for a, b, c, d, e in itertools.permutations(range(5)):
        thrust = run_amps([*ints], a, b, c, d, e)
        if thrust > max_thrusters:
            max_thrusters = thrust

    print(max_thrusters)


def solve_pt2():
    ints = get_ints(fname)

    max_thrusters = 0
    for a, b, c, d, e in itertools.permutations(range(5, 10)):
        thrust = loop_run_amps([*ints], a, b, c, d, e)
        if thrust > max_thrusters:
            max_thrusters = thrust

    print(max_thrusters)
