"""
    Per-file ASM edits for Appareden.
"""

# Let's store the dictionary at 0x4b2ea, which is at seg 46f4:43aa.
# So, put 43aa in ESI
# mov si, 43aa = be aa 43

# Dict is going to be stuff like The[ff]as[ff]

FULLWIDTH_CHECK = b'\x81\x74\x34\x3C\x82\x74\x30'
"""
fullwidthCheck:
    cmp al, 82     ; just the 82 part of the instruction
    jz 5842        ; fullwidthOriginal
    cmp al, 81
    jz 5842
"""

"""
dictEndCheck
    cmp al, ff
    jnz 5816       ; dictStartCheck
    pop si
    lodsb
    jmp 57de      ; initial text handling code
"""

DICT_END_CHECK =     b'\x3C\xFF\x75\x04\x5E\xAC\xEB\xC4'
BTL_DICT_END_CHECK = b'\x3c\xff\x75\x04\x5e\xac\xeb\xcc'

"""
dictStartCheck:
    cmp al, f0
    jg 5825       ; overlineCode
    push si
    mov ah, al
    lodsb
    and ah, 0f
    mov si, 43aa    ; 4c18 for ORBTL
    add si, ax
    lodsb
"""

DICT_START_CHECK =     b'\x3C\xF0\x7f\x0d\x56\x88\xc4\xac\x80\xe4\x0f\xbe\xaa\x43\x01\xc6\xac'
BTL_DICT_START_CHECK = b'\x3c\xfe\x75\x0a\x56\xac\xbe\x18\x4c\x30\xe4\x01\xc6\xac'


#SPACE_COMPRESSION = b'\x3c\x5f\x75\x06\xac\x30\xe4\x01\xc7\xac'
"""
spaceCompression:
    cmp al, 5f
    jnz 5818      ; overlineCode
    lodsb
    xor ah, ah
    add di, ax
    lodsb

"""

OVERLINE_CODE =     b'\x3C\x7E\x75\x01\x4F\xeb\x33'
#OVERLINE_CODE =     b'\x90\x90\x90'
BTL_OVERLINE_CODE = b'\x3c\x7e\x75\x01\x4f'
"""
overlineCode:
    cmp al, 7e
    jnz 5830       ; jmp 5868
    dec di
    jmp 5868       ; halfwidthOriginal
"""

NOPS = b'\x90'*16



#SKIP_SHADOFF =     b'\x3C\x5E\x75\x03\xAC\x74\x30'
BTL_SKIP_SHADOFF = b'\x90\x90\x90\x90\x90\x90\x90'
"""
skipCompression:
    cmp al, 5e
    jnz 5824       ; shadoffCompression
    lodsb
    jz 5865        ; halfwidthOriginal
"""

#SHADOFF_COMPRESSION =     b'\x3C\x5A\x7F\x2c\x3C\x40\x7C\x28\x47\x04\x20\xEB\x23'
BTL_SHADOFF_COMPRESSION = b'\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xeb\x14'
"""
shadoffCompression:
    cmp al, 5a
    jg 5865        ; halfwidthOriginal
    cmp al, 40
    jl 5865        ; halfwidthOriginal
    inc di
    add al, 20
    jmp 5865       ; halfwidthOriginal
"""

# 8a e0 ac e8 af fe 8b d0 e8 11 ff 56 e8 4a fe e8 c7 fe be 14 04 e8 d7 fe a1 d6 03 e8 bb fe be d8 03 e8 cb fe 5e 47 47 eb 24
#                                                                                  v Begins to be overwritten
FULLWIDTH_ORIGINAL = b'\x8A\xE0\xAC\xE8\xAB\xFE\x8B\xD0\xE8\x0D\xFF\x56\xE8\x46\xFE\x90\xB4\x09\xA1\xD6\x03\xE8\xBd\xFE\xBE\xD8\x03\xE8\xCd\xFE\x5E\x47\x47\xEB\x26'
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
    mov si, 0414
    call 572d
    mov ax, [03d6]
    call 5717
    mov si, 03d8
    call 572d
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

#ORFIELD_CODE = [FULLWIDTH_CHECK, SPACE_COMPRESSION, OVERLINE_CODE, 
#                SKIP_COMPRESSION, SHADOFF_COMPRESSION, NOPS, FULLWIDTH_ORIGINAL, 
#                HALFWIDTH_ORIGINAL]

ORFIELD_CODE = [FULLWIDTH_CHECK, DICT_END_CHECK, DICT_START_CHECK, OVERLINE_CODE,
                NOPS, FULLWIDTH_ORIGINAL, HALFWIDTH_ORIGINAL]

ORBTL_CODE = [BTL_DICT_END_CHECK, BTL_DICT_START_CHECK, BTL_OVERLINE_CODE,
              BTL_SKIP_SHADOFF, BTL_SHADOFF_COMPRESSION]

# ORBTL dictionary should go at offset 0x29d38, which is at seg 2443:5908?
    # Nope. Ingame it's at 4b568.
    # Oh right, it loads from DS. It's at seg 4695:4c18.



"""
    ORFIELD FD: 0x8c0b. 81 72 3f 3c a0 72 08 3c e0 72 37 3c fe 73 33 8a e0 ac e8 d3 fe 3c 09 72 04 3c 0b 76 30 8b d0 e8 2d ff 56 e8 66 fe 33 c0 e8 e1 fe be 14 04 e8 f1 fe a1 d6 03 e8 d5 fe be d8 03 e8 e5 fe 5e 47 47 eb 8d b4 09 3c a0 72 03 05 80 00 86 e0 8b d0 e8 fd fe 56 be d8 03 b9 14 00 46 80 24 80 46 c6 04 00 46 e2 f5 e8 25 fe 33 c0 e8 a0 fe be 14 04 e8 c6 fe a1 d6 03 e8 d5 fe be d8 03 e8 e5 fe 5e 47 47 eb 8d b4 09 3c a0 72 03 05 80 00 86 e0 8b d0 e8 fd fe 56 be d8
    ORFIELD CD: 0x8e05. 81 72 3f 3c a0 72 08 3c e0 72 37 3c fe 73 33 8a e0 ac e8 d3 fe 3c 09 72 04 3c 0b 76 30 8b d0 e8 2d ff 56 e8 66 fe 33 c0 e8 e1 fe be 14 04 e8 f1 fe a1 d6 03 e8 d5 fe be d8 03 e8 e5 fe 5e 47 47 eb 8d b4 09 3c a0 72 03 05 80 00 86 e0 8b d0 e8 fd fe 56 be d8 03 b9 14 00 46 80 24 80 46 c6 04 00 46 e2 f5 e8 25 fe 33 c0 e8 a0 fe be 14 04 e8 c6 fe a1 d6 03 e8 94 fe be d8 03 e8 ba fe 5e 47 e9 4c ff 32 c0 e6 7c 1f 5f 5e 5d
  
  Yep. They are just different enough that it'll need some debugging.  
"""

CD_ORFIELD_CODE = b'\x3C\x81\x74\x2C\x3C\x82\x74\x28\x3C\xFF\x75\x04\x5E\xAC\xEB\xD1\x3C\xF0\x7F\x0D\x56\x88\xC4\xAC\x80\xE4\x0F\xBE\xAA\x43\x01\xC6\xAC\x3C\x7E\x75\x01\x4F\xEB\x33\x90\x90\x90\x90\x90\x90\x90\x90\x8A\xE0\xAC\xE8\xB3\xFE\x8B\xD0\xE8\x15\xFF\x56\xE8\x4E\xFE\x33\xC0\xE8\xC9\xFE\xBE\x14\x04\xE8\xD9\xFE\xA1\xD6\x03\xE8\xBD\xFE\xBE\xD8\x03\xE8\xCD\xFE\x5E\x47\x47\xEB\x26\xB4\x09\x86\xE0\x8B\xD0\xE8\xEC\xFE\x56\xE8\x25\xFE\x33\xC0\xE8\xA0\xFE\xBE\x14\x04\xE8\xC6\xFE\xA1\xD6\x03\xE8\x94\xFE\xBE\xD8\x03\xE8\xBA\xFE\x5E\x47\xE9\x4C'

"""
    cd_fullwidthOriginal = 5834
    cd_halfwidthOriginal = 585f
"""

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
    jmp 57d4     ; actually 5885, which is 'jmp 57d4' in halfwidth original
"""

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
    jmp 57d4
"""

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
       (0x3647, b''.join(ORBTL_CODE)),
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

        (0x8e04, CD_ORFIELD_CODE)
    ],


}