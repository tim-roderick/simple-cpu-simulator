class Component:
    def __init__(self):
        self.pipeline_register = {
            "current": "",
            "next": ""
        }
        
        self.halt = False

    def advance_state(self):
        self.pipeline_register["current"] = self.pipeline_register["next"]
    
    def run(self, cpu):
        pass

    def halt_unit(self):
        self.halt = True
        self.pipeline_register["next"] = ""

    def start_unit(self):
        self.halt = False