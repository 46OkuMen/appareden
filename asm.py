"""
    Per-file ASM edits for Appareden.
"""

FULLWIDTH_CHECK = b'\x81\x74\x2b\x3C\x82\x74\x27'
"""
fullwidthCheck:
    cmp al, 82     ; just the 82 part of the instruction
    jz 5839        ; fullwidthOriginal
    cmp al, 81
    jz 5839
"""

"""
dictEndCheck
    cmp al, ee
    jnz 5816       ; dictStartCheck
    pop si
    lodsb
    jmp 57de      ; initial text handling code
"""

DICT_END_CHECK =     b'\x3C\xee\x75\x04\x5E\xAC\xEB\xC4'

"""
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
"""

DICT_START_CHECK =     b'\x3C\xef\x76\x0d\x56\x88\xc4\xac\x80\xe4\x0f\xbe\xaa\x43\x01\xc6\xac'

OVERLINE_CODE =     b'\x3C\x7E\x75\x01\x4F'
#BTL_OVERLINE_CODE = b'\x3c\x7e\x75\x01\x4f'
"""
overlineCode:
    cmp al, 7e
    jnz 5830       ; overlineEndCode
    dec di
"""

OVERLINE_END_CODE = b'\x3c\x7c\x75\x31\x47\x30\xc0\xeb\x2c'
"""
overlineEndCode:
    cmp al, 7c
    jnz 585f       ; halfwidthOriginal
    inc di
    xor al, al
    jmp 585f       ; halfwidthOriginal
    nop
"""

#NOPS = b'\x90'*9

FULLWIDTH_ORIGINAL = b'\x8a\xe0\xac\xe8\xb4\xfe\x8b\xd0\xe8\x16\xff\x56\xe8\x4f\xfe\xe8\xcc\xfe\xbe\x14\x04\xe8\xdc\xfe\x90\x90\x90\xa1\xd6\x03\xe8\xbd\xfe\xbe\xd8\x03\xe8\xcd\xfe\x5e\x47\x47\xeb\x26'
"""
fullwidthOriginal:
    mov ah, al
    lodsb
    call 56f3
    mov dx, ax
    call 575a
    push si
    call 5697
    call 5717
    mov si, 0414      <- Makes shadows look good
    call 572d         <- in charge of outlines/shadows
    mov ax, [03d6]
    call 5717
    mov si, 03d8
    call 572d        <- Makes text appear on top of shadows
    pop si
    inc di
    inc di
    jmp 588b       ; jumps to the 'jmp 57da' in halfwidthOriginal, since it can't reach 57da with a short jump
"""

HALFWIDTH_ORIGINAL = b'\xB4\x09\x86\xE0\x8B\xD0\xE8\xEc\xFE\x56\xE8\x25\xFE\x33\xc0\xE8\xA0\xFE\xBE\x14\x04\xE8\xC6\xFE\xA1\xD6\x03\xE8\x94\xFE\xBE\xD8\x03\xE8\xBA\xFE\x5E\x47\xE9\x4C'
"""
halfwidthOriginal:
    mov ah, 09
    xchg al, ah
    mov dx, ax
    call 575a
    push si
    call 5697
    xor ax, ax      <- necessary for fixing weird parens/overline coloring
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

ORFIELD_CODE = [FULLWIDTH_CHECK, DICT_END_CHECK, DICT_START_CHECK, OVERLINE_CODE, OVERLINE_END_CODE,
                FULLWIDTH_ORIGINAL, HALFWIDTH_ORIGINAL]


CD_FULLWIDTH_CHECK = b"\x3C\x81\x74\x2C\x3C\x82\x74\x28"
"""
cd_fullwidthCheck:
    cmp al, 81
    jz 5834      ; cd_fullwidthOriginal
    cmp al, 82
    jz 5834      ; cd_fullwidthOriginal
"""

CD_DICT_END_CHECK = b'\x3C\xEE\x75\x04\x5E\xAC\xEB\xc4'

"""
cd_dictEndCheck:
    cmp al, ee
    jnz 5814      ; dict_start_check
    pop si
    lodsb
    jmp 57d8      ; beginning of text handling loop, 'lodsb'
"""

CD_DICT_START_CHECK = b'\x3C\xEF\x76\x0D\x56\x88\xC4\xAC\x80\xE4\x0F\xBE\xD0\x43\x01\xC6\xAC'

"""
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
"""

CD_OVERLINE_CODE = b'\x3C\x7E\x75\x01\x4F'

"""
cd_overlineCode:
    cmp al, 7e
    jnz 582a
    dec di
"""

CD_OVERLINE_END_CODE = b'\x3c\x7c\x75\x31\x47\x30\xc0\xeb\x2c\x90'

"""
cd_overlineEndCode:
    cmp al, 7c
    jnz 585f       ; cd_halfwidthOriginal
    inc di
    xor al, al
    jmp 585f       ; cd_halfwidthOriginal
    nop
"""

CD_FULLWIDTH_ORIGINAL = b'\x8A\xE0\xAC\xE8\xB3\xFE\x8B\xD0\xE8\x15\xFF\x56\xE8\x4E\xFE\x33\xC0\xE8\xC9\xFE\xBE\x14\x04\xE8\xD9\xFE\xA1\xD6\x03\xE8\xBD\xFE\xBE\xD8\x03\xE8\xCD\xFE\x5E\x47\x47\xEB\x26'

"""
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
"""

CD_HALFWIDTH_ORIGINAL = b'\xB4\x09\x86\xE0\x8B\xD0\xE8\xEC\xFE\x56\xE8\x25\xFE\x33\xC0\xE8\xA0\xFE\xBE\x14\x04\xE8\xC6\xFE\xA1\xD6\x03\xE8\x94\xFE\xBE\xD8\x03\xE8\xBA\xFE\x5E\x47\xE9\x4c'

"""
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
"""

CD_ORFIELD_CODE = [CD_FULLWIDTH_CHECK, CD_DICT_END_CHECK, CD_DICT_START_CHECK, CD_OVERLINE_CODE,
                   CD_OVERLINE_END_CODE, CD_FULLWIDTH_ORIGINAL, CD_HALFWIDTH_ORIGINAL]

CD_ORBTL_CODE = b'\x3C\xEE\x75\x04\x5E\xAC\xEB\xCC\x3C\xEF\x76\x0d\x56\x88\xc4\xAC\x80\xE4\x0F\xBE\x66\x44\x01\xC6\xAC\x3C\x7E\x75\x01\x4F\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xEB\x14'

ORBTL_CODE = CD_ORBTL_CODE.replace(b'\xBE\x66\x44', b'\xBE\x18\x4c')


# Those control codes as bytes.
B_CONTROL_CODES = {
  b'w': b'}',
  b'c': b'$',
  b'n': b'/'
}

FD_EDITS = {
    # ORFIELD
    'ORFIELD.EXE': [
        (0x151b7, B_CONTROL_CODES[b'w']),         # w = "}"
        (0x15b0f, B_CONTROL_CODES[b'w']),         # w = "}"
        (0x15b99, B_CONTROL_CODES[b'w']),         # w = "}"

        (0x15519, B_CONTROL_CODES[b'n']),         # n = "/"
        (0x15528, B_CONTROL_CODES[b'n']),         # n = "/"
        (0x155df, B_CONTROL_CODES[b'n']),         # n = "/"
        (0x155ee, B_CONTROL_CODES[b'n']),         # n = "/"
        (0x15b1d, B_CONTROL_CODES[b'n']),         # n = "/"
        (0x15b5f, B_CONTROL_CODES[b'n']),         # n = "/"

        (0x15b16, B_CONTROL_CODES[b'c']),         # c = "$"
        (0x15b6c, B_CONTROL_CODES[b'c']),         # c = "$"
        (0x2551b, B_CONTROL_CODES[b'c']),         # c = "$"

        (0x1ab14, b'\xb2'),                       # Ailment buffer fix

        (0x8c0b, b''.join(ORFIELD_CODE))          # Text handling code
    ],

    'ORBTL.EXE': [
       #(0x3647, b''.join(ORBTL_CODE)),
       (0x3647, ORBTL_CODE)
    ]
}

CD_EDITS = {
    'ORFIELD.EXE': [
        (0x157c9, B_CONTROL_CODES[b'w']),
        (0x1612b, B_CONTROL_CODES[b'w']),
        (0x161b5, B_CONTROL_CODES[b'w']),

        (0x15b2b, B_CONTROL_CODES[b'n']),
        (0x15b3a, B_CONTROL_CODES[b'n']),
        (0x15bf1, B_CONTROL_CODES[b'n']),
        (0x15c00, B_CONTROL_CODES[b'n']),
        (0x16139, B_CONTROL_CODES[b'n']),
        (0x1617b, B_CONTROL_CODES[b'n']),

        (0x16132, B_CONTROL_CODES[b'c']),
        (0x16188, B_CONTROL_CODES[b'c']),
        (0x25b49, B_CONTROL_CODES[b'c']),

        (0x1b141, b'\xb2'),

        (0x8e04, b''.join(CD_ORFIELD_CODE))
    ],

    'ORBTL.EXE': [
        (0x3647, CD_ORBTL_CODE)
    ]


}