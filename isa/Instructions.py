from cpu.Memory import REGISTERS, MEMORY, SCOREBOARD

# General Instruction class that all instructions are subclasses of
class Instruction:
    def __init__(self, cpu, instruction):
        self.opcode = instruction[0]
        # self.dest
        # self.source
        # self.immediate
        # self.decoded_operands
        # self.fetched_operands

        # Raw operands
        self.operands = instruction[1:]
        # Operands to evaluate
        self.to_evaluate = []
        # Evaluated operands
        self.eo = []

        self.result = 0
        self.cycles = 1
        self.finished = False
        self.pc = cpu.program_counter - ( (len(list(filter(None, cpu.decode_unit.pipeline_register)))) - cpu.decode_unit.pipeline_register.index(instruction))
        
    def __repr__(self):
        return self.opcode + " " + " ".join(self.operands)
    
    def decode(self, cpu):
        pass
    
    def reservation_issue(self):
        pass

    def reservation_update(self):
        pass

    # def reservation_operands_available(self):
    #     pass

    def execute(self, cpu):
        pass

    def writeback(self, cpu):
        pass
    
    # def evaluate_params(self, operands):
    #     #change to now instead of evaluating a specified set of 
    #     #things, change operands to be those that are needed to
    #     # be evaluated and evaluate them all
    #     for elem in self.to_evaluate:
    #         valu = 0
    #         if elem.startswith('r'):
    #             valu = REGISTERS[elem]
    #         else:
    #             valu = int(elem)
    #         self.eo.append(valu)
    
    def evaluate_params(self):
        #change to now instead of evaluating a specified set of 
        #things, change operands to be those that are needed to
        # be evaluated and evaluate them all
        # for elem in self.to_evaluate:
        #     valu = 0
        #     if elem.startswith('r'):
        #         valu = REGISTERS[elem]
        #     else:
        #         valu = int(elem)
        #     self.eo.append(valu)
        #
        # Changed again for reservation issue change
        for elem in self.to_evaluate:
            valu = 0
            index = self.to_evaluate.index(elem)
            #maybe account for if eo isnt empty
            if elem.startswith('r'):
                if SCOREBOARD[elem]:
                    valu = REGISTERS[elem]
                    self.to_evaluate[index] = ""
                else:
                    valu = elem
            else:
                valu = int(elem)
                self.to_evaluate[index] = ""

            self.eo.append(valu)
        self.to_evaluate = list(filter(None, self.to_evaluate))


           

class ALUInstruction(Instruction):
    def decode(self, cpu):
        self.eo.append(self.operands[0])
        self.to_evaluate = self.operands[1:]

    def reservation_issue(self):
        SCOREBOARD[self.operands[0]] = 0

    def reservation_update(self):
        SCOREBOARD[self.operands[0]] = 1
    
    def execute(self, cpu):
        pass

    def writeback(self, cpu):
        REGISTERS[self.eo[0]] = self.result

class MEMORYInstruction(Instruction):
    def decode(self, cpu):
        if self.opcode in ["LD", "LDC", "MOV"]:
            self.eo.append(self.operands[0])
            self.to_evaluate = self.operands[1:]

        else:
            self.to_evaluate = self.operands[0:]

    def reservation_issue(self):
        if self.opcode in ["LD", "LDC", "MOV"]:
            SCOREBOARD[self.operands[0]] = 0

    def reservation_update(self):
        if self.opcode in ["LD", "LDC", "MOV"]:
            SCOREBOARD[self.operands[0]] = 1

    def execute(self, cpu):
        pass

    def writeback(self, cpu):
        REGISTERS[self.eo[0]] = self.result

class CONTROLInstruction(Instruction):
    def __init__(self, cpu, instruction):
        super(CONTROLInstruction, self).__init__(cpu, instruction)
        self.cycles = 2

    def decode(self, cpu):
        self.to_evaluate = self.operands[0:]

    def execute(self, cpu):
        pass

        




