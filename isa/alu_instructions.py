from .Instructions import ALUInstruction
from cpu.Memory import REGISTERS, MEMORY

## Arithmetic, comparisons and logic

class ADD(ALUInstruction):
    def execute(self, cpu):
        self.result = self.eo[1] + self.eo[2]

class ADDI(ALUInstruction):
    def execute(self, cpu):
        self.result = REGISTERS[self.eo[0]] + self.eo[1]

class SUB(ALUInstruction):
    def execute(self, cpu):
        self.result = self.eo[1] - self.eo[2]

class SUBI(ALUInstruction):
    def execute(self, cpu):
        self.result = REGISTERS[self.eo[0]] - self.eo[1]

class MUL(ALUInstruction):
    def execute(self, cpu):
        self.result = self.eo[1] * self.eo[2]

class DIV(ALUInstruction):
    def execute(self, cpu):
        self.result = self.eo[1] / self.eo[2]

class CMP(ALUInstruction):
    def execute(self, cpu):
        x = self.eo[1] - self.eo[2]
        if x == 0:
            self.result = 0
        else:
            self.result = int(x / abs(x))