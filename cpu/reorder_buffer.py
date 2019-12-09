from cpu.Memory import REGISTERS, MEMORY, SCOREBOARD
import queue

class reorder_buffer():
    def __init__(self, buffer_size=32):
        self.buffer = [""] * buffer_size
        self.tail = 0
        self.head = 0
        # each entry needs to hold following info
        # i, x, or f | Instruction obj | speculative

    def is_retirable(self, instruction):
        if instruction in self.buffer:
            index = self.buffer.index(instruction)
            return self.retire_entry(index)

    
    def retire_entry(self, index):
        # Shouldnt need and self.buffer[index].state() == FINISHED as its in writeback meaning it should always be finished
        if index == self.tail and self.buffer[index].finished:
            self.buffer[index] = ""
            self.move_tail(1)
            return True
        return False
        # if all previous instructions retired and it has finished
        # move tail 

    def add_entry(self, instruction):
        self.buffer[self.head] = instruction
        self.move_head(1)
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
    
    def flush(self, instruction):
        # return_array = []
        new_head = self.buffer.index(instruction)
        self.head = self.buffer.index(instruction)

        self.buffer[self.head] = ""
        self.move_head(1)

        while self.buffer[self.head] and not self.head == self.tail:
            self.buffer[self.head] = ""
            self.move_head(1)

        self.head = new_head
        # return return_array



    
                



    
        
    
    

