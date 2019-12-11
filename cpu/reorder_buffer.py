from cpu.Memory import REGISTERS, MEMORY, SCOREBOARD, RAT
import queue

class reorder_buffer():
    def __init__(self, buffer_size=32):
        self.buffer = [""] * buffer_size
        self.tail = 0
        self.head = 0
        # each entry needs to hold following info
        # i, x, or f | Instruction obj | speculative

    def is_retirable(self, cpu, instruction):
        if instruction in self.buffer:
            index = self.buffer.index(instruction)
            return self.retire_entry(cpu, index)

    
    def retire_entry(self, cpu, index):
        if index == self.tail and self.buffer[index].finished:
            for reg, v in RAT.items():
                if v == "rob"+str(index):
                    RAT[reg] = reg
            self.buffer[index] = ""
            self.move_tail(1)
            # print("\n\n")
            # print(cpu.memory_order_buffer.store_queue)
            cpu.memory_order_buffer.flush(cpu)
            # print(cpu.memory_order_buffer.store_queue)
            # print("\n\n")


            return True
        return False
        # if all previous instructions retired and it has finished
        # move tail 

    def add_entry(self, instruction):
        return_index = self.head
        self.buffer[self.head] = instruction
        #
        

        #
        self.move_head(1)
        return return_index
        # add entry
        # move head

    def move_head(self, num):
        self.head = (self.head + num) % len(self.buffer)
        # move head index by num

    def move_tail(self, num):
        self.tail = (self.tail + num) % len(self.buffer)
        # move head index by num
    
    def distance_to_head(self, instruction):
        distance = 0
        if self.head < self.buffer.index(instruction):
            distance = len(self.buffer) - self.buffer.index(instruction) + self.head
        else:
            distance = self.head - self.buffer.index(instruction)
        return distance
        
    def is_empty(self):
        return not any(self.buffer)
        # move head index by num
    
    def flush(self, instruction, index=None):
        # return_array = []
        new_head = 0
        if not instruction in self.buffer:
            #assume its the tail
            new_head = self.tail
            self.head = self.tail
        else:
            new_head = self.buffer.index(instruction)
            self.head = self.buffer.index(instruction)

        self.buffer[self.head] = ""
        self.move_head(1)

        while self.buffer[self.head] and not self.head == self.tail:
            for addr, v in RAT.items():
                if v == "rob"+str(self.head):
                    copy = self.head
                    value = ""
                    while not self.head == self.tail:
                        self.move_head(-1)
                        if self.buffer[self.head]:
                            if self.buffer[self.head].operands[0] == addr:
                                value = "rob"+str(self.head)
                                break
                    if value:
                        RAT[addr] = value
                    else:
                        RAT[addr] = addr
                    self.head = copy                    
            self.buffer[self.head] = ""
            self.move_head(1)

        
        # TODO flush memory queue, done when this fliush is called in flush_pipeline
        
        
        self.head = new_head
        # return return_array



    
                



    
        
    
    

