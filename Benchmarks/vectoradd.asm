;r1 is base of Array 1, r3 is base of array 2, r3, r4
LDC r4 1000
LDC r15 0
LDC r1 0
LDC r2 1000
LDC r3 2000

-while
CMP r5 r15 r4
BEQZ -end r5
LD r10 r1 r15
LD r11 r2 r15
ADD r6 r10 r11
ST r3 r6 r15
ADDI r14 r15 1
MOV r15 r14
J -while

-end
LDC r31 1337
