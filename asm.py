"""
	Per-file ASM edits for Appareden.
"""

# TODO: This needs cleanup, it is mostly old comments and old raw bytes that are meaningless now

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
# TODO: STill not sure: What else should be done after the dict ends?
    # lodsb again? maybe increment si?
    # Maybe I should jump to the initial lodsb that starts the text processing? It's at 57de, so jmp is ebc9
# 

# Found the way to do 16-bit add si, ax. It's 01c6, so that and the xor ah, ah can be dropped
    # Whoops, that's not right. Need to add sl, al (which can't be done, oops)

DICT_END_CHECK =     b'\x3C\xFF\x75\x04\x5E\xAC\xEB\xC4'
BTL_DICT_END_CHECK = b'\x3c\xff\x75\x04\x5e\xac\xeb\xcc'

"""
dictStartCheck:
    cmp al, fe
    jnz 5825       ; overlineCode
    push si
    lodsb
    mov si, 43aa    ; 4c18 for ORBTL
    xor ah, ah
    add si, ax
    lodsb
    nop
"""

DICT_START_CHECK =     b'\x3C\xFE\x75\x0B\x56\xAC\xBE\xAA\x43\x30\xE4\x01\xC6\xAC\x90'
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

OVERLINE_CODE =     b'\x3C\x7E\x75\x01\x4F'
BTL_OVERLINE_CODE = b'\x3c\x7e\x75\x01\x4f'
"""
overlineCode:
    cmp al, 7e
    jnz 581d       ; skipCompression
    dec di
"""

SKIP_SHADOFF =     b'\x3C\x5E\x75\x03\xAC\x74\x32'
BTL_SKIP_SHADOFF = b'\x90\x90\x90\x90\x90\x90\x90'
"""
skipCompression:
    cmp al, 5e
    jnz 5824       ; shadoffCompression
    lodsb
    jz 5867        ; halfwidthOriginal
"""

SHADOFF_COMPRESSION =     b'\x3C\x5A\x7F\x2E\x3C\x40\x7C\x2A\x47\x04\x20\xEB\x25'
BTL_SHADOFF_COMPRESSION = b'\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xeb\x14'
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
#                                                                                  v Begins to be overwritten
FULLWIDTH_ORIGINAL = b'\x8A\xE0\xAC\xE8\xAB\xFE\x8B\xD0\xE8\x0D\xFF\x56\xE8\x46\xFE\x90\x90\x90\xB4\x09\xA1\xD6\x03\xE8\xBB\xFE\xBE\xD8\x03\xE8\xCB\xFE\x5E\x47\x47\xEB\x24'
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

HALFWIDTH_ORIGINAL = b'\xB4\x09\x86\xE0\x8B\xD0\xE8\xEA\xFE\x56\xE8\x23\xFE\xE8\xA0\xFE\xBE\x14\x04\xE8\xC6\xFE\xA1\xD6\x03\xE8\x94\xFE\xBE\xD8\x03\xE8\xBA\xFE\x5E\x47\xE9\x4C'
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
                SKIP_SHADOFF, SHADOFF_COMPRESSION, FULLWIDTH_ORIGINAL,
                HALFWIDTH_ORIGINAL]

ORBTL_CODE = [BTL_DICT_END_CHECK, BTL_DICT_START_CHECK, BTL_OVERLINE_CODE,
              BTL_SKIP_SHADOFF, BTL_SHADOFF_COMPRESSION]

# ORBTL dictionary should go at offset 0x29d38, which is at seg 2443:5908?
    # Nope. Ingame it's at 4b568.
    # Oh right, it loads from DS. It's at seg 4695:4c18.