from isa.opcodes import OPCODES
from .component import Component

class decode_unit(Component):   
    def run(self, cpu):
        if not self.halt:
            instruction = cpu.fetch_unit.pipeline_register["current"].split(' ')
            instruction = OPCODES[instruction[0]](cpu, instruction)
            instruction.decode(cpu)
            self.pipeline_register["next"] = instruction