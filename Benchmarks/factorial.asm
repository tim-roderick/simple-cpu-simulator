;Starts with r1 = n > 1
LDC r1 5
MOV r2 r1

;loop
SUBI r2 1
MUL r3 r2 r1
MOV r1 r3
CMP r9 r2 1
BNEZ 2 r9
