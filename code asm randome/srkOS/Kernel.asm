[org 0x0000]
bits 16

%define VIDEO_MEM 0xB800
%define MAX_INPUT 80
%define MAX_FILES 5
%define MAX_NAME 15
%define MAX_CONTENT 80

section .bss
input_buffer resb MAX_INPUT
files resb MAX_FILES * (MAX_NAME + MAX_CONTENT + 2)

section .text

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    sti

    mov si, input_buffer
    mov cx, 0
    mov di, files
    mov word [file_count], 0

    call enable_cursor

.main_loop:
    call read_key
    cmp al, 0x0D
    je .handle_enter
    cmp al, 0x08
    je .handle_backspace
    cmp al, 32
    jb .main_loop
    cmp al, 126
    ja .main_loop
    mov ah, 0x0E
    int 0x10
    cmp cx, MAX_INPUT
    jae .main_loop
    mov [si], al
    inc si
    inc cx
    jmp .main_loop

.handle_enter:
    mov byte [si], 0
    mov ax, 0
    mov [file_read], ax
    mov si, input_buffer
    mov cx, 0

    mov di, input_buffer
    call check_cls
    cmp ax, 1
    je .clear_screen

    mov di, input_buffer
    call parse_dir
    cmp ax, 1
    je .main_loop

    mov di, input_buffer
    call parse_ldt
    cmp ax, 1
    je .main_loop

    mov di, input_buffer
    call parse_tre
    cmp ax, 1
    je .main_loop

    jmp .main_loop

.handle_backspace:
    cmp cx, 0
    je .main_loop
    dec si
    dec cx
    mov ah, 0x0E
    mov al, 0x08
    int 0x10
    mov al, ' '
    int 0x10
    mov al, 0x08
    int 0x10
    jmp .main_loop

.clear_screen:
    mov ax, 0x0600
    mov bh, 0x07
    mov cx, 0
    mov dx, 0x184F
    int 0x10
    mov dx, 0x0000
    mov ah, 0x02
    int 0x10
    jmp .main_loop

read_key:
    mov ah, 0x00
    int 0x16
    ret

enable_cursor:
    mov dx, 0x03D4
    mov al, 0x0A
    out dx, al
    inc dx
    in al, dx
    and al, 0xC0
    or al, 0x0F
    out dx, al
    dec dx
    mov al, 0x0B
    out dx, al
    inc dx
    in al, dx
    and al, 0xE0
    or al, 0x0F
    out dx, al
    ret

strcmp:
    xor ax, ax
.next_char:
    mov al, [di]
    mov dl, [si]
    cmp al, dl
    jne .notequal
    cmp al, 0
    je .equal
    inc di
    inc si
    jmp .next_char
.notequal:
    mov ax, 1
    ret
.equal:
    ret

strncmp:
    xor ax, ax
.next_char2:
    cmp bx, 0
    je .equal2
    mov al, [di]
    mov dl, [si]
    cmp al, dl
    jne .notequal2
    cmp al, 0
    je .equal2
    inc di
    inc si
    dec bx
    jmp .next_char2
.notequal2:
    mov ax, 1
    ret
.equal2:
    ret

check_cls:
    mov di, cls_str
    mov si, input_buffer
    mov bx, 3
    call strncmp
    ret

parse_dir:
    mov ax, 0
    mov si, input_buffer
    mov di, dir_str
    mov bx, 4
    call strncmp
    cmp ax, 1
    jne .not_dir
    mov ax, 1
    call handle_dir
    ret
.not_dir:
    mov ax, 0
    ret

parse_ldt:
    mov ax, 0
    mov si, input_buffer
    mov di, ldt_str
    mov bx, 4
    call strncmp
    cmp ax, 1
    jne .not_ldt
    mov ax, 1
    call handle_ldt
    ret
.not_ldt:
    mov ax, 0
    ret

parse_tre:
    mov ax, 0
    mov si, input_buffer
    mov di, tre_str
    mov bx, 3
    call strncmp
    cmp ax, 1
    jne .not_tre
    mov ax, 1
    call handle_tre
    ret
.not_tre:
    mov ax, 0
    ret

handle_dir:
    mov si, input_buffer
    add si, 4
    call extract_name
    cmp ax, 0
    je .fail_dir
    mov cx, ax
    mov bx, si

    call extract_content
    cmp ax, 0
    je .fail_dir

    call save_file
    ret
.fail_dir:
    ret

handle_ldt:
    mov si, input_buffer
    add si, 4
    call extract_name
    cmp ax, 0
    je .fail_ldt

    call print_file_content
    ret
.fail_ldt:
    ret

handle_tre:
    mov cx, [file_count]
    cmp cx, 0
    je .tre_no_files
    mov bx, 0
.list_loop:
    mov si, files
    mov dx, MAX_NAME + MAX_CONTENT + 2
    mul bx
    add si, ax
    call print_file_name
    inc bx
    cmp bx, cx
    jne .list_loop
    ret
.tre_no_files:
    mov si, no_files_msg
    call print_string
    ret

extract_name:
    mov di, 0
    mov bx, si
    mov dx, 0
.next_char_name:
    mov al, [bx]
    cmp al, '_'
    je .end_name
    cmp al, 0
    je .fail_name
    cmp dx, MAX_NAME
    jae .fail_name
    mov [name_buffer + dx], al
    inc dx
    inc bx
    jmp .next_char_name
.end_name:
    mov byte [name_buffer + dx], 0
    mov ax, dx
    mov si, bx
    inc si
    ret
.fail_name:
    mov ax, 0
    ret

extract_content:
    mov dx, 0
    mov bx, si
.next_char_content:
    mov al, [bx]
    cmp al, 0
    je .end_content
    cmp dx, MAX_CONTENT
    jae .end_content
    mov [content_buffer + dx], al
    inc dx
    inc bx
    jmp .next_char_content
.end_content:
    mov byte [content_buffer + dx], 0
    mov ax, dx
    ret

save_file:
    mov cx, [file_count]
    cmp cx, MAX_FILES
    jae .fail_save
    mov di, files
    mov bx, cx
    mov dx, MAX_NAME + MAX_CONTENT + 2
    mul dx
    add di, ax

    mov si, name_buffer
    mov di, di
.copy_name:
    mov al, [si]
    mov [di], al
    inc si
    inc di
    cmp al, 0
    jne .copy_name

    mov si, content_buffer
.copy_content:
    mov al, [si]
    mov [di], al
    inc si
    inc di
    cmp al, 0
    jne .copy_content

    inc word [file_count]
    ret
.fail_save:
    ret

print_file_content:
    mov cx, [file_count]
    cmp cx, 0
    je .not_found
    mov bx, 0
.search_loop:
    mov si, files
    mov dx, MAX_NAME + MAX_CONTENT + 2
    mul bx
    add si, ax
    mov di, si
    call strcmp_file_name
    cmp ax, 0
    je .found_file
    inc bx
    cmp bx, cx
    jne .search_loop
.not_found:
    mov si, err_nf
    call print_string
    ret
.found_file:
    add si, MAX_NAME + 1
    call print_string
    ret

strcmp_file_name:
    xor ax, ax
.next_char_file:
    mov al, [di]
    mov dl, [si]
    cmp al, dl
    jne .notequal_file
    cmp al, 0
    je .equal_file
    inc di
    inc si
    jmp .next_char_file
.notequal_file:
    mov ax, 1
    ret
.equal_file:
    ret

print_file_name:
    mov ah, 0x0E
.print_loop_name:
    lodsb
    or al, al
    jz .print_done_name
    int 0x10
    jmp .print_loop_name
.print_done_name:
    mov al, 0x0D
    int 0x10
    mov al, 0x0A
    int 0x10
    ret

print_string:
    mov ah, 0x0E
.print_loop_str:
    lodsb
    or al, al
    jz .print_done
    int 0x10
    jmp .print_loop_str
.print_done:
    ret

cls_str db "cls",0
dir_str db "dir_",0
ldt_str db "ldt_",0
tre_str db "tre",0
file_count dw 0
file_read dw 0
name_buffer times MAX_NAME+1 db 0
content_buffer times MAX_CONTENT+1 db 0
err_nf db "Fichier non trouve",0
no_files_msg db "Aucun fichier existant",0
