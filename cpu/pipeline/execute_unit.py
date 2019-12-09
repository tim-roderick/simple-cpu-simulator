from .component import Component
from .reservation_station import reservation_station
from isa.Instructions import CONTROLInstruction as branch, ALUInstruction
from cpu.Memory import SCOREBOARD

class execute_unit(Component):
    def __init__(self):

        super(execute_unit, self).__init__()
        
        self.cycles_left = 0
        self.busy = False

        self.reservation_station = reservation_station(self)

    def run(self, cpu):
        if not self.halt:
            if self.busy:
                if self.cycle():
                    return
                else:
                    if self.pipeline_register: 
                        self.execute_instruction(cpu)
            
            if self.pipeline_register:
                self.cycles_left = self.pipeline_register.cycles-1

                if self.cycles_left == 0:
                    self.execute_instruction(cpu)
                    # if isinstance(self.pipeline_register, branch):
                    #     self.pipeline_register.execute(cpu)
                    #     cpu.flush_pipeline(self.pipeline_register)
                    #     return

                    # self.pipeline_register.execute(cpu)
                    # #
                    # if str(self.pipeline_register.eo[0]).startswith('r'):
                    #     cpu.update_reservation(self.pipeline_register)
                    # #
                    # cpu.writeback_unit.add_result(self.pipeline_register)
                    # self.pipeline_register = []
                else: 
                    self.busy = True
                
    #if self.eo[0] starts with r then its a dest one
    def cycle(self):
        if self.cycles_left == 1:
            self.busy = False
        else:
            self.cycles_left -= 1
        return self.busy 
    
    def execute_instruction(self, cpu):
        if isinstance(self.pipeline_register, branch):
            self.pipeline_register.execute(cpu)
            # add pc, operand values to branch_target_buffer
            cpu.flush_pipeline(self.pipeline_register)
            cpu.flushed_count += 1
            return

        self.pipeline_register.execute(cpu)
        #
        if str(self.pipeline_register.eo[0]).startswith('r'):
            cpu.update_reservation(cpu, self.pipeline_register)
        #
        
        cpu.writeback_unit.add_result(self.pipeline_register)
        self.pipeline_register = []
        
    def flush(self, cpu, instruction):
        #self.halt_unit()
        self.halt = True
    #################################
        if self.pipeline_register:
            if self.pipeline_register not in cpu.reorder_buffer.buffer:    
                #
                if isinstance(self.pipeline_register, ALUInstruction) or self.pipeline_register.opcode in ["LD", "LDC", "MOV"]:
                    SCOREBOARD[self.pipeline_register.operands[0]] = 1
                #
                self.pipeline_register = []
    ##########################
        for instruction in self.reservation_station.reservation:
            if instruction not in cpu.reorder_buffer.buffer:
                #
                if isinstance(instruction, ALUInstruction) or instruction.opcode in ["LD", "LDC", "MOV"]:
                    SCOREBOARD[instruction.operands[0]] = 1
                #
                index = self.reservation_station.reservation.index(instruction)
                self.reservation_station.reservation[index] = ""
        self.reservation_station.clean_queue()

    def update_reservation(self, cpu, instruction):
        # print(instruction.eo[0], instruction.result, instruction.operands)
        last_instr = None
        for instr in cpu.reorder_buffer.buffer:
            if not instr:
                continue

            if instruction in cpu.reorder_buffer.buffer:
                if cpu.reorder_buffer.distance_to_head(instr) > cpu.reorder_buffer.distance_to_head(instruction):
                    continue

            if isinstance(instr, ALUInstruction) or instr.opcode in ["LD", "LDC", "MOV"]:
                if instr.operands[0] == instruction.eo[0]:
                    last_instr = instr
                    break

        for elem in self.reservation_station.reservation:
            if not elem:
                continue

            # if not last_instr == None:
            #     if not cpu.reorder_buffer.distance_to_head(elem) > cpu.reorder_buffer.distance_to_head(last_instr):
            #         continue

            # # if index of instruction is closer to head than elem return
            # if instruction in cpu.reorder_buffer.buffer:
            #     if cpu.reorder_buffer.distance_to_head(instruction) < cpu.reorder_buffer.distance_to_head(elem):
            #         continue
                
            if instruction.eo[0] in elem.to_evaluate:
                i = elem.to_evaluate.index(instruction.eo[0])
                j = elem.eo.index(instruction.eo[0])

                elem.to_evaluate[i] = ""
                elem.eo[j] = instruction.result
            elem.to_evaluate = list(filter(None, elem.to_evaluate))

            
        # self.reservation_station.clean_queue()
    