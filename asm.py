"""
	Per-file ASM edits for Appareden.
"""

#SPACECODE_ASM = b'\x3c\x5f\x75\x07\xac\x88\xc1\x47\xe2\xfd\xac'
#OVERLINE_ASM =  b'\x3c\x7e\x75\x01\x4f'
#FULLWIDTH_ASM = b'\x3c\x82\x75\x0a\x88\xc4\xac\x2d\x1e\x7f\x86\xe0\xeb\x30'
#SKIPCODE_ASM =  b'\x3c\x5e\x75\x05\xac\x0f\x84\x1c\x00'
#ASCII_ASM =     b'\x3c\x5a\x0f\x8f\x16\x00\x3c\x40\x0f\x8c\x10\x00\x47\x04\x20\xeb\x0b\x90'

#ORIGINAL_FULLWIDTH_ASM = b'\x8b\xd0\xe8\x2d\xff\x56\xe8\x66\xfe\x33\xc0\xe8\xe1\xfe\xbe\x14\x04\xe8\xf1\xfe\xa1\xd6\x03\xe8\xd5\xfe\xbe\xd8\x03\xe8\xe5\xfe\x5e\x47\x47\xeb\x8d'
# 11 bytes, 5 bytes, 27 bytes
# sum: 43 bytes
# Needs to be less than (580a-584d) bytes long

# inserted at 2443:580b, or 0x8bf0 in ORFIELD.EXE


FULLWIDTH_CHECK = b'\x82\x74\x30'
"""
fullwidthCheck:
    cmp al, 82     ; just the 82 part of the instruction
    jz 583e        ; fullwidthOriginal
"""

SPACE_COMPRESSION = b'\x3c\x5f\x75\x06\xac\x30\xe4\x01\xc7\xac'
"""
spaceCompression:
    cmp al, 5f
    jnz 5818      ; overlineCode
    lodsb
    xor ah, ah
    add di, ax
    lodsb

"""

OVERLINE_CODE = b'\x3c\x7e\x75\x01\x4f'
"""
overlineCode:
    cmp al, 7e
    jnz 581d       ; skipCompression
    dec di
"""

SKIP_COMPRESSION = b'\x3c\x5e\x75\x03\xac\x74\x43'
"""
skipCompression:
    cmp al, 5e
    jnz 5824       ; shadoffCompression
    lodsb
    jz 5867        ; halfwidthOriginal
"""

SHADOFF_COMPRESSION = b'\x3c\x5a\x7f\x3f\x3c\x40\x7c\x3b\x47\x04\x20\xeb\x36'
"""
shadoffCompression:
    cmp al, 5a
    jg 5867        ; halfwidthOriginal
    cmp al, 40
    jl 5867        ; halfwidthOriginal
    inc di
    add al, 20
    jmp 5867       ; halfwidthOriginal
"""

NOPS = b'\x90'*13
"""
    just some nops.
"""

FULLWIDTH_ORIGINAL = b'\x8a\xe0\xac\xe8\xaf\xfe\x8b\xd0\xe8\x11\xff\x56\xe8\x4a\xfe\xe8\xc7\xfe\xbe\x14\x04\xe8\xd7\xfe\xa1\xd6\x03\xe8\xbb\xfe\xbe\xd8\x03\xe8\xcb\xfe\x5e\x47\x47\xeb\x24'
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

HALFWIDTH_ORIGINAL = b'\xb4\x09\x86\xe0\x8b\xd0\xe8\xea\xfe\x56\xe8\x23\xfe\xe8\xa0\xfe\xbe\x14\x04\xe8\xc6\xfe\xa1\xd6\x03\xe8\x94\xfe\xbe\xd8\x03\xe8\xba\xfe\x5e\x47\xe9\x4c\xff'
"""
halfwidthOriginal:
    mov ah, 09
    xchg al, ah
    mov dx, ax
    call 575a
    push si
    call 5697
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

ORFIELD_CODE = [FULLWIDTH_CHECK, SPACE_COMPRESSION, OVERLINE_CODE, 
                SKIP_COMPRESSION, SHADOFF_COMPRESSION, NOPS, FULLWIDTH_ORIGINAL, 
                HALFWIDTH_ORIGINAL]
