from .component import Component

class execute_unit(Component):
    def run(self, cpu):
        if not self.halt:
            self.pipeline_register["next"] = cpu.decode_unit.pipeline_register["current"]
            self.pipeline_register["next"] .execute(cpu)
    