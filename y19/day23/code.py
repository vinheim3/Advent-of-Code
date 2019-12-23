from collections import deque

from IntCode import Machine, get_ints
from util import get_fname

fname = get_fname(__file__)


class NIC:
    def __init__(self, idx):
        self.idx = idx
        self.data_queue = deque()
        self.is_x = True  # for input
        self.output = []

        self.idle_cnt = 0
        self.is_idle = False

    def set_not_idle(self):
        self.idle_cnt = 0
        self.is_idle = False

    def input_func(self, input_cnt):
        if input_cnt == 0:
            return self.idx
        if not self.data_queue:
            self.idle_cnt += 1
            if self.idle_cnt == 2:
                self.is_idle = True
            return -1

        self.set_not_idle()
        if self.is_x:
            ret = self.data_queue[0][0]
            self.is_x = False
            return ret
        else:
            ret = self.data_queue[0][1]
            self.is_x = True
            self.data_queue.popleft()
            return ret


def solve_pt1():
    ints = get_ints(fname)
    nics = []
    machs = []
    for i in range(50):
        nics.append(NIC(i))
        machs.append(Machine([*ints], input_func=nics[i].input_func))

    while True:
        for i in range(50):
            res = machs[i].process_opcode()
            if res is True:
                continue

            output = nics[i].output
            output.append(res)
            if len(output) == 3:
                if output[0] == 255:
                    print(output[2])
                    return
                nics[output[0]].data_queue.append((output[1], output[2]))
                nics[i].output = []


def solve_pt2():
    ints = get_ints(fname)
    nics = []
    machs = []

    for i in range(50):
        nics.append(NIC(i))
        machs.append(Machine([*ints], input_func=nics[i].input_func))

    last_nat_y = None
    nat_data = None

    while True:
        for i in range(50):
            res = machs[i].process_opcode()
            if res is True:
                continue

            nics[i].set_not_idle()
            output = nics[i].output
            output.append(res)
            if len(output) == 3:
                if output[0] == 255:
                    nat_data = (output[1], output[2])
                    nics[i].output = []
                else:
                    nics[output[0]].data_queue.append((output[1], output[2]))
                    nics[i].output = []

        # NAT part
        if all(nic.is_idle for nic in nics) and \
                all(len(nic.data_queue) == 0 for nic in nics):
            if nat_data[1] == last_nat_y:
                print(last_nat_y)
                return
            nics[0].data_queue.append(nat_data)
            last_nat_y = nat_data[1]
            nics[0].set_not_idle()
