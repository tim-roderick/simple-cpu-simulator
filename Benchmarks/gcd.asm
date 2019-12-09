; r1 = a, r2 = b, r10 return address, r15 = d
LDC r1 2000
LDC r2 1000
LDC r15 0

-while1
;while a and b both even
;   if a and b even
;       call mod with a and 2
;           save return address
LDC r10 -re1
;           set r3 = a, r4 = 2
LDC r4 2
MOV r3 r1
;           call mod
J -mod

-re1
;       if r7 is not 0, jump to next while
BNEZ -while2 r7
;       call mod with b and 2
;           save return address
LDC r10 -re2
;           set r3 = a, r4 = 2
;LDC r4 2
MOV r3 r2
;           call mod
J -mod

-re2
;   if r7 is not 0, jump to next while
BNEZ -while2 r7

;   execute code inside while loop 
;       divide a and b by 2
;       add 1 to d
IDIV r5 r1 2
IDIV r6 r2 2
ADDI r11 r15 1
MOV r1 r5
MOV r2 r6
MOV r15 r11
;       jump back to beginning of while
J -while1


-while2
;while a =/= b
;   check a=/=b
CMP r5 r1 r2
BEQZ -end r5
;   execute code in while
;       if a is even
LDC r10 -re3
LDC r4 2
MOV r3 r1
J -mod

-re3
BNEZ -elif1 r7
IDIV r5 r1 2
MOV r1 r5
J -while2

;       else if b is even
-elif1
LDC r10 -re4
LDC r4 2
MOV r3 r2
J -mod

-re4
BNEZ -elif2 r7
IDIV r6 r2 2
MOV r2 r6
J -while2

;       else if a > b 
-elif2
CMP r5 r2 r1
BGEZ -else r5
SUB r6 r1 r2
IDIV r5 r6 2
MOV r1 r5
J -while2

;       else 
-else
SUB r6 r2 r1
IDIV r5 r6 2
MOV r2 r5
J -while2

;mod
;   r7 = r3 mod r4
; = r3 - r4*(r3 // r4)
-mod
IDIV r5 r3 r4
MUL r6 r4 r5
SUB r7 r3 r6
;   jump back to return address
J r10

; let g = a
-end
MOV r30 r1
MOV r31 r15


