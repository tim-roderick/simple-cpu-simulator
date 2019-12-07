import sys
from cpu import CPU
from assembler import assemble
from cpu.pipeline import fetch_unit, decode_unit, execute_unit, writeback_unit

if len(sys.argv) < 2:
    sys.exit()
else:
    debug = False
    if len(sys.argv) > 2:
        debug = sys.argv[2] == "debug"

    instructions, labels = assemble(sys.argv[1])
    
    eus = [execute_unit.execute_unit(), execute_unit.execute_unit(), execute_unit.execute_unit(), execute_unit.execute_unit()]
    fu = fetch_unit.fetch_unit(len(eus))
    du = decode_unit.decode_unit()
    wu = writeback_unit.writeback_unit()

    cpu = CPU.CPU(instructions, labels, fu, du, eus, wu)
    
    while not cpu.check_done():
        cpu.iterate(debug) 
    cpu.print_state(True) 

