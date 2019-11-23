import sys
from .component import Component

class fetch_unit(Component):
    def run(self, cpu):
        if not self.halt:
            if cpu.program_counter < len(cpu.instruction_cache):
                self.pipeline_register["next"] = cpu.instruction_cache[cpu.program_counter]
                cpu.increment_pc()
            else:
                self.halt_unit()
        