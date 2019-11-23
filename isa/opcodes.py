from .alu_instructions import *
from .memory_instructions import *
from .control_instructions import *

OPCODES = {
    # * Means a general purpose register 
    # @ means a registers to write to
    # $ Means an constant operand
    # MEM[] Means a location in memory
    # {} Are special registers: PC,
    # TYPE R ~ |OPC| * | */$ | */$ |
    # TYPE I ~ |OPC| */$   |  */$  |
    # TYPE J ~ |OPC|      */$      |  
    
    # Arithmetic, comparisons and logic
    "ADD" : ADD,  # | ADD  | @dest | *src1 | *src2 |  ->  @dest = *src1 + *src2   
    "ADDI": ADDI, # | ADDI | @dest | $valu |          ->  @dest = *dest + $valu 
    "SUB" : SUB,  # | SUB  | @dest | *src1 | *src2 |  ->  @dest = *src1 - *src2 
    "SUBI": SUBI, # | SUBI | @dest | $valu |          ->  @dest = *dest - $valu
    "MUL" : MUL,  # | MUL  | @dest | *src1 | *src2 |  ->  @dest = *src1 * *src2   
    "DIV" : DIV,  # | DIV  | @dest | *src1 | *src2 |  ->  @dest = *src1 / *src2 
    "CMP" : CMP,  # | CMP  | @dest | *src1 | *src2 |  ->  @dest = 1, 0, -1 IF *src1 >/=/< *src2

    # Memory access
    "LD"  : LD,   # | LD   | @dest | *addr | *offs |  ->  @dest = MEM[*addr + *offs]
    "LDC" : LDC,  # | LDC  | @dest | $valu |          ->  @dest = $valu
    "MOV" : MOV,  # | MOV  | @dest | *src  |          ->  @dest = *src  
    "ST"  : ST,   # | ST   | *addr | *src  | *offs |  ->  MEM[*addr + *offs] = *src  
    "STC" : STC,  # | STC  | *addr | $valu |          ->  MEM[*addr] = $valu 

    # Branches and Jumps
    "J"   : J,    # | J    | *addr |                  ->  {PC} = *addr  
    "BEQZ": BEQZ, # | BEQZ | *addr | *src  |          ->  {PC} = *addr IF *src = 0
    "BNEZ": BNEZ, # | BNEZ | *addr | *src  |          ->  {PC} = *addr IF *src != 0
    "BLTZ": BLTZ, # | BLTZ | *addr | *src  |          ->  {PC} = *addr IF *src < 0 
    "BGEZ": BGEZ  # | BGEZ | *addr | *src  |          ->  {PC} = *addr IF *src >= 0
}