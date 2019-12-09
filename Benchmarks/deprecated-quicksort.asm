;SETUP
STC 0 8
STC 1 7
STC 2 6
STC 3 2
STC 4 2
STC 5 3
STC 6 3
STC 7 5

;r1 is base of Array
;r4 SP
;r2 is lo
;r3 is hi
LDC r1 0
LDC r2 0
LDC r3 7
LDC r4 8

;CALL QUICKSORT
ST r1 15 r4
ADDI r4 1
J 16
J 80

;QUICKSORT (line 16)
CMP r14 r2 r3
BGEZ 39 r14
ST r1 21 r4
ADDI r4 1
J 42

;below is line 21
ST r1 r3 r4
ADDI r4 1

ST r1 r15 r4
ADDI r4 1

SUBI r15 1
MOV r3 r15

;Call QUICKSORT
ST r1 30 r4
ADDI r4 1
J 16

;below is line 30
SUBI r4 1
LD r15 r1 r4

SUBI r4 1
LD r3 r1 r4

ADDI r15 1
MOV r2 r15

;Call QUICKSORT
ST r1 39 r4
ADDI r4 1
J 16

;below is line 39
;return 
SUBI r4 1
LD r14 r1 r4
J r14



;PARTITION
;pivot r5 is Array[hi = r3]
;i is r6, j is r7
;r15 return value

;below is line 42
LD r5 r1 r3
MOV r6 r2
MOV r7 r2

CMP r14 r7 r3
SUBI r14 1
BGEZ 59 r14

;below is line 48
LD r8 r1 r7
CMP r14 r8 r5
BGEZ 57 r14
MOV r10 r6
MOV r11 r7
ST r1 56 r4
ADDI r4 1
J 68
ADDI r6 1

;increment loop index
;below is line 57
ADDI r7 1
J 45

MOV r10 r6
MOV r11 r3

ST r1 64 r4
ADDI r4 1
J 68

;below is line 64
MOV r15 r6

;return
SUBI r4 1
LD r14 r1 r4
J r14


;SWAP
; r10, r11 the registers to swap
;below line is 68
LD r12 r1 r10
LD r13 r1 r11
ST r1 r12 r11
ST r1 r13 r10

;return
SUBI r4 1
LD r14 r1 r4
J r14

ADDI r15 0