from .Memory import REGISTERS, MEMORY
import pprint

class CPU():
    def __init__(self,  instructions, labels, fetch_unit, decode_unit, execute_unit, writeback_unit):
        self.program_counter = 0
        self.instruction_cache = instructions
        self.labels = labels
        #self.current_instruction = ""        
        
        self.fetch_unit = fetch_unit
        self.decode_unit = decode_unit
        self.execute_unit = execute_unit
        self.writeback_unit = writeback_unit

        self.all_components = [self.fetch_unit, self.decode_unit, self.execute_unit, self.writeback_unit]

        self.cycle_count = 0
    
    def increment_pc(self):
        self.program_counter += 1

    def increment_cycle(self):
        self.cycle_count += 1    

    def check_done(self):
        return all(component.halt == True for component in self.all_components)

    def iterate(self):
        print(self.fetch_unit.pipeline_register)
        print(self.decode_unit.pipeline_register)
        print(self.execute_unit.pipeline_register)
        print(self.writeback_unit.pipeline_register)
        
        #pipeline
        self.fetch_unit.run(self)
        for i in range(1, len(self.all_components)):
            if self.all_components[i-1].pipeline_register["current"]:
                self.all_components[i].start_unit()
            else:
                self.all_components[i].halt_unit()
            self.all_components[i].run(self)

        for comp in self.all_components:
            comp.advance_state()    

        self.increment_cycle()

    def print_state(self):
        first = ("CURRENT CYCLE: " + str(self.cycle_count) + "  |  "
                 "PC: " + str(self.program_counter) + "  |  ")
                 #"CURRENT INSTRUCTION: " + str(self.decode_unit.pipeline_register["current"].opcode))
        print(first)
        print("\nREGISTERS:")
        pprint.pprint(REGISTERS, compact=True)

        print("\nMEMORY:")
        pprint.pprint(MEMORY, compact=True)

