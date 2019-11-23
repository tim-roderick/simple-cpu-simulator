from .component import Component

class writeback_unit(Component):
    def run(self, cpu):
        if not self.halt:
            self.pipeline_register["next"] = cpu.execute_unit.pipeline_register["current"]
            self.pipeline_register["next"].writeback(cpu)