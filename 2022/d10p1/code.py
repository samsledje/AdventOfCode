import sys

n = 1
X = 1

class Processor:
    def __init__(self):
        self.cycle = 0
        self.X = 1

        self.instructions = []
        self.record = []

        self.add_buffer = 0
        self.add_wait = 1
        self.active_instruction = False

        self.debug = False

    def load_instructions(self, L):
        self.instructions.extend(L)

    def run_for(self, N_ticks):
        for _ in range(N_ticks):
            self.tick()

    def tick(self):
        self.cycle += 1
        self.add_wait -= 1
        self.record.append(self.X)

        if not self.active_instruction:
            self.read_instruction()

        if self.debug:
            print(f'Cycle {self.cycle}')
            print(f'X: {self.X}')
            print(f'add_buffer: {self.add_buffer}')
            print(f'add_wait: {self.add_wait}')
            print('=====')

        if self.active_instruction and not self.add_wait:
            self.X = self.X + self.add_buffer
            self.add_buffer = 0
            self.add_wait = 1
            self.active_instruction = False

    def read_instruction(self):
        try:
            ins, x = self.instructions.pop(0)
            if self.debug:
                print(f'Cycle {self.cycle}: Instruction {ins} {x}')
        except IndexError:
            return
        if ins == 'NOOP':
            pass
        if ins == 'ADDX':
            self.add_buffer = x
            self.add_wait = 1
            self.active_instruction = True

    def cycleN_X(self, n):
        if n > self.cycle:
            raise ValueError(f'Processor has not run for {n} cycles ({self.cycle})')
        return self.record[n - 1]

    def cycleN_signal(self, n):
        x = self.cycleN_X(n)
        return n * x

proc = Processor()
instruction_buffer = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        if line.startswith('noop'):
            instruction_buffer.append(('NOOP', None))
        else:
            x = line.strip().split()[1]
            instruction_buffer.append(('ADDX', int(x)))

#print(instruction_buffer)
#proc.debug = True
proc.load_instructions(instruction_buffer)
proc.run_for(220)

signal_sum = sum([proc.cycleN_signal(c) for c in [20, 60, 100, 140, 180, 220]])
print(signal_sum)
