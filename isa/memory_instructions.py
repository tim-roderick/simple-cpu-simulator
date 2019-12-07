from .Instructions import MEMORYInstruction
from cpu.Memory import REGISTERS, MEMORY
## Memory access

class LD(MEMORYInstruction):
    def __init__(self, cpu, instruction):
        super(LD, self).__init__(cpu, instruction)
        self.cycles = 5

    def execute(self, cpu):
        self.result = MEMORY[self.eo[1] + self.eo[2]]        

class LDC(MEMORYInstruction):
    def __init__(self, cpu, instruction):
        super(LDC, self).__init__(cpu, instruction)
        self.cycles = 5

    def execute(self, cpu):
        self.result = self.eo[1]

class MOV(MEMORYInstruction):
    def __init__(self, cpu, instruction):
        super(MOV, self).__init__(cpu, instruction)
        self.cycles = 3
    def execute(self, cpu):
        self.result = self.eo[1]

class ST(MEMORYInstruction):
    def __init__(self, cpu, instruction):
        super(ST, self).__init__(cpu, instruction)
        self.cycles = 3

    def execute(self, cpu):
        self.result = self.eo[1]

    def writeback(self, cpu):
        MEMORY[self.eo[0] + self.eo[2]] = self.result

class STC(MEMORYInstruction):
    def __init__(self, cpu, instruction):
        super(STC, self).__init__(cpu, instruction)
        self.cycles = 3

    def execute(self, cpu):
        self.result = self.eo[1]

    def writeback(self, cpu):
        MEMORY[self.eo[0]] = self.result

