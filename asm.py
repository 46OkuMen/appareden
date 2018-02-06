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


# code I'm trying to move:
#3c 7e 75 01 4f 3c 5e 75 03 ac 74 43 3c 5a 7f 3f 3c 40 7c 3b 47 04 20 eb 36
# All the jumps should go to 5867 except hte first, which goes to the "cmp al, 5a" instruction


"""
checkIfDictOver:
    cmp al, dictEndCode ; 0xFF?
    jnz dictCompression
    pop esi
"""

"""
dictCompression:
    cmp al, dictCode
    jnz fullwidthCheck
    push esi ; where it's reading the text from
    lodsb
    mov esi, dictBase + al  ; begin reading from dictionary location + dictionary offset
    lodsb
"""

# lodsb loads the thing from DS:SI into AL

# Let's store the dictionary at 0x4b2ea, which is at seg 46f4:43aa.
# So, put 43aa in ESI
# mov si, 43aa = be aa 43

# Dict is going to be stuff like The[ff]as[ff]

# At 2443:580a:
# fullwidth      dictcompress                                                 overline
# 3c82 741b      3cff 7501 5e 3cfe 7b0b 56 ac beaa43 30e4 6601c6 ac           3c7e 7501 4f


FULLWIDTH_CHECK = b'\x82\x74\x30'
"""
fullwidthCheck:
    cmp al, 82     ; just the 82 part of the instruction
    jz 583e        ; fullwidthOriginal
"""

"""
dictEndCheck
    cmp al, ff
    jnz 5816       ; dictStartCheck
    pop si
    lodsb
    jmp 57de      ; initial text handling code
"""
# TODO: STill not sure: What else should be done after the dict ends?
    # lodsb again? maybe increment si?
    # Maybe I should jump to the initial lodsb that starts the text processing? It's at 57de, so jmp is ebc9
# 

# Found the way to do 16-bit add si, ax. It's 01c6, so that and the xor ah, ah can be dropped
    # Whoops, that's not right. Need to add sl, al (which can't be done, oops)

DICT_END_CHECK = b'\x3c\xff\x75\x04\x5e\xac\xeb\xc8'

"""
dictStartCheck:
    cmp al, fe
    jnz 5825       ; overlineCode
    push si
    lodsb
    mov si, 43aa
    xor ah, ah
    add si, ax
    lodsb
    nop
"""

DICT_START_CHECK = b'\x3c\xfe\x75\x0b\x56\xac\xbe\xaa\x43\x30\xe4\x01\xc6\xac\x90'



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

OVERLINE_CODE = b'\x3c\x7e\x75\x01\x4f'
"""
overlineCode:
    cmp al, 7e
    jnz 581d       ; skipCompression
    dec di
"""

SKIP_COMPRESSION = b'\x3c\x5e\x75\x03\xac\x74\x36'
"""
skipCompression:
    cmp al, 5e
    jnz 5824       ; shadoffCompression
    lodsb
    jz 5867        ; halfwidthOriginal
"""

SHADOFF_COMPRESSION = b'\x3c\x5a\x7f\x32\x3c\x40\x7c\x2e\x47\x04\x20\xeb\x29'
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

#NOPS = b'\x90'*13
"""
    just some nops.
"""

# 8a e0 ac e8 af fe 8b d0 e8 11 ff 56 e8 4a fe e8 c7 fe be 14 04 e8 d7 fe a1 d6 03 e8 bb fe be d8 03 e8 cb fe 5e 47 47 eb 24
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

#ORFIELD_CODE = [FULLWIDTH_CHECK, SPACE_COMPRESSION, OVERLINE_CODE, 
#                SKIP_COMPRESSION, SHADOFF_COMPRESSION, NOPS, FULLWIDTH_ORIGINAL, 
#                HALFWIDTH_ORIGINAL]

ORFIELD_CODE = [FULLWIDTH_CHECK, DICT_END_CHECK, DICT_START_CHECK, OVERLINE_CODE,
                SKIP_COMPRESSION, SHADOFF_COMPRESSION, FULLWIDTH_ORIGINAL,
                HALFWIDTH_ORIGINAL]
