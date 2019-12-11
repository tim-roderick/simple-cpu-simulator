import sys
from cpu import CPU
from assembler import assemble
from cpu.pipeline import fetch_unit, decode_unit, execute_unit, writeback_unit
from Benchmarks.memory_initialisation import INITIALISATION
from cpu.Memory import MEMORY

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
    if sys.argv[1][11:] in INITIALISATION:
        MEMORY[:] = INITIALISATION[sys.argv[1][11:]]
    i = 0
    while not cpu.check_done():
        cpu.iterate(debug) 
        # i += 1
        # if i == 3000:
        #     debug = True
        
    cpu.print_state(True) 

