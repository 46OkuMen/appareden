import os
import re

SRC_DISK = os.path.join('original', 'Appareden.HDI')
DEST_DISK = os.path.join('patched', 'Appareden.HDI')

FILES = ['ORTITLE.EXE', 'ORMAIN.EXE', 'ORFIELD.EXE', 'ORBTL.EXE', 'NEKORUN.EXE', 'SFIGHT.EXE', 'ENDING.EXE',]

SHADOFF_COMPRESSED_EXES = ['ORFIELD.EXE',]

SJIS_FIRST_BYTES = [0x81, 0x82, 0x83, 0x84, 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0xad, 0x8e, 0x8f, 0x90, 0x91, 0x92,
                    0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f, 0xe0, 0xe1,
                    0xe2, 0xe3, 0xe4, 0x35, 0xe6, 0xe7, 0xe8, 0xe9, 0xea]

FILE_BLOCKS = {
    'ENDING.EXE': [(0x64bb, 0x6512), ],  # memory error texts
    'NEKORUN.EXE': [(0xa840, 0xa8aa),   # error text + scene text
                (0xacc0, 0xacda),   # memory error text
                (0xaecc, 0xaf00), ],  # ems driver version text"
    'ORBTL.EXE': [(0x25130, 0x25150),   # null pointer error
              (0x251d2, 0x2524b),  # battle commands
              (0x252dd, 0x252fd),  # run/surprise
              (0x25330, 0x253d2),  # after battle
              (0x262e8, 0x26302),  # memory error text
              (0x2715a, 0x271aa),  # ems driver version texts
              (0x27282, 0x27345),  # hp/mp
              (0x27352, 0x2738e),  # skill sheets
              (0x2739b, 0x273fd),  # insufficient stuff text
              (0x28178, 0x28c9c),  # skill/spell names/descriptions
              (0x28ca3, 0x28cc9),  # item menu
              (0x29d38, 0x2b066),  # item descriptions
              (0x2d2ce, 0x2d931),  # people, places, things
              (0x2ea7a, 0x2eb0d)],  # stealing msgs"
    'ORFIELD.EXE': [(0x25f20, 0x25f40),  # null pointer error                  # TODO: Try to end blocks after section headers!! That'll keep their length where it needs to be.
                (0x25f72, 0x25fba),  # ems driver version texts
                (0x26120, 0x26195),  # names and memory error text
                (0x26368, 0x26444),  # memory and disk switches
                (0x26641, 0x26776),  # save and ui texts
                (0x267ef, 0x2694e),  # ui texts
                (0x26a0b, 0x26a8f),  # places
                (0x26b28, 0x26bbd),
                (0x26e16, 0x26e8a),
                (0x26e94, 0x26f1c),
                (0x2718d, 0x271ac),
                (0x271c1, 0x271e6),
                (0x271f8, 0x2723d),
                (0x27496, 0x27557),
                (0x275f0, 0x275fe),  # death msg
                (0x2760e, 0x27676),  # ship msg
                (0x28044, 0x280bf),  # Pause menu
                (0x281c9, 0x28214),
                (0x28265, 0x28279),  # Main menu, status select, setting names
                (0x282e0, 0x283c0),  # Status screen
                (0x283c0, 0x2847d),  # Settings
                (0x2847d, 0x28567),  # Equip screen header, "whose"
                (0x286b1, 0x28758),  # Equip screen
                (0x2894e, 0x28989),  # Equipment categories
                (0x2899c, 0x289c7),  # Unequip message, "who will use it"
                (0x28a15, 0x28a3d),
                (0x28c36, 0x28ccf),
                (0x28ce2, 0x28cf0),
                (0x28d3e, 0x28d67),
                (0x28f60, 0x29020), # Equipment and such
                (0x29020, 0x290bc),  # menu msgs
                (0x2a2ba, 0x2cc45),  # items and weapons
                (0x2d022, 0x2d3c4),  # result msgs
                (0x2da74, 0x2e690),  # skills/spells names/descriptions
                (0x2e9b2, 0x2ea84),
                (0x2eb4d, 0x2ebbd),
                (0x2ec86, 0x2ecf6),
                (0x2edbf, 0x2ef13),],  # result msgs"
    'ORMAIN.EXE': [(0x1580, 0x167b),   # null pointer msgs
                   (0x1706, 0x1735),   # ems driver msgs
                   (0x3ee4, 0x4547), ],   # names, menus, things"
    'ORTITLE.EXE': [(0x3ec0, 0x3ee0),   # null pointer msgs
                    (0x3f48, 0x407b),   # main menus
                    (0x407b, 0x4104),   # release dates?
                    (0x5000, 0x501a), ],   # memory error"
    'SFIGHT.EXE': [(0xd090, 0xd135),   # null pointer msgs
               (0xd4ea, 0xd586),   # names and things
               (0xd6c6, 0xd6fa)],    # ems driver msgs"
}

POINTER_CONSTANT = {
    'ORTITLE.EXE': 0x3eb0,
    'ORMAIN.EXE': 0x1570,
    'ORFIELD.EXE': 0x25f10,
    'ORBTL.EXE': 0x25120,
    'SFIGHT.EXE': 0xd080,
}

SPARE_BLOCK = {
  'ORMAIN.EXE': (0x1765, 0x1f6b),
  'ORBTL.EXE': (0x26303, 0x26b54),
  'ORFIELD.EXE': (0x2f570, 0x30570),
}

# Tables are (start, stop, stride) tuples.
POINTER_TABLES = {
    'ORMAIN.EXE': [],
    'ORTITLE.EXE': [],
    'ORBTL.EXE': [
        (0x25154, 0x25178, 2),
        (0x25f5c, 0x25f60, 2),
        (0x271fa, 0x27200, 2),
        (0x27202, 0x27208, 4),
        (0x27a50, 0x27dd2, 0xe),
        (0x27dd2, 0x27e50, 2),
        (0x27e50, 0x280f0, 0x10),
        (0x280f0, 0x28178, 2),
        (0x28cc2, 0x2905e, 12),
        (0x2905e, 0x290f8, 2),
        (0x29108, 0x29d38, 16),
        (0x2b4be, 0x2b4cf, 2),
        (0x2b65e, 0x2b7a0, 0x28),
        (0x2b7c6, 0x2d2a9, 0x28),

    ],
    'SFIGHT.EXE': [],
    'ORFIELD.EXE': [
        (0x260a8, 0x260bc, 2),
        (0x26362, 0x26368, 2),
        (0x265ee, 0x2663e, 2),
        (0x269e2, 0x269fa, 2),
        (0x26a90, 0x26a96, 2),
        (0x26aa0, 0x26acc, 2),
        (0x26ad8, 0x26afa, 2),
        (0x26b04, 0x26acc, 2),
        (0x26ad8, 0x26afa, 2),
        (0x26b04, 0x26b26, 2),
        (0x27f00, 0x27f90, 2),
        (0x27fa4, 0x28041, 2),
        (0x290be, 0x29450, 0xc), # BOT TOP 00 00 08 00 03 00 06 00 2d 00, repeat
        (0x2945a, 0x294f4, 2),
        (0x29504, 0x2a136, 0x10), # BOT TOP 05 00 01 00 00 00 00 00 ff 01 06 00 f4 01, repeat
        (0x2a136, 0x2a2ba, 2),
        (0x2d3c6, 0x2d746, 0xe), # BOT TOP 00 01 00 04 00 00 00 3c 00 c6 00, repeat
        (0x2d746, 0x2d7c6, 2),
        (0x2d7c6, 0x2da68, 0x10), # BOT TOP 1e 00 04 00 06 00 01 00 1a 00 00 00 01 00, repeat
        (0x2da66, 0x2da74, 2),

    ]
}

# Commenting out the ones that are above the pointer constant
POINTER_DISAMBIGUATION = {
    # ORFIELD
  0x3fe8: 0x1ffc,
  0x26858: 0x1313f,
  0x2896c: 0x1d93d,
  0x2ea5d: 0x23190,
  0x2ea44: 0x2314b,
  0x2ea2b: 0x230e6,
  0x2ea20: 0x23064,
  0x28f66: 0x1fc48,
  0x263be: 0xbe10,
  0x263cf: 0xbe2c,
  0x26e9d: 0x167d6,
  0x26ef9: 0x16e07,
  0x2718d: 0x16abf,
  0x271a2: 0x16bbc,
  0x271aa: 0x16bf2,
  0x271c1: 0x16e80,
  0x2900e: 0x204af,
  0x2e9e2: 0x22f68,
  0x26b64: 0x15e3e,
  0x290a1: 0x20d10,
  0x2eb50: 0x2324d,
  0x2e9b2: 0x22e57,
  0x2eab3: 0x2346b,
  0x28355: 0x1b14a,
  0x28c78: 0x1f191,
  0x28f90: 0x1fce4,
  0x2d111: 0x21720,
  0x2d24d: 0x21edc,
  0x2d298: 0x220d7,


  # ORBTL
  0x27359: 0x13bfd,
  0x25376: 0xd277,
  0x2538f: 0xd422,
  0x2539c: 0xd53d,
  0x253a7: 0xd658,
  0x25330: 0xcf33,
}

POINTERS_TO_REASSIGN = {
    'ORFIELD.EXE': [
            (0x2dc17, 0x2dbf4),   # Blaze2, Blaze3 descriptions
            (0x2dc3a, 0x2dbf4),
            (0x2dc80, 0x2dc5d),
            (0x2dca3, 0x2dc5d),
            (0x2dce9, 0x2dcc6),
            (0x2dd2f, 0x2dd0c),
            (0x2dd52, 0x2dd0c),
            (0x2dd98, 0x2dd75),
            (0x2ddbb, 0x2dd75),
            (0x2de01, 0x2ddde),
            (0x2de47, 0x2de24),
            (0x2de6a, 0x2de24),
            (0x2deb0, 0x2de8d),
            (0x2df19, 0x2def6),
            (0x2df3c, 0x2def6),
            (0x2df82, 0x2df5f),
            (0x2dfa5, 0x2df5f),
            (0x2dfeb, 0x2dfc8),
            (0x2e031, 0x2e00e),
            (0x2e054, 0x2e00e),
            (0x2e09a, 0x2e077),
            (0x2e0bd, 0x2e077),
            (0x2e103, 0x2e0e0),
            (0x2826a, 0x28315),
            (0x2826f, 0x2831b),
            (0x28272, 0x28320),
            (0x28277, 0x28326),
            (0x28c66, 0x28315),
            (0x28c6c, 0x2831b),
            (0x28c72, 0x28320),
            (0x28c78, 0x28326),
            (0x28fcf, 0x28315),
            (0x28fd5, 0x2831b),
            (0x28fdb, 0x28320),
            (0x28fe1, 0x28326),
            (0x2908b, 0x28315),
            (0x290a5, 0x28315),
            (0x290ab, 0x2831b),
            (0x290b1, 0x28320),
            (0x290b7, 0x28326),
            (0x2d056, 0x2e9b2),
            (0x2d06f, 0x2e9cb),
            (0x2d07a, 0x2e9d6),
            (0x2d097, 0x2e9b2),
            (0x2d0b0, 0x2e9cb),
            (0x2d0bb, 0x2e9d6),
            (0x2d0c7, 0x2d086),
            (0x2d0d8, 0x2e9b2),

            (0x2d100, 0x2d086),
            (0x2d111, 0x2e9b2),
            (0x2d12a, 0x2e9cb),
            (0x2d135, 0x2e9d6),
            (0x2d141, 0x2d086),
            (0x2d152, 0x2e9b2),
            (0x2d16b, 0x2e9cb),
            (0x2d176, 0x2e9d6),
            (0x2d182, 0x2d086),
            (0x2d193, 0x2e9b2),
            (0x2d1e9, 0x28315),
            (0x2d219, 0x28315),
            (0x2d247, 0x28315),
            (0x2d27b, 0x28315),
            (0x2d3b0, 0x2d396),

            (0x2e9fb, 0x2e9b2),
            (0x2ea14, 0x2e9cb),
            (0x2ea20, 0x2e9d6),
            (0x2ea2b, 0x2e9e2),
            (0x2ea44, 0x2e9b2),
            (0x2ea5d, 0x2d0f1),
            (0x2ea6c, 0x2e9e2),
            (0x2eb6e, 0x2e9cb),
            (0x2eb7c, 0x2e9d6),
            (0x2eba5, 0x2e9e2),
            (0x2ec89, 0x2eb50),
            (0x2eca7, 0x2e9cb),
            (0x2ecb5, 0x2e9d6),
            (0x2ecc3, 0x2eb8a),
            (0x2ecde, 0x2e9e2),
            (0x2edc2, 0x2eb50),
            (0x2edf8, 0x2eb8a),
            (0x2ee13, 0x2e9e2),
            (0x2ee5c, 0x2e9e2),
            (0x2ee7b, 0x2ee32),
            (0x2ee8a, 0x2e9e2),
            (0x2eea9, 0x2d264),
            (0x2eec0, 0x2e9e2),
            (0x2eed9, 0x2d396),

    ],
}

def effective_length(s):
    """The length of a string, ignoring the control codes."""

    # TODO: Not working properly yet.
    length = 0
    chars = s.split()
    while chars:
        if chars[0] != b'[':
            length += 1
            chars.pop(0)
        else:
            while chars[0] != b']':
                chars.pop(0)
            chars.pop(0)

    return length

def typeset(s):
    if len(s) <= 37:
        return s

    words = s.split(b' ')
    lines = []

    while words:
        line = b''
        while len(line) <= 37 and words:
            if len(line + words[0] + b' ') > 37:
                break
            line += words.pop(0) + b' '

        line = line.rstrip()
        lines.append(line)
    #for l in lines:
    #    print(l)

    return b'/'.join(lines)

def shadoff_compress(s):
    # Definitely don't compress filenames!
    if b'.GEM' in s:
        return s

    s = s.decode('shift-jis')
    compressed = ''

    chars = list(s)

    continuous_spaces = 0
    while chars:
        c = chars.pop(0)
        if c == ' ':
            continuous_spaces += 1
        elif c.isupper():
            if continuous_spaces > 2:
                compressed += '_' + chr(continuous_spaces)
            elif continuous_spaces > 0:
                compressed += ' '*(continuous_spaces)
            continuous_spaces = 0
            compressed += '^'
            compressed += c
        else:
            if continuous_spaces > 2:
                compressed += '_' + chr(continuous_spaces)
                c = c.upper()
            elif continuous_spaces > 0:
                compressed += ' '*(continuous_spaces-1)
                c = c.upper()
            continuous_spaces = 0
            compressed += c

    return bytes(compressed, encoding='shift-jis')

def replace_control_codes(s):
    s = s.decode('shift-jis')
    cursor = 0
    while cursor < len(s):
        c = s[cursor]
        if c == 'n':
            if s[cursor-1] != '>':
                s = s[:cursor] + '/' + s[cursor+1:]
        if c == 'w':
            s = s[:cursor] + '}' + s[cursor+1:]
        if c == 'c':
            if s[cursor-1] != '>':
                s = s[:cursor] + '$' + s[cursor+1:]
        cursor += 1
    s = s.encode('shift-jis')
    return s

CONTROL_CODES = {
  b'[LN]': b'/',
  b'[WAIT1]': b'}01',
  b'[WAIT2]': b'}02',
  b'[WAIT3]': b'}03',
  b'[WAIT4]': b'}04',
  b'[WAIT5]': b'}05',
  b'[WAIT6]': b'}06',
  b'[00]': bytes([0x00]),
  b'[BLANK]': b'',
}

POSTPROCESSING_CONTROL_CODES = {
    b'~': b' ',
    b'[BLANK]': b'',
}

"""
ORIGINAL_CONTROL_CODES = {
    b'[LN]': b'/',
    b'[WAIT1]': b'w01',
    b'[WAIT2]': b'w02',
    b'[WAIT3]': b'w03',
    b'[WAIT4]': b'w04',
    b'[WAIT5]': b'w05',
    b'[WAIT6]': b'w06',
}
"""

SPACECODE_ASM = b'\x3c\x5f\x75\x0c\xac\x88\xc1\x47\xe2\xfd\xac'
OVERLINE_ASM =  b'\x3c\x7e\x75\x01\x4f'
SHADOFF_ASM =   b'\x3c\x5e\x75\x05\xac\x0f\x84\x2a\x00\x3c\x5a\x0f\x8f\x24\x00\x3c\x40\x0f\x8c\x1e\x00\x47\x04\x20\xe9\x18\x00'
