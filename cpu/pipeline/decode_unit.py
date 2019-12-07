from isa.opcodes import OPCODES
from isa.Instructions import ALUInstruction, MEMORYInstruction, CONTROLInstruction
from isa.control_instructions import *
from .component import Component
from cpu.Memory import SCOREBOARD, REGISTERS
import copy

class decode_unit(Component): 
    def __init__(self):
        super(decode_unit, self).__init__()
        #For now hardcode 0, 1 to be alu, 2 mem, 3 branch
        # self.pipeline_register = {"current": ["","","",""] , "next": ["","","",""]}
        self.instruction_buffer = [""] * 16
        self.branch_target_buffer = {}

    def is_empty(self):
        return not any(self.pipeline_register)

    def buffer_is_empty(self):
        return not any(self.instruction_buffer)

    def fill(self):
        self.pipeline_register = self.instruction_buffer[:4]
        self.instruction_buffer = self.instruction_buffer[4:]
        self.instruction_buffer.extend([""] * 4)

    def run(self, cpu):
        # dispatch rs
        self.dispatch(cpu)

        if not self.halt:
            if not self.is_empty():
                self.issue(cpu)
                return
            
            self.fill()
            if self.is_empty():
                return
                
            # then issue rs 
            # instructions = []
            for i in range(len(self.pipeline_register)):
                if self.pipeline_register[i]:
                    self.pipeline_register[i][0] = self.pipeline_register[i][0].split(' ')
                    self.pipeline_register[i] = OPCODES[self.pipeline_register[i][0][0]](cpu, self.pipeline_register[i][0], self.pipeline_register[i][1])
                    self.pipeline_register[i].decode(cpu)
                    if self.check_branch(cpu, self.pipeline_register[i], i):
                        return
                #self.pipeline_register["next"]
                # instructions = [instruction] + instructions
            self.issue(cpu)

    # dispatch first then issue
    def dispatch(self, cpu):
        # if empty, bypass and immediately execute
        # for each rs, dispatch
        for unit in cpu.execute_units:
            unit.reservation_station.dispatch()


    def issue(self, cpu):
        #then issue rs 
        

        for i in range(len(self.pipeline_register)):
            instruction = self.pipeline_register[i]
            if not instruction:
                continue

            if isinstance(instruction, ALUInstruction) or instruction.opcode in ["LD", "LDC", "MOV"]:
                if not SCOREBOARD[instruction.operands[0]]:
                    break

            if isinstance(instruction, ALUInstruction):
                if cpu.execute_units[0].reservation_station.issue(instruction, cpu):
                    self.pipeline_register[i] = ""
                else:
                    if cpu.execute_units[1].reservation_station.issue(instruction, cpu):
                        self.pipeline_register[i] = ""
                    else:
                        break
                        #stop issue here to preserve in-order, same for below
                
            elif isinstance(instruction, MEMORYInstruction):
                if cpu.execute_units[2].reservation_station.issue(instruction, cpu):
                    self.pipeline_register[i] = ""
                else:
                    break

            elif isinstance(instruction, CONTROLInstruction):
                if cpu.execute_units[3].reservation_station.issue(instruction, cpu):
                    self.pipeline_register[i] = ""
                else:
                    break
    
    def check_branch(self, cpu, original_instruction, index):
        instruction = copy.deepcopy(original_instruction)

        if isinstance(instruction, CONTROLInstruction):
            if isinstance(instruction, J):
                if any(op.startswith("r") for op in instruction.operands):
                    if instruction.pc in self.branch_target_buffer:
                        print("NOT YET")
                        # self.branch_target_buffer[instruction.pc]
                    else:
                        return False
                    # for op in instruction.to_evaluate:
                    #     # if we don't already have a saved result for this branch in branch target buffer
                    #     # take current value of register ? or maybe don't speculate
                    #     # if we do have result in branch target buffer, use that
                    #     instruction.eo[instruction.eo.index(op)] = REGISTER[op]
                # if instruction.to_evaluate:
                #     print("HM")
                original_instruction.evaluate_params()
                original_instruction.execute(cpu)
                for i in range(index, len(self.pipeline_register)):
                    self.pipeline_register[i] = ""
                return True
        return False
    
    def halt_unit(self):
        self.halt = True
        self.pipeline_register = [""] * 4
        self.instruction_buffer = [""] * 16

