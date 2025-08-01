default rel
extern printf
global main

section .data
    start_value dq 27                        ; ← Modifie ici
    fmt_title   db === Suite de Collatz pour %lld ===, 10, 0
    fmt_step    db Etape %lld  %lld, 10, 0
    fmt_final1  db Nombre total d'etapes  %lld, 10, 0
    fmt_final2  db Valeur maximale atteinte  %lld, 10, 0

section .bss
    stack      resq 1000                     
    step_count resq 1
    maxval     resq 1

section .text

main
    push rbp
    mov rbp, rsp
    sub rsp, 32              

    lea rcx, [fmt_title]
    mov rdx, [start_value]
    call printf
    mov rcx, [start_value]
    call collatz
    lea rcx, [fmt_final1]
    mov rdx, [step_count]
    call printf
    lea rcx, [fmt_final2]
    mov rdx, [maxval]
    call printf

    mov rsp, rbp
    pop rbp
    xor eax, eax
    ret

collatz
    push rbp
    mov rbp, rsp
    sub rsp, 32

    mov rbx, rcx             
    mov [maxval], rbx
    xor rdx, rdx
    mov [step_count], rdx

.loop
    mov rdx, [step_count]
    lea rcx, [fmt_step]
    mov r8, rdx               
    mov r9, rbx               
    call printf

    mov rax, [step_count]
    mov rcx, rax
    mov rax, rbx
    mov [stack + rcx8], rax
    cmp rbx, 1
    je .done
    mov rax, [step_count]
    inc rax
    mov [step_count], rax
    mov rax, [maxval]
    cmp rbx, rax
    jle .skip_max
    mov [maxval], rbx
.skip_max
    test rbx, 1
    jz .even
    imul rbx, rbx, 3
    add rbx, 1
    jmp .loop

.even
    shr rbx, 1
    jmp .loop

.done
    leave
    ret
