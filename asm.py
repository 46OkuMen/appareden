"""
	Per-file ASM edits for Appareden.
"""

SPACECODE_ASM = b'\x3c\x5f\x75\x07\xac\x88\xc1\x47\xe2\xfd\xac'
OVERLINE_ASM =  b'\x3c\x7e\x75\x01\x4f'
FULLWIDTH_ASM = b'\x3c\x82\x75\x08\x88\xc4\xac\xe8\xc9\xfe\xeb\x27'
SKIPCODE_ASM =  b'\x3c\x5e\x75\x05\xac\x0f\x84\x1e\x00'
ASCII_ASM =     b'\x3c\x5a\x0f\x8f\x18\x00\x3c\x40\x0f\x8c\x12\x00\x47\x04\x20\xe9\x0c\x00'
# 11 bytes, 5 bytes, 27 bytes
# sum: 43 bytes
# Needs to be less than (580a-584d) bytes long