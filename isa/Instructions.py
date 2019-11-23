from cpu.Memory import REGISTERS, MEMORY

# General Instruction class that all instructions are subclasses of
class Instruction:
    def __init__(self, cpu, instruction):
        self.opcode = instruction[0]
        self.operands = instruction[1:]
        # eo meaning evaluated operands
        self.eo = []
        self.result = 0
        self.cycles = 1
    
    def decode(self, cpu):
        pass

    def execute(self, cpu):
        pass

    def writeback(self, cpu):
        pass
    
    def evaluate_params(self, operands):
        for elem in operands:
            valu = 0
            if elem.startswith('r'):
                valu = REGISTERS[elem]
            else:
                valu = int(elem)
            self.eo.append(valu)

class ALUInstruction(Instruction):
    def decode(self, cpu):
        self.eo.append(self.operands[0])
        self.evaluate_params(self.operands[1:])
    
    def execute(self, cpu):
        pass

    def writeback(self, cpu):
        REGISTERS[self.eo[0]] = self.result

class MEMORYInstruction(Instruction):
    def decode(self, cpu):
        if self.opcode in ["LD", "LDC", "MOV"]:
            self.eo.append(self.operands[0])
            self.evaluate_params(self.operands[1:])
        else:
            self.evaluate_params(self.operands[0:])

    def execute(self, cpu):
        pass

    def writeback(self, cpu):
        REGISTERS[self.eo[0]] = self.result

class CONTROLInstruction(Instruction):
    def decode(self, cpu):
        self.evaluate_params(self.operands[0:])

    def execute(self, cpu):
        pass

        




