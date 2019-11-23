from .Instructions import MEMORYInstruction
from cpu.Memory import REGISTERS, MEMORY
## Memory access

class LD(MEMORYInstruction):
    def execute(self, cpu):
        self.result = MEMORY[self.eo[1] + self.eo[2]]
        

class LDC(MEMORYInstruction):
    def execute(self, cpu):
        self.result = self.eo[1]

class MOV(MEMORYInstruction):
    def execute(self, cpu):
        self.result = self.eo[1]

class ST(MEMORYInstruction):
    def execute(self, cpu):
        self.result = self.eo[1]

    def writeback(self, cpu):
        MEMORY[self.eo[0] + self.eo[2]] = self.result

class STC(MEMORYInstruction):
    def execute(self, cpu):
        self.result = self.eo[1]

    def writeback(self, cpu):
        MEMORY[self.eo[0]] = self.result

