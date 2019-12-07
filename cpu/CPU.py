from .Memory import REGISTERS, MEMORY, SCOREBOARD
from .reorder_buffer import reorder_buffer
import pprint

class CPU():
    def __init__(self,  instructions, labels, fetch_unit, decode_unit, execute_units, writeback_unit):
        self.program_counter = 0
        self.instruction_cache = instructions
        self.labels = labels
        #self.current_instruction = ""        
        
        self.fetch_unit = fetch_unit
        self.decode_unit = decode_unit
        self.execute_units = execute_units
        self.writeback_unit = writeback_unit

        self.reorder_buffer = reorder_buffer()

        self.all_components = [self.fetch_unit, self.decode_unit] + self.execute_units + [self.writeback_unit]

        self.cycle_count = 0
        self.instructions_executed = 0
    
    def increment_pc(self, num=1):
        self.program_counter += num

    def increment_cycle(self):
        self.cycle_count += 1   

    def increment_ie(self):
        self.instructions_executed += 1 

    # def check_halt(self):
    #     if self.fetch_unit.halt and not self.decode_unit.halt:
    #         self.decode_unit.halt_unit()
    #         return

    #     if self.decode_unit.halt and any(unit.halt == False for unit in self.execute_units):
    #         for unit in self.execute_units:
    #             unit.halt_unit()
    #         return

    #     if all(unit.halt == True for unit in self.execute_units) and not self.decode_unit.halt:
    #         self.writeback_unit.halt_unit()
    #         return
        
    #     return False
    
    def check_start(self):
        if not self.fetch_unit.halt and self.decode_unit.halt:
            self.decode_unit.start_unit()
            return

        if not self.decode_unit.halt and any(unit.halt == True for unit in self.execute_units):
            for unit in self.execute_units:
                unit.start_unit()
            return

        if any(unit.halt == False for unit in self.execute_units) and self.writeback_unit.halt:
            self.writeback_unit.start_unit()
            return

        for unit in self.execute_units:
            if not unit.reservation_station.is_empty():
                unit.start_unit()
        
        return False

    # def check_halt(self):
    #     if not self.fetch_unit.halt:
    #         self.decode_unit.start_unit()
    #         return

    #     if not self.decode_unit.halt:
    #         for unit in self.execute_units:
    #             unit.halt_unit()
    #         return

    #     if  not all(unit.halt == True for unit in self.execute_units):
    #         self.writeback_unit.halt_unit()
    #         return
        
    #     return False

    def shutdown(self):
        for comp in self.all_components:
            comp.halt_unit()

    def check_done(self):
        return all(component.halt == True for component in self.all_components)

    def iterate(self, debug=False):
        #pipeline
        # self.check_halt()

        # Writeback
        self.writeback_unit.run(self)
        
        # Execute
        for unit in self.execute_units:
            unit.run(self)

        # Decode
        self.decode_unit.run(self)
            
        # Fetch
        self.fetch_unit.run(self)

        self.check_start()

        # # Decode
        # if self.fetch_unit.pipeline_register["current"]:
        #     self.decode_unit.start_unit()
        # else:
        #     self.decode_unit.halt_unit()
        # self.decode_unit.run(self)

        # # Execute
        # if not self.decode_unit.pipeline_register["current"] == ["", "", "", ""]:
        #     for unit in self.execute_units:
        #         unit.start_unit()
        # else:
        #     for unit in self.execute_units:
        #         unit.halt_unit()
        # for unit in self.execute_units:
        #     unit.run(self)
        
        # # Writeback
        
        # if any(map(lambda unit: unit.pipeline_register["current"], self.execute_units)):
        #     self.writeback_unit.start_unit()
        # else:
        #     self.writeback_unit.halt_unit()
        # self.writeback_unit.run(self)


        # for unit in self.all_components:
        #     unit.advance_state()

        self.increment_cycle()
        if debug:
            self.print_state()
            input("Press ENTER to continue... ")

    def flush_pipeline(self, instruction):
        self.reorder_buffer.flush(instruction)

        for comp in self.all_components:
            comp.flush(self, instruction)
    
    def update_reservation(self, instruction):
        for unit in self.execute_units:
            unit.update_reservation(instruction)
        
    
    def print_state(self, final=False):
        if final:    
            stats = ("CYCLE COUNT: " + str(self.cycle_count) + "  |  "
                    "INSTRUCTIONS EXECUTED: " + str(self.instructions_executed) + "  |  "
                    "INSTRUCTIONS PER CYCLE: " + str(self.instructions_executed / self.cycle_count))
        else:
            stats = ("CURRENT CYCLE: " + str(self.cycle_count) + "  |  "
                    "PC: " + str(self.program_counter) + "  |  ")
            
            data = {"Component": [], "Halted": [], "Pipeline Register": []}
            
            for comp in self.all_components[0:2]:
            #     data["Component"].append(comp.__class__.__name__)
            #     data["Halted"].append(str(comp.halt))
            #     data["Pipeline Register"].append(comp.pipeline_register)
                
            #     pprint.pprint(data, compact=True)
                print(comp.__class__.__name__ + "  |  " + str(comp.halt))
                pprint.pprint(comp.pipeline_register, compact=True)
            
            for unit in self.execute_units:
                print(unit.__class__.__name__ + "  |  " + str(unit.halt))
                pprint.pprint(unit.pipeline_register, compact=True)
                pprint.pprint(unit.reservation_station.reservation, compact=True)
            
            print(self.writeback_unit.__class__.__name__ + "  |  " + str(self.writeback_unit.halt))
            pprint.pprint(self.writeback_unit.pipeline_register, compact=True)
                    
        print("\n" + stats)
        
        print("\nINSTRUCTION BUFFER:")

        pprint.pprint(self.decode_unit.instruction_buffer, compact=True)

        print("\nREORDER BUFFER:")
        print(f"TAIL:{self.reorder_buffer.tail} HEAD:{self.reorder_buffer.head}")
        pprint.pprint(self.reorder_buffer.buffer, compact=True)

        print("\n|  REGISTER  |  VALUE  |  SCOREBOARD  |")
        for state in REGISTERS:
            if len(str(state)) > 2:
                print(f"|     {state}    |    {REGISTERS[str(state)]}    |      {SCOREBOARD[str(state)]}       |")
            else:
                print(f"|     {state}     |    {REGISTERS[str(state)]}    |      {SCOREBOARD[str(state)]}       |")

        # pprint.pprint(REGISTERS, compact=True)

        # print("\nSCOREBOARD:")
        # pprint.pprint(SCOREBOARD, compact=True)

        print("\nMEMORY:")
        pprint.pprint(MEMORY, compact=True)


