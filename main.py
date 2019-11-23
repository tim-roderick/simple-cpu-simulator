import sys
from cpu import CPU
from assembler import assemble
from cpu.pipeline import fetch_unit, decode_unit, execute_unit, writeback_unit

if len(sys.argv) != 2:
    sys.exit()
else:
    instructions, labels = assemble(sys.argv[1])
    
    fu = fetch_unit.fetch_unit()
    du = decode_unit.decode_unit()
    eu = execute_unit.execute_unit()
    wu = writeback_unit.writeback_unit()

    cpu = CPU.CPU(instructions, labels, fu, du, eu, wu)

    while not cpu.check_done():
        cpu.iterate() 
    cpu.print_state() 

