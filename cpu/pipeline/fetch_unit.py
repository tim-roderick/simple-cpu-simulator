import sys
from .component import Component

class fetch_unit(Component):
    def __init__(self, pipeline_size):
        super(fetch_unit, self).__init__()
        self.halt = False
        self.pipeline_size = pipeline_size
        

    def run(self, cpu):
        if not self.halt:
            for i in range(self.pipeline_size):
                if cpu.program_counter < len(cpu.instruction_cache):
                    if not cpu.decode_unit.is_empty():
                        return
                    
                    if self.add_to_instruction_buffer(cpu, cpu.instruction_cache[cpu.program_counter]):
                        cpu.increment_pc(1)
                else:
                    if cpu.reorder_buffer.is_empty() and cpu.decode_unit.buffer_is_empty():
                        if not any(any(comp.pipeline_register) for comp in cpu.all_components):
                            cpu.shutdown()

            # if cpu.program_counter < len(cpu.instruction_cache):
            #     if not cpu.decode_unit.is_empty():
            #         return

            #     if not cpu.program_counter + self.pipeline_size < len(cpu.instruction_cache):
            #         cpu.decode_unit.set_pipeline_register(cpu.instruction_cache[cpu.program_counter:])
            #     else:
            #         sliceObj = slice(cpu.program_counter, cpu.program_counter+self.pipeline_size)
            #         cpu.decode_unit.set_pipeline_register(cpu.instruction_cache[sliceObj])
            #     cpu.increment_pc(len(cpu.decode_unit.pipeline_register))
            # else:
            #     self.halt_unit()
    
    def add_to_instruction_buffer(self, cpu, instruction):
        for i in range(len(cpu.decode_unit.instruction_buffer)):
            if not cpu.decode_unit.instruction_buffer[i]:
                cpu.decode_unit.instruction_buffer[i] = [instruction, cpu.program_counter]
                return True
        return False
    
    def flush(self, cpu, instruction):
        self.pipeline_register = []
        