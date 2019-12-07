class Component:
    def __init__(self):
        self.pipeline_register = []
        self.halt = True

    # def advance_state(self):
    #     self.pipeline_register["current"] = self.pipeline_register["next"]

    # def check_halt(self):
    #     if self.pipeline_register
    
    def run(self, cpu):
        pass

    def halt_unit(self):
        if not self.halt:
            self.halt = True
            self.pipeline_register = []

    def start_unit(self):
        self.halt = False

    def set_pipeline_register(self, value):
        self.pipeline_register = value

    def flush(self, cpu, instruction):
        self.halt_unit()