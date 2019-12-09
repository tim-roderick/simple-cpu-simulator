from cpu.Memory import REGISTERS, MEMORY, SCOREBOARD
from isa.Instructions import ALUInstruction as aluclass

class reservation_station():
    def __init__(self, execute_unit):
        # instructio, VS1, VS2
        self.reservation = [""] * 3 
        # self.reservation = [
        #     ["",1,1],
        #     ["",1,1],
        #     ["",1,1]
        # ]

        self.execute_unit = execute_unit

    def is_empty(self):
        # return not any(reservation[0] for reservation in self.reservation)
        return self.reservation == [""] * 3
    
    def is_full(self):
        # return all(reservation[0] for reservation in self.reservation)
        return all(self.reservation)

    def clean_queue(self):
        # self.reservation = list(filter(lambda res: res[0], self.reservation))
        # self.reservation.extend([
        #     ["",1,1],
        #     ["",1,1],
        #     ["",1,1]
        # ])
        self.reservation = list(filter(None, self.reservation))
        self.reservation.extend([""] * (3 - len(self.reservation)))

    def issue(self, instruction, cpu):
        #recieve instr into reservation
        for i in range(len(self.reservation)):
            if not self.reservation[i]:
                #
                instruction.evaluate_params()
                #
                self.reservation[i] = instruction
                instruction.reservation_issue()

                # CHANGED reservation_issue
                # We now want to 
                # set v bit or destination like before
                # get values of registers at current time
                # if scoreboard bit isnt set, replace with eg "r1"
                
                # add instruction to reorder buffer
                cpu.reorder_buffer.add_entry(instruction)
                return True
        return False
              
    def check_operand_availability(self, instruction):
        # #check if an instruction has all the source operands available
        # if not instruction:
        #     return False

        # # if instruction.opcode in ["ADDI", "SUBI", "LDC"]:
        # #     return True

        # for operand in instruction.to_evaluate:
        #     #skip immediates
        #     if not operand.startswith("r"):
        #         continue

        #     if not SCOREBOARD[operand]:
        #         #check if we can bypass store, also this may be register renaming...
        #         # if self.check_bypass():
        #         return False
        # return True           
        
        #CHANGED FOR NEW RES
        #check if an instruction has all the source operands available
        if not instruction:
            return False
            
        if instruction.to_evaluate:
            return False
        return True           

    def dispatch(self):
        if self.execute_unit.busy or self.execute_unit.halt:
            return False
        
        #dispatch instr to execute unit
        for i in range(len(self.reservation)):
            if self.check_operand_availability(self.reservation[i]):
                # print(self.reservation[i])
                # print(self.execute_unit.pipeline_register)
                # print("WHY GOD WHY")
                # self.reservation[i].evaluate_params()
                self.execute_unit.pipeline_register = self.reservation[i]
                
                # self.execute_unit.pipeline_register.reservation_issue()
                self.reservation[i] = ""

                # print("\n\n\n\n\n\n\n")
                # print(self.reservation[i])
                # print(self.execute_unit.pipeline_register)
                # print("WHY GOD WHY")
                self.clean_queue()
                break
                



    
        
    
    

