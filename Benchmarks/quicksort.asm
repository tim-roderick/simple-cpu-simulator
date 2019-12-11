
;r1 is base of Array, r2 is lo, r3 is hi, r4 is SP, r16 is copy slave for r4
LDC r1 0
LDC r2 0
LDC r3 100
MOV r16 r3
ADDI r4 r16 1

;CALL QUICKSORT
ST r1 -re1 r4
MOV r16 r4
ADDI r4 r16 1
J -QUICKSORT

-re1
J -END


-QUICKSORT
CMP r14 r2 r3
BGEZ -re4 r14
ST r1 -re2 r4
MOV r16 r4
ADDI r4 r16 1
J -PARTITION

-re2
ST r1 r3 r4
MOV r16 r4
ADDI r4 r16 1
ST r1 r15 r4
MOV r16 r4
ADDI r4 r16 1
MOV r16 r15
SUBI r15 r16 1
MOV r3 r15

;Call QUICKSORT with lo p-1
ST r1 -re3 r4
MOV r16 r4
ADDI r4 r16 1
J -QUICKSORT

-re3
MOV r16 r4
SUBI r4 r16 1
LD r15 r1 r4
MOV r16 r4
SUBI r4 r16 1
LD r3 r1 r4
MOV r16 r15
ADDI r15 r16 1
MOV r2 r15

;Call QUICKSORT with p+1 hi
ST r1 -re4 r4
MOV r16 r4
ADDI r4 r16 1
J -QUICKSORT

-re4
MOV r16 r4
SUBI r4 r16 1
LD r14 r1 r4
J r14



;pivot r5 is Array[hi = r3]
;i is r6, j is r7
;r15 return value

-PARTITION
LD r5 r1 r3
MOV r6 r2
MOV r7 r2

-pl
CMP r14 r7 r3
MOV r16 r14
SUBI r14 r16 1
BGEZ -afterpl r14

LD r8 r1 r7
CMP r14 r8 r5
BGEZ -incrementloop r14
MOV r10 r6
MOV r11 r7
ST r1 -incrementi r4
MOV r16 r4
ADDI r4 r16 1
J -SWAP

-incrementi
MOV r16 r6
ADDI r6 r16 1

-incrementloop
MOV r16 r7
ADDI r7 r16 1
J -pl

-afterpl
MOV r10 r6
MOV r11 r3

ST r1 -re5 r4
MOV r16 r4
ADDI r4 r16 1
J -SWAP

-re5
MOV r15 r6

MOV r16 r4
SUBI r4 r16 1
LD r14 r1 r4
J r14


; r10, r11 the registers to swap

-SWAP
LD r12 r1 r10
LD r13 r1 r11
ST r1 r12 r11
ST r1 r13 r10

SUBI r16 r4 1
MOV r4 r16
LD r14 r1 r4
J r14

-END
MOV r16 r15
ADDI r15 r16 0