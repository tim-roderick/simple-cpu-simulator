from .Instructions import CONTROLInstruction
from cpu.Memory import REGISTERS, MEMORY

## Branches and Jumps

class J(CONTROLInstruction):
    def execute(self, cpu):
        cpu.program_counter = self.eo[0]

class BEQZ(CONTROLInstruction):
    def execute(self, cpu):
        if self.eo[1] == 0:
            cpu.program_counter = self.eo[0]
        else:
            cpu.program_counter = self.pc + 1

class BNEZ(CONTROLInstruction):
    def execute(self, cpu):
        if self.eo[1] != 0:
            cpu.program_counter = self.eo[0]
        else:
            cpu.program_counter = self.pc + 1

class BLTZ(CONTROLInstruction):
    def execute(self, cpu):
        if self.eo[1] < 0:
            cpu.program_counter = self.eo[0]
        else:
            cpu.program_counter = self.pc + 1

class BGEZ(CONTROLInstruction):
    def execute(self, cpu):
        if self.eo[1] >= 0:
            cpu.program_counter = self.eo[0]
        else:
            cpu.program_counter = self.pc + 1