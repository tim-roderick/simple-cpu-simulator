from .component import Component
from cpu.Memory import SCOREBOARD
from isa.Instructions import ALUInstruction as alu
class writeback_unit(Component):
    def add_result(self, result):
        result.finished = True
        self.pipeline_register = self.pipeline_register + [result]
        self.clean()

    def clean(self):
        self.pipeline_register = list(filter(None, self.pipeline_register))

    def run(self, cpu):
        if not self.halt:
            cpu.update_reservation()
            for instruction in self.pipeline_register:
                if cpu.reorder_buffer.is_retirable(cpu, instruction):
                    instruction.writeback(cpu)
                    instruction.reservation_update()
                    #
                    # if str(instruction.eo[0]).startswith('r'):
                    # cpu.update_reservation()
                    #
                    cpu.increment_ie()
                    if instruction in self.pipeline_register:
                        index = self.pipeline_register.index(instruction)
                        self.pipeline_register[index] = ""
            self.clean()

    def flush(self, cpu, instruction):
        self.halt = True
        
        for instruction in self.pipeline_register:
            if instruction not in cpu.reorder_buffer.buffer:
                #
                if isinstance(instruction, alu) or instruction.opcode in ["LD", "LDC", "MOV"]:
                    SCOREBOARD[instruction.operands[0]] = 1
                #
                index = self.pipeline_register.index(instruction)
                self.pipeline_register[index] = ""
        self.clean()

