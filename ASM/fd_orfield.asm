; ORFIELD.EXE (FD version) text handling assembly.

fullwidthCheck:
    cmp al, 82     ; just the 82 part of the instruction
    jz 5839        ; fullwidthOriginal
    cmp al, 81
    jz 5839


dictEndCheck:
    cmp al, ee
    jnz 5816       ; dictStartCheck
    pop si
    lodsb
    jmp 57de      ; initial text handling code


dictStartCheck:
    cmp al, ef
    jbe 5825       ; overlineCode   ; Must be an unsigned comparison! So use jnb instead of jg
    push si
    mov ah, al
    lodsb
    and ah, 0f
    mov si, 43aa    ; 4c18 for ORBTL
    add si, ax
    lodsb

overlineCode:
    cmp al, 7e
    jnz 5830       ; overlineEndCode
    dec di

overlineEndCode:
    cmp al, 7c
    jnz 585f       ; halfwidthOriginal
    inc di
    xor al, al
    jmp 585f       ; halfwidthOriginal
    nop

fullwidthOriginal:
    mov ah, al
    lodsb
    call 56f3
    mov dx, ax
    call 575a
    push si
    call 5697
    call 5717
    mov si, 0414     ; Makes shadows look good
    call 572d        ; charge of outlines/shadows
    mov ax, [03d6]
    call 5717
    mov si, 03d8
    call 572d        ; Makes text appear on top of shadows
    pop si
    inc di
    inc di
    jmp 588b       ; jumps to the 'jmp 57da' in halfwidthOriginal, since it can't reach 57da with a short jump

halfwidthOriginal:
    mov ah, 09
    xchg al, ah
    mov dx, ax
    call 575a
    push si
    call 5697
    xor ax, ax      ; necessary for fixing weird parens/overline coloring
    call 5717
    mov si, 0414
    call 5743
    mov ax, [03d6]
    call 5717
    mov si, 03d8
    call 5743
    pop si
    inc di
    jmp 57da
"""