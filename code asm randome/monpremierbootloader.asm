[org 0x7C00]
bits 16

start:
    mov si, message
.print_loop:
    lodsb
    or al, al
    jz .hang
    mov ah, 0x0E
    int 0x10
    jmp .print_loop

.hang:
    jmp $

message db "SrkOS", 0

times 510 - ($ - $$) db 0
dw 0xAA55