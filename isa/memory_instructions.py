from .Instructions import MEMORYInstruction
from cpu.Memory import REGISTERS, MEMORY
## Memory access

class LD(MEMORYInstruction):
    def __init__(self, cpu, instruction, pc):
        super(LD, self).__init__(cpu, instruction, pc)
        self.cycles = 5

    def execute(self, cpu):
        self.result = MEMORY[self.eo[1] + self.eo[2]]

    def writeback(self, cpu):
        first_result = self.result    
        self.execute(cpu)
        if self.result == first_result:
            super(LD, self).writeback(cpu)
        else:
            cpu.program_counter = self.pc+1
            super(LD, self).writeback(cpu)
            cpu.flush_pipeline(self)

class LDC(MEMORYInstruction):
    def __init__(self, cpu, instruction, pc):
        super(LDC, self).__init__(cpu, instruction, pc)
        self.cycles = 5

    def execute(self, cpu):
        self.result = self.eo[1]

class MOV(MEMORYInstruction):
    def __init__(self, cpu, instruction, pc):
        super(MOV, self).__init__(cpu, instruction, pc)
        self.cycles = 3
    def execute(self, cpu):
        self.result = self.eo[1]

class ST(MEMORYInstruction):
    def __init__(self, cpu, instruction, pc):
        super(ST, self).__init__(cpu, instruction, pc)
        self.cycles = 3

    def execute(self, cpu):
        self.result = self.eo[1]

    def writeback(self, cpu):
        MEMORY[self.eo[0] + self.eo[2]] = self.result

class STC(MEMORYInstruction):
    def __init__(self, cpu, instruction, pc):
        super(STC, self).__init__(cpu, instruction, pc)
        self.cycles = 3

    def execute(self, cpu):
        self.result = self.eo[1]

    def writeback(self, cpu):
        MEMORY[self.eo[0]] = self.result

