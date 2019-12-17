def get_ints(fname):
    with open(fname) as f:
        return [int(x) for x in f.read().split(',')]


class Machine:
    def __init__(self, data, input_func=None):
        self.pc = 0
        self.data = data
        self.input_func = input_func
        self.input_cnt = 0
        self.last_output = None

        # Further extension for day 17
        self.data.extend([0]*(len(self.data)*2))
        self.relative_base = 0

    def param_mode(self, idx):
        opcode_group = self.data[self.pc]
        divisor = 10 * (10 ** idx)
        return (opcode_group // divisor) % 10

    def get_op(self, idx):
        # idx is index of the op to get
        param_mode = self.param_mode(idx)
        immediate_value = self.data[self.pc+idx]
        relative_idx = immediate_value+self.relative_base

        if param_mode == 1:  # immediate mode
            return immediate_value
        elif param_mode == 0:  # position mode
            return self.data[immediate_value]
        elif param_mode == 2:  # relative mode
            return self.data[relative_idx]
        else:
            raise Exception(f"Invalid paramMode: {param_mode}")

    def set_op(self, idx, val):
        # idx is index of the op to get
        param_mode = self.param_mode(idx)
        immediate_value = self.data[self.pc+idx]
        relative_idx = immediate_value+self.relative_base

        if param_mode == 1:  # immediate mode
            raise Exception("Cannot write to a parameter in immediate mode")
        elif param_mode == 0:  # position mode
            self.data[immediate_value] = val
        elif param_mode == 2:  # relative mode
            self.data[relative_idx] = val
        else:
            raise Exception(f"Invalid paramMode: {param_mode}")

    def endless(self):
        res = self.process_opcode()
        while res is not False:
            res = self.process_opcode()
        return self.last_output

    def process_opcode(self, stop_on_output=False):
        opcode_group = self.data[self.pc]
        opcode = opcode_group % 100
        if opcode == 99:
            return False

        if opcode == 1:  # add
            self.set_op(3, self.get_op(1) + self.get_op(2))
            self.pc += 4

        elif opcode == 2:  # mult
            self.set_op(3, self.get_op(1) * self.get_op(2))
            self.pc += 4

        elif opcode == 3:  # input
            if self.input_func is None:
                raise Exception('input not configured')
            self.set_op(1, self.input_func(self.input_cnt))
            self.input_cnt += 1
            self.pc += 2

        elif opcode == 4:  # output
            self.last_output = self.get_op(1)
            self.pc += 2
            if stop_on_output:
                return self.last_output

        elif opcode == 5:  # jump-if-true
            if self.get_op(1) != 0:
                self.pc = self.get_op(2)
            else:
                self.pc += 3

        elif opcode == 6:  # jump-if-false
            if self.get_op(1) == 0:
                self.pc = self.get_op(2)
            else:
                self.pc += 3

        elif opcode == 7:  # less than
            if self.get_op(1) < self.get_op(2):
                self.set_op(3, 1)
            else:
                self.set_op(3, 0)
            self.pc += 4

        elif opcode == 8:  # equals
            if self.get_op(1) == self.get_op(2):
                self.set_op(3, 1)
            else:
                self.set_op(3, 0)
            self.pc += 4

        elif opcode == 9:  # adjust relative base
            self.relative_base += self.get_op(1)
            self.pc += 2

        else:
            raise Exception(
                f"PC: {self.pc}\nOpcode: {opcode}\nData: {self.data}")

        return True
