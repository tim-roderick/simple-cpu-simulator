class memory_order_buffer():
    def __init__(self, buffer_size=8):
        # self.load_queue = {}
        self.store_queue = {}
        self.load_queue = {}
        # each entry needs to hold following info
        # i, x, or f | Instruction obj | speculative

    # def is_retirable(self, instruction):
    #     if instruction in self.buffer:
    #         index = self.buffer.index(instruction)
    #         return self.retire_entry(index)

    
    # def retire_entry(self, index):
    #     # Shouldnt need and self.buffer[index].state() == FINISHED as its in writeback meaning it should always be finished
    #     if index == self.tail and self.buffer[index].finished:
    #         for reg, v in RAT.items():
    #             if v == "rob"+str(index):
    #                 RAT[reg] = reg
    #         self.buffer[index] = ""
    #         self.move_tail(1)
    #         return True
    #     return False
    #     # if all previous instructions retired and it has finished
    #     # move tail 

    def add_to_store(self, cpu, instruction):
        index = cpu.reorder_buffer.buffer.index(instruction)
        memory_address = 0
        if instruction.opcode == "ST":
            memory_address = instruction.eo[0] + instruction.eo[2] 
        elif instruction.opcode == "STC":
            memory_address = instruction.eo[0]
        else:
            print("Error")

        self.store_queue[index] = memory_address

        # for key, v in self.load_queue.items():
        #     forward = self.get_latest_store(cpu, v, key)
        #     if forward:
        #         cpu.reorder_buffer.buffer[key].result = cpu.reorder_buffer.buffer[forward].result
        # print(self.store_queue)
    
    def add_to_load(self, cpu, instruction):
        index = cpu.reorder_buffer.buffer.index(instruction)
        memory_address = 0
        if instruction.opcode == "LD":
            memory_address = instruction.eo[1] + instruction.eo[2]
        else:
            print("Error")

        self.load_queue[index] = memory_address

        forward = self.get_latest_store(cpu, memory_address, index)
        if forward:
            cpu.reorder_buffer.buffer[index].result = cpu.reorder_buffer.buffer[forward].result
    
    def remove_from_store(self, rob_index):
        self.store_queue.pop(rob_index, None)
    
    def remove_from_load(self, rob_index):
        self.load_queue.pop(rob_index, None)

    def get_latest_store(self, cpu, address, rob_index):
        current_min = None
        for index, addr in self.store_queue.items():
            if addr == address:
                print("OH")
                if cpu.reorder_buffer.distance_to_head(cpu.reorder_buffer.buffer[rob_index]) < cpu.reorder_buffer.distance_to_head(cpu.reorder_buffer.buffer[index]):
                    print("OH2")
                    if current_min == None:
                        current_min = index
                    else:
                        if cpu.reorder_buffer.distance_to_head(cpu.reorder_buffer.buffer[index]) < cpu.reorder_buffer.distance_to_head(cpu.reorder_buffer.buffer[current_min]):
                            current_min = index
        if current_min == None:
            return False
        else:
            return current_min

        # add entry
        # move head

    # def move_head(self, num):
    #     self.head = (self.head + num) % len(self.buffer)
    #     # move head index by num

    # def move_tail(self, num):
    #     self.tail = (self.tail + num) % len(self.buffer)
    #     # move head index by num
    
    # def distance_to_head(self, instruction):
    #     distance = 0
    #     if self.head < self.buffer.index(instruction):
    #         distance = len(self.buffer) - self.buffer.index(instruction) + self.head
    #     else:
    #         distance = self.head - self.buffer.index(instruction)
    #     return distance
        
    # def is_empty(self):
    #     return not any(self.buffer)
    #     # move head index by num
    
    def flush(self, cpu):
        to_remove_store = []
        to_remove_load = []
        for key, value in self.store_queue.items():
            if not cpu.reorder_buffer.buffer[key]:
                to_remove_store.append(key)

        for key, value in self.load_queue.items():
            if not cpu.reorder_buffer.buffer[key]:
                to_remove_load.append(key)
        
        for key in to_remove_store:
            self.remove_from_store(key)

        for key in to_remove_load:
            self.remove_from_load(key)
        # return return_array