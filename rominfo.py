import os
import re

SRC_DISK = os.path.join('original', 'Appareden.HDI')
DEST_DISK = os.path.join('patched', 'Appareden.HDI')

FILES = ['ORTITLE.EXE', 'ORMAIN.EXE', 'ORFIELD.EXE', 'ORBTL.EXE', 'NEKORUN.EXE', 'SFIGHT.EXE', 'ENDING.EXE',]

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
                (0x26b28, 0x27557),  # shops and inns
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
                (0x2da79, 0x2e690),  # skills/spells names/descriptions
                (0x2e9b2, 0x2ef13)],  # result msgs"
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

POINTER_DISAMBIGUATION = {
  0x3fe8: 0x1ffc,
  0x26393: 0x26362,
  0x26858: 0x1313f,
  0x283f8: 0x27f44,
  0x2896c: 0x1d93d,
  0x28ce2: 0x28012,
  0x2ea5d: 0x23190,
  0x2ea44: 0x2314b,
  0x2ea2b: 0x230e6,
  0x2ea20: 0x23064,
  0x2e9cb: 0x2c90e,
  0x2d022: 0x20e8a,
  0x28f66: 0x1fc48,
  0x28436: 0x27f4c,
  0x26b41: 0x26a92,
  0x26b46: 0x26a94,
  0x26e16: 0x26ab4,
  0x26b79: 0x26aa0,
  0x26941: 0x2662e,
  0x26947: 0x26630,
  0x267ef: 0x2661e,
  0x263be: 0xbe10,
  0x263cf: 0xbe2c,
  0x267ef: 0x2661e,
  0x2692c: 0x2662c,
  0x26e9d: 0x167d6,
  0x26ef9: 0x16e07,
  0x2718d: 0x16abf,
  0x271a2: 0x16bbc,
  0x271aa: 0x16bf2,
  0x271c1: 0x16e80,
  0x271f9: 0x26b04,
  0x2900e: 0x204af,
  0x2e9e2: 0x22f68,
  0x2847d: 0x27f54,
  0x2853f: 0x27f70,
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



    """
    words = s.split()
    compressed = ''
    for w in words:
        if w[0].isupper():
            w = '^' + w
        else:
            w = w[0].upper() + w[1:]
        compressed += w
    """
    print(s)
    print(compressed)
    return bytes(compressed, encoding='shift-jis')

CONTROL_CODES = {
  b'[LN]': bytes([0x2f]),
  b'[WAIT1]': bytes([0x77, 0x01]),
  b'[WAIT2]': bytes([0x77, 0x02]),
  b'[WAIT3]': bytes([0x77, 0x03]),
  b'[WAIT4]': bytes([0x77, 0x04]),
  b'[WAIT5]': bytes([0x77, 0x05]),
  b'[WAIT6]': bytes([0x77, 0x06]),
}

SPACECODE_ASM = b'\x3c\x5f\x75\x0c\xac\x88\xc1\x47\xe2\xfd\xac'
OVERLINE_ASM =  b'\x3c\x7e\x75\x01\x4f'
SHADOFF_ASM =   b'\x3c\x5e\x75\x05\xac\x0f\x84\x2a\x00\x3c\x5a\x0f\x8f\x24\x00\x3c\x40\x0f\x8c\x1e\x00\x47\x04\x20\xe9\x18\x00'
