; ORFIELD.EXE (CD version) text handling assembly.

cd_fullwidthCheck:
    cmp al, 81
    jz 5834      ; cd_fullwidthOriginal
    cmp al, 82
    jz 5834      ; cd_fullwidthOriginal


cd_dictEndCheck:
    cmp al, ee
    jnz 5814      ; dict_start_check
    pop si
    lodsb
    jmp 57d8      ; beginning of text handling loop, 'lodsb'



cd_dictStartCheck:
    cmp al, ef
    jbe 5825
    push si
    mov ah, al
    lodsb
    and ah, 0f
    mov si, 43d0
    add si, ax
    lodsb


cd_overlineCode:
    cmp al, 7e
    jnz 582a
    dec di

cd_overlineEndCode:
    cmp al, 7c
    jnz 585f       ; cd_halfwidthOriginal
    inc di
    xor al, al
    jmp 585f       ; cd_halfwidthOriginal
    nop

cd_fullwidthOriginal:
    mov ah, al
    lodsb
    call 56ed
    mov dx, ax
    call 5754
    push si
    call 5691
    xor ax, ax
    call 5711
    mov si, 0414
    call 5727
    mov ax, [03d6]
    call 5711
    mov si, 03d8
    call 5727
    pop si
    inc di
    inc di
    jmp 5885

cd_halfwidthOriginal:
    mov ah, 09
    xchg al, ah
    mov dx, ax
    call 5754
    push si
    call 5691
    xor ax, ax
    call 5711
    mov si, 0414
    call 573d
    mov ax, [03d6]
    call 5711
    mov si, 03d8
    call 573d
    pop si
    inc di
    jmp 57d4    ; actually 5885, which is 'jmp 57d4'
