"""
    Info on Appareden rom structure and project directory layout.
"""

import os
from collections import OrderedDict
from pointer_info import POINTER_DISAMBIGUATION, POINTERS_TO_REASSIGN
from appareden.asm import FD_EDITS, FD_CHEATS

SRC_DIR = 'original'
DEST_DIR = 'patched'

SRC_DISK = os.path.join(SRC_DIR, 'Appareden (UPDATED).HDI')
#SRC_CD_DISK = os.path.join('original_cd', 'Appareden (CD-UPDATED).hdi')
DEST_DISK = os.path.join(DEST_DIR, 'Appareden (UPDATED).HDI')
DEST_CD_DISK = os.path.join('patched_cd', 'Appareden (CD-UPDATED).hdi')

DUMP_XLS_PATH = 'appareden_sys_dump.xlsx'
POINTER_XLS_PATH = 'appareden_pointer_dump.xlsx'

# Rows to be displayed in the progress section of the README.
PROGRESS_ROWS = ['ORTITLE.EXE','ORFIELD.EXE', 'ORBTL.EXE', 'Dialogue', 'Images']

MSGS = ['ENDING.MSG', 'SCN02400.MSG', 'SCN02401.MSG', 'SCN02402.MSG', 'SCN02403.MSG',
        'SCN02404.MSG', 'SCN02500.MSG', 'SCN02501.MSG', 'SCN02502.MSG',
        'SCN02503.MSG', 'SCN02600.MSG', 'SCN02601.MSG', 'SCN02700.MSG', 'SCN02701.MSG',
        'SCN02702.MSG', 'SCN02800.MSG', 'SCN02900.MSG', 'SCN02901.MSG',
        'SCN02902.MSG', 'SCN02903.MSG', 'SCN02904.MSG', 'SCN03000.MSG',
        'SCN03001.MSG', 'SCN03002.MSG', 'SCN03003.MSG', 'SCN03004.MSG',
        'SCN03100.MSG', 'SCN03200.MSG', 'SCN03201.MSG', 'SCN03202.MSG',
        'SCN03203.MSG', 'SCN03204.MSG', 'SCN03205.MSG', 'SCN03206.MSG',
        'SCN03207.MSG', 'SCN03208.MSG', 'SCN03209.MSG', 'SCN03210.MSG',
        'SCN03300.MSG', 'SCN03400.MSG', 'SCN03401.MSG', 'SCN03402.MSG',
        'SCN03403.MSG', 'SCN03404.MSG', 'SCN03405.MSG', 'SCN03406.MSG',
        'SCN03500.MSG', 'SCN03600.MSG', 'SCN03700.MSG', 'SCN03701.MSG',
        'SCN03702.MSG', 'SCN03703.MSG', 'SCN03800.MSG', 'SCN03900.MSG',
        'SCN03901.MSG', 'SCN03902.MSG', 'SCN03903.MSG', 'SCN03904.MSG',
        'SCN03905.MSG', 'SCN03906.MSG', 'SCN03907.MSG', 'SCN04000.MSG',
        'SCN04001.MSG', 'SCN04100.MSG', 'SCN04200.MSG', 'SCN04201.MSG',
        'SCN04202.MSG', 'SCN04203.MSG', 'SCN04204.MSG', 'SCN04205.MSG',
        'SCN04206.MSG', 'SCN04300.MSG', 'SCN04400.MSG', 'SCN04401.MSG',
        'SCN04500.MSG', 'SCN04501.MSG', 'SCN04502.MSG', 'SCN04503.MSG',
        'SCN04504.MSG', 'SCN04505.MSG', 'SCN04506.MSG', 'SCN04600.MSG',
        'SCN04700.MSG', 'SCN04701.MSG', 'SCN04702.MSG', 'SCN04703.MSG',
        'SCN04704.MSG', 'SCN04705.MSG', 'SCN04900.MSG', 'SCN05000.MSG',
        'SCN05001.MSG', 'SCN05002.MSG', 'SCN05003.MSG', 'SCN05004.MSG',
        'SCN05005.MSG', 'SCN05006.MSG', 'SCN05007.MSG', 'SCN05011.MSG',
        'SCN05012.MSG', 'SCN05013.MSG', 'SCN05014.MSG', 'SCN05015.MSG',
        'SCN05016.MSG', 'SCN05021.MSG', 'SCN05022.MSG', 'SCN05023.MSG',
        'SCN05024.MSG', 'SCN05025.MSG', 'SCN05026.MSG', 'SCN05031.MSG',
        'SCN05100.MSG', 'SCN05101.MSG', 'SCN05102.MSG', 'SCN05103.MSG',
        'SCN05110.MSG', 'SCN05120.MSG', 'SCN05600.MSG', 'SCN05601.MSG',
        'SCN05602.MSG', 'SCN05603.MSG', 'SCN05900.MSG', 'SCN05901.MSG',
        'SCN05903.MSG', 'SCN05904.MSG', 'SCN06000.MSG', 'SCN06001.MSG',
        'SCN06003.MSG', 'SCN06004.MSG', 'SCN06005.MSG', 'SCN06100.MSG',
        'SCN06200.MSG', 'SCN06300.MSG', 'SCN09900.MSG', 'SCN10000.MSG',
        'SCN10200.MSG', 'SCN10300.MSG', 'SCN10301.MSG', 'SCN10400.MSG',
        'SCN10401.MSG', 'SCN10500.MSG', 'SCN10501.MSG', 'SCN10600.MSG',
        'SCN10601.MSG', 'SCN10700.MSG', 'SCN10701.MSG', 'SCN10702.MSG',
        'SCN10703.MSG', 'SCN10800.MSG', 'SCN10801.MSG', 'SCN10802.MSG',
        'SCN10803.MSG', 'SCN10900.MSG', 'SCN11000.MSG', 'SCN11001.MSG',
        'SCN11100.MSG', 'SCN11200.MSG', 'SCN11201.MSG', 'SCN11202.MSG',
        'SCN11203.MSG', 'SCN11204.MSG', 'SCN11205.MSG', 'SCN11300.MSG',
        'SCN11301.MSG', 'SCN11302.MSG', 'SCN11303.MSG', 'SCN11304.MSG',
        'SCN11400.MSG', 'SCN11401.MSG', 'SCN11402.MSG', 'SCN11403.MSG',
        'SCN11404.MSG', 'SCN11500.MSG', 'SCN11501.MSG', 'SCN11502.MSG',
        'SCN11503.MSG', 'SCN11600.MSG', 'SCN11601.MSG', 'SCN11602.MSG',
        'SCN11603.MSG', 'SCN11604.MSG', 'SCN11700.MSG', 'SCN11701.MSG',
        'SCN11800.MSG', 'SCN11801.MSG', 'SCN11900.MSG', 'SCN11903.MSG',
        'SCN12000.MSG', 'SCN12300.MSG', 'SCN12301.MSG', 'SCN12302.MSG',
        'SCN12303.MSG', 'SCN12304.MSG', 'SCN12305.MSG', 'SCN12306.MSG',
        'SCN12307.MSG', 'SCN12603.MSG', 'SCN12704.MSG', 'SCN12800.MSG',
        'SCN12803.MSG'
        ]



#MSGS = []

SHADOFF_COMPRESSED_EXES = []

# First bytes in SJIS Japanese strings.
SJIS_FIRST_BYTES = [0x81, 0x82, 0x83, 0x84, 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0xad, 0x8e, 0x8f, 0x90, 0x91, 0x92,
                    0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f, 0xe0, 0xe1,
                    0xe2, 0xe3, 0xe4, 0x35, 0xe6, 0xe7, 0xe8, 0xe9, 0xea]


class Rominfo:
    def __init__(self, file_blocks, pointer_constant, dictionary_location, pointer_tables,
                 compression_dictionary, pointer_disambiguation, pointers_to_reassign,
                 asm_edits, cheats):
        self.file_blocks = file_blocks
        self.pointer_constant = pointer_constant
        self.dictionary_location = dictionary_location
        self.pointer_tables = pointer_tables
        self.compression_dictionary = compression_dictionary
        self.pointer_disambiguation = pointer_disambiguation
        self.pointers_to_reassign = pointers_to_reassign
        self.asm_edits = asm_edits
        self.cheats = cheats

FILE_BLOCKS = {
    'ENDING.EXE': [(0x64bb, 0x6512), ],  # memory error texts
    'NEKORUN.EXE': [(0xa840, 0xa8aa),   # error text + scene text
                    (0xacc0, 0xacda),   # memory error text
                    (0xaecc, 0xaf00), ],  # ems driver version text"
    'ORBTL.EXE': [(0x251d2, 0x25265),  # battle commands
                  (0x252dd, 0x252fe),  # run/surprise
                  (0x25330, 0x253d3),  # after battle
                  (0x2715a, 0x271ac),  # ems driver version texts
                  (0x27282, 0x273fe),  # insufficient stuff text
                  (0x28178, 0x28c2a),  # skill/spell names/descriptions
                  (0x28c67, 0x28cc1),  # item menu
                  (0x29d38, 0x2b067),  # item descriptions
                  (0x2d2ce, 0x2d932),  # people, places, things
                  (0x2ea7a, 0x2eb0e)],  # stealing msgs"
    'ORFIELD.EXE': [(0x26120, 0x26195),  # names and memory error text
                    (0x26368, 0x26444),  # memory and disk switches
                    (0x2663e, 0x26777),  # save and ui texts
                    (0x267ef, 0x267ff),
                    (0x26855, 0x2694f),  # ui texts
                    (0x26a0b, 0x26a8f),  # places
                    (0x26b28, 0x26bbe),            # TODO: Item shop slots can go here
                    (0x26e16, 0x26f1d),            # TODO: Armor shop slots can go here
                    (0x2718d, 0x27557),
                    (0x275f0, 0x275fe),  # death msg
                    (0x2760e, 0x27627),  # ship msg
                    (0x27ef0, 0x27f00),  # Repel wore off msg
                    (0x28044, 0x28851),  # Equip screen
                    (0x2894e, 0x29021), # Equipment and such
                    (0x29021, 0x290be),  # menu msgs
                    (0x2a2ba, 0x2cc46),  # items and weapons
                    (0x2d022, 0x2d3c6),  # result msgs
                    (0x2da74, 0x2e692),  # skills/spells names/descriptions
                    (0x2e9b2, 0x2ea85),             # TODO: More slots can go here
                    (0x2eb4d, 0x2ef14),],  # result msgs" # TODO: Two undocumented sets of slots here!!
    'ORMAIN.EXE': [(0x1580, 0x167b),   # null pointer msgs
                   (0x1706, 0x1735),   # ems driver msgs
                   (0x3ee4, 0x4547), ],   # names, menus, things"
    'ORTITLE.EXE': [(0x3ec0, 0x3ee0),   # null pointer msgs
                    (0x3f48, 0x407b),   # main menus
                    (0x407b, 0x4105),   # release dates?
                    (0x5000, 0x501a), ],   # memory error"
    'SFIGHT.EXE': [(0xd090, 0xd135),   # null pointer msgs
                   (0xd4ea, 0xd586),   # names and things
                   (0xd6c6, 0xd6fa)],    # ems driver msgs"
}

# The constant added to a pointer's value to get its dereference.
POINTER_CONSTANT = {
    'ORTITLE.EXE': 0x3eb0,
    'ORFIELD.EXE': 0x25f10,
    'ORBTL.EXE': 0x25120,
}

# Location of the compression dictionary, where applicable.
DICTIONARY_LOCATION = {
    'ORFIELD.EXE': 0x2a2ba,
    'ORBTL.EXE':  0x29d38,
    'ORTITLE.EXE': None,
}

# Tables are (start, stop, stride) tuples.
POINTER_TABLES = {
    'ORTITLE.EXE': [
        (0x3ee4, 0x3f16, 2),
    ],
    'ORBTL.EXE': [
        (0x25154, 0x25178, 2),
        (0x25f5c, 0x25f60, 2),
        (0x271fa, 0x27200, 2),
        (0x27202, 0x27208, 4),
        (0x27a50, 0x27dd2, 0xe),
        (0x27dd2, 0x27e50, 2),
        (0x27e50, 0x280f0, 0x10),
        (0x2816a, 0x28178, 2),
        (0x28cc2, 0x2905e, 12),
        (0x2905e, 0x290f8, 2),
        (0x29108, 0x29d38, 16),
        (0x2b4be, 0x2b4cf, 2),
        (0x2b65e, 0x2b7a0, 0x28),
        (0x2b7c6, 0x2d2a9, 0x28),

    ],
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

# Control codes reassigned in ASM, as strings.
S_CONTROL_CODES = {
  'w': '}',
  'c': '$',
  'n': '/'
}

# Those control codes as bytes.
B_CONTROL_CODES = {
  b'w': b'}',
  b'c': b'$',
  b'n': b'/'
}

# Control codes as given in the dump.
CONTROL_CODES = {
  b'[LN]': b'/',
  b'[WAIT1]': B_CONTROL_CODES[b'w'] + b'01',
  b'[WAIT2]': B_CONTROL_CODES[b'w'] + b'02',
  b'[WAIT3]': B_CONTROL_CODES[b'w'] + b'03',
  b'[WAIT4]': B_CONTROL_CODES[b'w'] + b'04',
  b'[WAIT5]': B_CONTROL_CODES[b'w'] + b'05',
  b'[WAIT6]': B_CONTROL_CODES[b'w'] + b'06',
  b'[00]': bytes([0x00]),
  b'[BLANK]': b'',
  b'[ee]': bytes([0xee]),
  b'[sysLN]': b'\r\n',
}

# Convert these after all text processing.
POSTPROCESSING_CONTROL_CODES = {

    'ORFIELD.EXE': OrderedDict([
        (b'~', b' '),
        (b'[BLANK]', b''),
        (b'[O]', b'O\x7e'),
        (b'[o]', b'o\x7e'),
        (b'[U]', b'U\x7e'),
        (b'[u]', b'u\x7e'),
        (b'[|]', b'\x7c'),
    ]),

    'ORBTL.EXE': OrderedDict([
        (b'~', b' '),
        (b'[BLANK]', b''),
        (b'[O]', b'O\x7e'),
        (b'[o]', b'o\x7e'),
        (b'[U]', b'U\x7e'),
        (b'[u]', b'u\x7e'),
        #(b'[|]', b'\x7c'),
    ]),

    'ORTITLE.EXE': [],
}

DICTIONARY_LOCATION = {
    'ORFIELD.EXE': 0x2a2ba,
    'ORBTL.EXE': 0x29d38,
    'ORTITLE.EXE': None
}

COMPRESSION_DICTIONARY = {

'ORFIELD.EXE': OrderedDict([
    #(b'~', b' '),
    #(b'[BLANK]', b''),
    #(b'[O]', b'O\x7e'),
    #(b'[o]', b'o\x7e'),
    #(b'[U]', b'U\x7e'),
    #(b'[u]', b'u\x7e'),

    (b'the', b'\xf0\x0e'),
    (b'with', b'\xf0\x12'),
    (b'that', b'\xf0\x17'),
    (b'The', b'\xf0\x1c'),
    (b'from', b'\xf0 '),
    (b'Zen', b'\xf0%'),
    (b'for', b'\xf0)'),
    (b'sword', b'\xf0-'),
    (b'blade', b'\xf03'),
    (b'True', b'\xf09'),
    (b'made', b'\xf0>'),
    (b'katana', b'\xf0C'),
    (b'Ultimate', b'\xf0J'),
    (b'God', b'\xf0S'),
    (b'enemies', b'\xf0W'),
    (b'against', b'\xf0_'),
    (b'bell', b'\xf0g'),
    (b'Good', b'\xf0l'),
    (b'power', b'\xf0q'),
    (b'holy', b'\xf0w'),
    (b'defense', b'\xf0|'),
    (b'Journal', b'\xf0\x84'),
    (b'battle', b'\xf0\x8c'),
    (b'happi', b'\xf0\x93'),
    (b'enemy', b'\xf0\x99'),
    (b'use', b'\xf0\x9f'),
    (b'Receive', b'\xf0\xa3'),
    (b'powers', b'\xf0\xab'),
    (b'magic', b'\xf0\xb2'),
    (b'light', b'\xf0\xb8'),
    (b'Claws', b'\xf0\xbe'),
    (b'into', b'\xf0\xc4'),
    (b'and', b'\xf0\xc9'),
    (b'protects', b'\xf0\xcd'),
    (b'blessing', b'\xf0\xd6'),
    (b'spirit', b'\xf0\xdf'),
    (b'Unable', b'\xf0\xe6'),
    (b'Dragon', b'\xf0\xed'),
    (b'peace', b'\xf0\xf4'),
    (b'fully', b'\xf0\xfa'),
    (b'tabi', b'\xf1\x00'),
    (b'Sell', b'\xf1\x05'),
    (b'lightning', b'\xf1\n'),
    (b'legendary', b'\xf1\x14'),
    (b'blessings', b'\xf1\x1e'),
    (b'Equipment', b'\xf1('),
    (b'Elemental', b'\xf12'),
    (b'strength', b'\xf1<'),
    (b'favorite', b'\xf1E'),
    (b'symbol', b'\xf1N'),
    (b'letter', b'\xf1U'),
    (b'Status', b'\xf1\\'),
    (b'staff', b'\xf1c'),
    (b'socks', b'\xf1i'),
    (b'will', b'\xf1o'),
    (b'pipe', b'\xf1t'),
    (b'gods', b'\xf1y'),
    (b'evil', b'\xf1~'),
    (b'axe', b'\xf1\x83'),
    (b'Gem', b'\xf1\x87'),
    (b'points~~~~~~~~~~', b'\xf1\x8b'),
    (b'Tanegashima', b'\xf1\x9c'),
    (b'increased~', b'\xf1\xa8'),
    (b'containing', b'\xf1\xb3'),
    (b'increases', b'\xf1\xbe'),
    (b'darkness', b'\xf1\xc8'),
    (b'Strength', b'\xf1\xd1'),
    (b'Defender', b'\xf1\xda'),
    (b'through', b'\xf1\xe3'),
    (b'strikes', b'\xf1\xeb'),
    (b'pattern', b'\xf1\xf3'),
    (b'enhance', b'\xf1\xfb'),
    (b"enemy's", b'\xf2\x03'),
    (b'Leather', b'\xf2\x0b'),
    (b'Spirit', b'\xf2\x13'),
    (b'times', b'\xf2\x1a'),
    (b'robes', b'\xf2 '),
    (b'lower', b'\xf2&'),
    (b'soul', b'\xf2,'),
    (b'ring', b'\xf21'),
    (b'gold', b'\xf26'),
    (b'coat', b'\xf2;'),
    (b'body', b'\xf2@'),
    (b'War,', b'\xf2E'),
    (b'Type', b'\xf2J'),
    (b'Pill', b'\xf2O'),
    (b'Name', b'\xf2T'),
    (b'Holy', b'\xf2Y'),
    (b'Gold', b'\xf2^'),
    (b'Bolt', b'\xf2c'),
    (b'Arms', b'\xf2h'),
    (b'any', b'\xf2m'),
    (b'Supernatural', b'\xf2q'),
    (b'recovered', b'\xf2~'),
    (b'protected', b'\xf2\x88'),
    (b'shuriken', b'\xf2\x92'),
    (b'restores', b'\xf2\x9b'),
    (b'Festival', b'\xf2\xa4'),
    (b'special', b'\xf2\xad'),
    (b'magical', b'\xf2\xb5'),
    (b'ancient', b'\xf2\xbd'),
    (b'Inferno', b'\xf2\xc5'),
    (b'Eternal', b'\xf2\xcd'),
    (b'Defense', b'\xf2\xd5'),
    (b'Crystal', b'\xf2\xdd'),
    (b'Boulder', b'\xf2\xe5'),
    (b'Blessed', b'\xf2\xed'),
    (b'silver', b'\xf2\xf5'),
    (b'sacred', b'\xf2\xfc'),
    (b'escape', b'\xf3\x03'),
    (b'enough', b'\xf3\n'),
    (b'energy', b'\xf3\x11'),
    (b'dragon', b'\xf3\x18'),
    (b'breath', b'\xf3\x1f'),
    (b'breaks', b'\xf3&'),
    (b'Poison', b'\xf3-'),
    (b'Meteor', b'\xf34'),
    (b'Icicle', b'\xf3;'),
    (b'Icebud', b'\xf3B'),
    (b'winds', b'\xf3I'),
    (b'steel', b'\xf3O'),
    (b'heavy', b'\xf3U'),
    (b'demon', b'\xf3['),
    (b'crest', b'\xf3a'),
    (b'above', b'\xf3g'),
    (b'Storm', b'\xf3m'),
    (b'Karma', b'\xf3s'),
    (b'Items', b'\xf3y'),
    (b'Charm', b'\xf3\x7f'),
    (b'Blaze', b'\xf3\x85'),
    (b'moon', b'\xf3\x8b'),
    (b'like', b'\xf3\x90'),
    (b'life', b'\xf3\x95'),
    (b'have', b'\xf3\x9a'),
    (b'fire', b'\xf3\x9f'),
    (b'book', b'\xf3\xa4'),
    (b'This', b'\xf3\xa9'),
    (b'Item', b'\xf3\xae'),
    (b'Head', b'\xf3\xb3'),
    (b'Hand', b'\xf3\xb8'),
    (b'Call', b'\xf3\xbd'),
    (b'Boot', b'\xf3\xc2'),
    (b'Body', b'\xf3\xc7'),
    (b'you', b'\xf3\xcc'),
    (b'was', b'\xf3\xd0'),
    (b'gun', b'\xf3\xd4'),
    (b'gem', b'\xf3\xd8'),
    (b'art', b'\xf3\xdc'),
    (b'all', b'\xf3\xe0'),
    (b'Yes', b'\xf3\xe4'),
    (b'Use', b'\xf3\xe8'),
    (b'Not', b'\xf3\xec'),
    (b'~~Choose~~~~~~~~~~~~~~', b'\xf3\xf0'),
    (b'Choose~~~~~~~~~~~~~~~', b'\xf4\x07'),
    (b'miniaturized', b'\xf4\x1d'),
    (b'manji-shaped', b'\xf4*'),
    (b'purchased~~', b'\xf47'),
    (b'beautifully', b'\xf4C'),
    (b'Anti-Spirit', b'\xf4O'),
    (b'reinforced', b'\xf4['),
    (b'protection', b'\xf4f'),
    (b'mysterious', b'\xf4q'),
    (b'here~~~~~~', b'\xf4|'),
    (b'concealing', b'\xf4\x87'),
    (b'Neutralize', b'\xf4\x92'),
    (b'Apocalypse', b'\xf4\x9d'),
    (b'~~OK?~~~~', b'\xf4\xa8'),
    (b'salvation', b'\xf4\xb2'),
    (b'encounter', b'\xf4\xbc'),
    (b'beautiful', b'\xf4\xc6'),
    (b'admirable', b'\xf4\xd0'),
    (b'Transform', b'\xf4\xda'),
    (b'Protected', b'\xf4\xe4'),
    (b'Lightning', b'\xf4\xee'),
    (b'Furyquake', b'\xf4\xf8'),
    (b'Amaterasu', b'\xf5\x02'),
    (b'warriors', b'\xf5\x0c'),
    (b'requires', b'\xf5\x15'),
    (b'imported', b'\xf5\x1e'),
    (b'headband', b"\xf5'"),
    (b"dragon's", b'\xf50'),
    (b'defenses', b'\xf59'),
    (b'attached', b'\xf5B'),
    (b'Manjusri', b'\xf5K'),
    (b'Hellfire', b'\xf5T'),
    (b'Heavenly', b'\xf5]'),
    (b"Goemon's", b'\xf5f'),
    (b'Contains', b'\xf5o'),
    (b'without', b'\xf5x'),
    (b'threads', b'\xf5\x80'),
    (b'silence', b'\xf5\x88'),
    (b'samurai', b'\xf5\x90'),
    (b'returns', b'\xf5\x98'),
    (b'quality', b'\xf5\xa0'),
    (b'polearm', b'\xf5\xa8'),
    (b'do?~~~~', b'\xf5\xb0'),
    (b'created', b'\xf5\xb8'),
    (b'clothes', b'\xf5\xc0'),
    (b'attacks', b'\xf5\xc8'),
    (b'agility', b'\xf5\xd0'),
    (b'Strikes', b'\xf5\xd8'),
    (b'Barrier', b'\xf5\xe0'),
    (b'~~What', b'\xf5\xe8'),
    (b'wisdom', b'\xf5\xef'),
    (b"wasn't", b'\xf5\xf6'),
    (b'strike', b'\xf5\xfd'),
    (b'random', b'\xf6\x04'),
    (b'raises', b'\xf6\x0b'),
    (b'proper', b'\xf6\x12'),
    (b'poison', b'\xf6\x19'),
    (b'plates', b'\xf6 '),
    (b'mobile', b"\xf6'"),
    (b'mirror', b'\xf6.'),
    (b'master', b'\xf65'),
    (b'lowers', b'\xf6<'),
    (b'imbued', b'\xf6C'),
    (b'flames', b'\xf6J'),
    (b'famous', b'\xf6Q'),
    (b'cursed', b'\xf6X'),
    (b'collar', b'\xf6_'),
    (b'Talons', b'\xf6f'),
    (b'Sacred', b'\xf6m'),
    (b'Flurry', b'\xf6t'),
    (b'Elixir', b'\xf6{'),
    (b'Divine', b'\xf6\x82'),
    (b'Create', b'\xf6\x89'),
    (b'Attack', b'\xf6\x90'),
    (b'Appare', b'\xf6\x97'),
    (b'~~Who', b'\xf6\x9e'),
    (b'white', b'\xf6\xa4'),
    (b'which', b'\xf6\xaa'),
    (b'their', b'\xf6\xb0'),
    (b'super', b'\xf6\xb6'),
    (b'stone', b'\xf6\xbc'),
    (b'souls', b'\xf6\xc2'),
    (b'skies', b'\xf6\xc8'),
    (b'short', b'\xf6\xce'),
    (b'sharp', b'\xf6\xd4'),
    (b'quite', b'\xf6\xda'),
    (b'parts', b'\xf6\xe0'),
    (b'ninja', b'\xf6\xe6'),
    (b'named', b'\xf6\xec'),
    (b'known', b'\xf6\xf2'),
    (b'force', b'\xf6\xf8'),
    (b'flesh', b'\xf6\xfe'),
    (b'flame', b'\xf7\x04'),
    (b"don't", b'\xf7\n'),
    (b'cured', b'\xf7\x10'),
    (b'black', b'\xf7\x16'),
    (b'armor', b'\xf7\x1c'),
    (b'Vajra', b'\xf7"'),
    (b'Stuff', b'\xf7('),
    (b'Spear', b'\xf7.'),
    (b'Price', b'\xf74'),
    (b'Metal', b'\xf7:'),
    (b'Light', b'\xf7@'),
    (b'Level', b'\xf7F'),
    (b'Gimme', b'\xf7L'),
    (b'Apple', b'\xf7R'),
    (b'15-40', b'\xf7X'),
    (b'10-20', b'\xf7^'),
    (b'your', b'\xf7d'),
    (b'rate', b'\xf7i'),
    (b'many', b'\xf7n'),
    (b'item', b'\xf7s'),
    (b'heal', b'\xf7x'),
    (b'full', b'\xf7}'),
    (b'down', b'\xf7\x82'),
    (b'dark', b'\xf7\x87'),
    (b'cold', b'\xf7\x8c'),
    (b'bone', b'\xf7\x91'),
    (b'away', b'\xf7\x96'),
    (b'Word', b'\xf7\x9b'),
    (b'West', b'\xf7\xa0'),
    (b'Tabi', b'\xf7\xa5'),
    (b'Sake', b'\xf7\xaa'),
    (b'Hail', b'\xf7\xaf'),
    (b'Form', b'\xf7\xb4'),
    (b'Dead', b'\xf7\xb9'),
    (b'Club', b'\xf7\xbe'),
    (b'too', b'\xf7\xc3'),
    (b'sea', b'\xf7\xc7'),
    (b'one', b'\xf7\xcb'),
    (b'max', b'\xf7\xcf'),
    (b'has', b'\xf7\xd3'),
    (b'god', b'\xf7\xd7'),
    (b'fog', b'\xf7\xdb'),
    (b'can', b'\xf7\xdf'),
    (b'are', b'\xf7\xe3'),
    (b'You', b'\xf7\xe7'),
    (b'Son', b'\xf7\xeb'),
    (b'Has', b'\xf7\xef'),
    (b'Fog', b'\xf7\xf3'),
    (b'Buy', b'\xf7\xf7'),
]),

'ORBTL.EXE': OrderedDict([
    #(b'~', b' '),
    #(b'[BLANK]', b''),
    #(b'[O]', b'O\x7e'),
    #(b'[o]', b'o\x7e'),
    #(b'[U]', b'U\x7e'),
    #(b'[u]', b'u\x7e'),

    (b'the', b'\xf0\x0e'),
    (b'with', b'\xf0\x12'),
    (b'True', b'\xf0\x17'),
    (b'Ultimate', b'\xf0\x1c'),
    (b'Dragon', b'\xf0%'),
    (b'from', b'\xf0,'),
    (b'Pill', b'\xf01'),
    (b'Happi', b'\xf06'),
    (b'enemies', b'\xf0<'),
    (b'Zen', b'\xf0D'),
    (b'Tachi', b'\xf0H'),
    (b'Bell', b'\xf0N'),
    (b'Appare', b'\xf0S'),
    (b'enemy', b'\xf0Z'),
    (b'Staff', b'\xf0`'),
    (b'Claws', b'\xf0f'),
    (b'Tabi', b'\xf0l'),
    (b'ZP:', b'\xf0q'),
    (b'HP:', b'\xf0u'),
    (b'defense', b'\xf0y'),
    (b'Spirit', b'\xf0\x81'),
    (b'that', b'\xf0\x88'),
    (b'Pipe', b'\xf0\x8d'),
    (b'and', b'\xf0\x92'),
    (b'Tanegashima', b'\xf0\x96'),
    (b'lightning', b'\xf0\xa2'),
    (b'spirit', b'\xf0\xac'),
    (b'Scroll', b'\xf0\xb3'),
    (b'Rosary', b'\xf0\xba'),
    (b'Collar', b'\xf0\xc1'),
    (b'Robes', b'\xf0\xc8'),
    (b'Grail', b'\xf0\xce'),
    (b'Wall', b'\xf0\xd4'),
    (b'Ring', b'\xf0\xd9'),
    (b'Gold', b'\xf0\xde'),
    (b'Frog', b'\xf0\xe3'),
    (b'Fang', b'\xf0\xe8'),
    (b'increases', b'\xf0\xed'),
    (b"enemy's", b'\xf0\xf7'),
    (b'element', b'\xf0\xff'),
    (b'against', b'\xf1\x07'),
    (b'Blesses', b'\xf1\x0f'),
    (b'weapon', b'\xf1\x17'),
    (b'Votive', b'\xf1\x1e'),
    (b'Light', b'\xf1%'),
    (b'holy', b'\xf1+'),
    (b'Bolt', b'\xf10'),
    (b'all', b'\xf15'),
    (b'The', b'\xf19'),
    (b'Transform', b'\xf1='),
    (b'Ochimusha', b'\xf1G'),
    (b'Amaterasu', b'\xf1Q'),
    (b'attacks', b'\xf1['),
    (b'Inferno', b'\xf1c'),
    (b'Eternal', b'\xf1k'),
    (b'Breaker', b'\xf1s'),
    (b'Boulder', b'\xf1{'),
    (b'elixir', b'\xf1\x83'),
    (b'breath', b'\xf1\x8a'),
    (b'Silver', b'\xf1\x91'),
    (b'Poison', b'\xf1\x98'),
    (b'Meteor', b'\xf1\x9f'),
    (b'Kimono', b'\xf1\xa6'),
    (b'Katana', b'\xf1\xad'),
    (b'Icicle', b'\xf1\xb4'),
    (b'Icebud', b'\xf1\xbb'),
    (b'Golden', b'\xf1\xc2'),
    (b'Falcon', b'\xf1\xc9'),
    (b'Elixir', b'\xf1\xd0'),
    (b'Bracer', b'\xf1\xd7'),
    (b'Benkei', b'\xf1\xde'),
    (b'winds', b'\xf1\xe5'),
    (b'magic', b'\xf1\xeb'),
    (b'lower', b'\xf1\xf1'),
    (b'above', b'\xf1\xf7'),
    (b'White', b'\xf1\xfd'),
    (b'Vajra', b'\xf2\x03'),
    (b'Tiger', b'\xf2\t'),
    (b'Tengu', b'\xf2\x0f'),
    (b'Storm', b'\xf2\x15'),
    (b'Stone', b'\xf2\x1b'),
    (b'Mochi', b'\xf2!'),
    (b'Blaze', b"\xf2'"),
    (b'will', b'\xf2-'),
    (b'life', b'\xf22'),
    (b'into', b'\xf27'),
    (b'fire', b'\xf2<'),
    (b'Soul', b'\xf2A'),
    (b'Sake', b'\xf2F'),
    (b'Koma', b'\xf2K'),
    (b'Holy', b'\xf2P'),
    (b'Gale', b'\xf2U'),
    (b'Call', b'\xf2Z'),
    (b'Old', b'\xf2_'),
    (b'Cat', b'\xf2c'),
    (b'Anti-Spirit', b'\xf2g'),
    (b'Neutralize', b'\xf2s'),
    (b'Mysterious', b'\xf2~'),
    (b'Hallelujah', b'\xf2\x89'),
    (b'instantly', b'\xf2\x94'),
    (b'Tsukuyomi', b'\xf2\x9e'),
    (b'Moonlight', b'\xf2\xa8'),
    (b'Longevity', b'\xf2\xb2'),
    (b'Furyquake', b'\xf2\xbc'),
    (b'defenses', b'\xf2\xc6'),
    (b'darkness', b'\xf2\xcf'),
    (b'Training', b'\xf2\xd8'),
    (b'Strength', b'\xf2\xe1'),
    (b'Masamune', b'\xf2\xea'),
    (b'Judgment', b'\xf2\xf3'),
    (b'Hellfire', b'\xf2\xfc'),
    (b'Headband', b'\xf3\x05'),
    (b'Samurai', b'\xf3\x0e'),
    (b'Leather', b'\xf3\x16'),
    (b'Induces', b'\xf3\x1e'),
    (b'Icicles', b'\xf3&'),
    (b'Defense', b'\xf3.'),
    (b'Chinese', b'\xf36'),
    (b'random', b'\xf3>'),
    (b'powers', b'\xf3E'),
    (b'mirror', b'\xf3L'),
    (b'escape', b'\xf3S'),
    (b'enough', b'\xf3Z'),
    (b'energy', b'\xf3a'),
    (b'battle', b'\xf3h'),
    (b'Suzaku', b'\xf3o'),
    (b'Sacred', b'\xf3v'),
    (b'Priest', b'\xf3}'),
    (b'Leaves', b'\xf3\x84'),
    (b'Helper', b'\xf3\x8b'),
    (b'Flurry', b'\xf3\x92'),
    (b'Flames', b'\xf3\x99'),
    (b'Escape', b'\xf3\xa0'),
    (b'Divine', b'\xf3\xa7'),
    (b'Copper', b'\xf3\xae'),
    (b'Byakko', b'\xf3\xb5'),
    (b'skies', b'\xf3\xbc'),
    (b'party', b'\xf3\xc2'),
    (b'light', b'\xf3\xc8'),
    (b'force', b'\xf3\xce'),
    (b'Water', b'\xf3\xd4'),
    (b'Stole', b'\xf3\xda'),
    (b'Steal', b'\xf3\xe0'),
    (b'Santa', b'\xf3\xe6'),
    (b'Manji', b'\xf3\xec'),
    (b'Majin', b'\xf3\xf2'),
    (b'Lucia', b'\xf3\xf8'),
    (b'Haori', b'\xf3\xfe'),
    (b'Grass', b'\xf4\x04'),
    (b'Gimme', b'\xf4\n'),
    (b'Genbu', b'\xf4\x10'),
    (b'Flute', b'\xf4\x16'),
    (b'Flame', b'\xf4\x1c'),
    (b'Dress', b'\xf4"'),
    (b'Death', b'\xf4('),
    (b'Bible', b'\xf4.'),
    (b'wind', b'\xf44'),
    (b'sake', b'\xf49'),
    (b'made', b'\xf4>'),
    (b'down', b'\xf4C'),
    (b'dark', b'\xf4H'),
    (b'away', b'\xf4M'),
    (b'Word', b'\xf4R'),
    (b'Type', b'\xf4W'),
    (b'Tree', b'\xf4\\'),
    (b'Pray', b'\xf4a'),
    (b'Name', b'\xf4f'),
    (b'Moon', b'\xf4k'),
    (b'Mask', b'\xf4p'),
    (b'Lion', b'\xf4u'),
    (b'Item', b'\xf4z'),
    (b'Hail', b'\xf4\x7f'),
    (b'Form', b'\xf4\x84'),
    (b'Fire', b'\xf4\x89'),
    (b'Dark', b'\xf4\x8e'),
    (b'Crow', b'\xf4\x93'),
    (b'you', b'\xf4\x98'),
    (b'sea', b'\xf4\x9c'),
    (b'fog', b'\xf4\xa0'),
    (b'air', b'\xf4\xa4'),
    (b'aid', b'\xf4\xa8'),
    (b'Six', b'\xf4\xac'),
    (b'Red', b'\xf4\xb0'),
    (b'Not', b'\xf4\xb4'),
    (b'Max', b'\xf4\xb8'),
    (b'God', b'\xf4\xbc'),
    (b'Fog', b'\xf4\xc0'),
  ]),

'ORTITLE.EXE': [],
}

WAITS = [b'}01', b'}02', b'}03', b'}04', b'}05', b'}06',]

MAX_LENGTH = {
    'Item Name': 19,
    'Item Description (Buyable)': 28,
    'Item Description': 28,                    # (Going to assume every item is buyable until I determine otherwise)
    'Item Description (Non-Buyable)': 43,
    'Equipment (Left) Name': 18,     # hand, head, boot
    'Equipment (Right) Name': 17,    # body, arms, acc
    'Equipment Description (Buyable)': 33, 
    'Equipment Description (Non-Buyable)': 46,
    'Equipment Description': 33,
    'Zen Name': 19,
    'Zen Description': 36,

    # All item and equipment names will be be padded to an odd number.
    # This should have no effect on stuff hopefully.
    # Hopefully they will still fit in equipment name buffers!

    'Dictionary': 5000,
    "Don't Compress": 5000,
}

ITEM_NAME_CATEGORIES = [
    'Item Name',
    'Equipment (Left) Name',
    'Equipment (Right) Name'
]

FdRom = Rominfo(FILE_BLOCKS, POINTER_CONSTANT, DICTIONARY_LOCATION, POINTER_TABLES,
                COMPRESSION_DICTIONARY, POINTER_DISAMBIGUATION,
                POINTERS_TO_REASSIGN, FD_EDITS, FD_CHEATS)
