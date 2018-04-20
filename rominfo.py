"""
    Info on Appareden rom structure and project directory layout.
"""

import os
from collections import OrderedDict
from pointer_info import POINTER_DISAMBIGUATION, POINTERS_TO_REASSIGN
from appareden.asm import FD_EDITS

SRC_DIR = 'original'
DEST_DIR = 'patched'

SRC_DISK = os.path.join(SRC_DIR, 'Appareden (UPDATED).HDI')
#SRC_CD_DISK = os.path.join('original_cd', 'Appareden (CD-UPDATED).hdi')
DEST_DISK = os.path.join(DEST_DIR, 'Appareden (UPDATED).HDI')
#DEST_CD_DISK = os.path.join('patched_cd', 'Appareden (CD-UPDATED).hdi')

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
                 asm_edits):
        self.file_blocks = file_blocks
        self.pointer_constant = pointer_constant
        self.dictionary_location = dictionary_location
        self.pointer_tables = pointer_tables
        self.compression_dictionary = compression_dictionary
        self.pointer_disambiguation = pointer_disambiguation
        self.pointers_to_reassign = pointers_to_reassign
        self.asm_edits = asm_edits

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
                    (0x26b28, 0x26bbd),            # TODO: Item shop slots can go here
                    (0x26e16, 0x26f1d),            # TODO: Armor shop slots can go here
                    (0x2718d, 0x27557),
                    (0x275f0, 0x275fe),  # death msg
                    (0x2760e, 0x27627),  # ship msg
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
    (b'~', b' '),
    (b'[BLANK]', b''),
    (b'[O]', b'O\x7e'),
    (b'[o]', b'o\x7e'),
    (b'[U]', b'U\x7e'),
    (b'[u]', b'u\x7e'),

    (b'the', b'\xf0\r'),
    (b'with', b'\xf0\x11'),
    (b'that', b'\xf0\x16'),
    (b'The', b'\xf0\x1b'),
    (b'from', b'\xf0\x1f'),
    (b'power', b'\xf0$'),
    (b'katana', b'\xf0*'),
    (b'sword', b'\xf01'),
    (b'True', b'\xf07'),
    (b'for', b'\xf0<'),
    (b'Zen', b'\xf0@'),
    (b'containing', b'\xf0D'),
    (b'blade', b'\xf0O'),
    (b'Ultimate', b'\xf0U'),
    (b'made', b'\xf0^'),
    (b'holy', b'\xf0c'),
    (b'enemy', b'\xf0h'),
    (b'bell', b'\xf0n'),
    (b'happi', b'\xf0s'),
    (b'into', b'\xf0y'),
    (b'body', b'\xf0~'),
    (b'use', b'\xf0\x83'),
    (b'Journal', b'\xf0\x87'),
    (b'battle', b'\xf0\x8f'),
    (b'god', b'\xf0\x96'),
    (b'can', b'\xf0\x9a'),
    (b'restores', b'\xf0\x9e'),
    (b'protects', b'\xf0\xa7'),
    (b'through', b'\xf0\xb0'),
    (b'socks', b'\xf0\xb8'),
    (b'light', b'\xf0\xbe'),
    (b'Claws', b'\xf0\xc4'),
    (b'evil', b'\xf0\xca'),
    (b'coat', b'\xf0\xcf'),
    (b'and', b'\xf0\xd4'),
    (b'lightning', b'\xf0\xd8'),
    (b'magical', b'\xf0\xe2'),
    (b'enemies', b'\xf0\xea'),
    (b'Receive', b'\xf0\xf2'),
    (b'weapon', b'\xf0\xfa'),
    (b'dragon', b'\xf1\x01'),
    (b'Status', b'\xf1\x08'),
    (b'peace', b'\xf1\x0f'),
    (b'tabi', b'\xf1\x15'),
    (b'pill', b'\xf1\x1a'),
    (b'Symbolizes', b'\xf1\x1f'),
    (b'legendary', b'\xf1*'),
    (b'Equipment', b'\xf14'),
    (b'strength', b'\xf1>'),
    (b'favorite', b'\xf1G'),
    (b'&5Unable', b'\xf1P'),
    (b'Blesses', b'\xf1Y'),
    (b'sacred', b'\xf1a'),
    (b'letter', b'\xf1h'),
    (b'health', b'\xf1o'),
    (b'Myouou', b'\xf1v'),
    (b'staff', b'\xf1}'),
    (b'soul', b'\xf1\x83'),
    (b'Sell', b'\xf1\x88'),
    (b'Arms', b'\xf1\x8d'),
    (b'axe', b'\xf1\x92'),
    (b'Gem', b'\xf1\x96'),
    (b'Tanegashima', b'\xf1\x9a'),
    (b'resistance', b'\xf1\xa6'),
    (b'increased~', b'\xf1\xb1'),
    (b'blessings', b'\xf1\xbc'),
    (b'Lightning', b'\xf1\xc6'),
    (b'defender', b'\xf1\xd0'),
    (b'attached', b'\xf1\xd9'),
    (b'Increase', b'\xf1\xe2'),
    (b'special', b'\xf1\xeb'),
    (b"enemy's", b'\xf1\xf3'),
    (b'Leather', b'\xf1\xfb'),
    (b'spirit', b'\xf2\x03'),
    (b'silver', b'\xf2\n'),
    (b'points', b'\xf2\x11'),
    (b'imbued', b'\xf2\x18'),
    (b'breath', b'\xf2\x1f'),
    (b'Spirit', b'\xf2&'),
    (b'white', b'\xf2-'),
    (b'robes', b'\xf23'),
    (b'meant', b'\xf29'),
    (b'&5Not', b'\xf2?'),
    (b'war,', b'\xf2E'),
    (b'ring', b'\xf2J'),
    (b'pipe', b'\xf2O'),
    (b'gods', b'\xf2T'),
    (b'Type', b'\xf2Y'),
    (b'Gold', b'\xf2^'),
    (b'you', b'\xf2c'),
    (b'one', b'\xf2g'),
    (b'any', b'\xf2k'),
    (b'supernatural', b'\xf2o'),
    (b'protection', b'\xf2|'),
    (b'concealing', b'\xf2\x87'),
    (b'recovered', b'\xf2\x92'),
    (b'protected', b'\xf2\x9c'),
    (b'beautiful', b'\xf2\xa6'),
    (b'Snowflake', b'\xf2\xb0'),
    (b'Longevity', b'\xf2\xba'),
    (b'Increases', b'\xf2\xc4'),
    (b'shuriken', b'\xf2\xce'),
    (b'darkness', b'\xf2\xd7'),
    (b'blessing', b'\xf2\xe0'),
    (b'Strength', b'\xf2\xe9'),
    (b'quality', b'\xf2\xf2'),
    (b'pattern', b'\xf2\xfa'),
    (b'crystal', b'\xf3\x02'),
    (b'created', b'\xf3\n'),
    (b'attacks', b'\xf3\x12'),
    (b'ancient', b'\xf3\x1a'),
    (b'Defense', b'\xf3"'),
    (b'within', b'\xf3*'),
    (b'spells', b'\xf31'),
    (b'lowers', b'\xf38'),
    (b'flames', b'\xf3?'),
    (b'enough', b'\xf3F'),
    (b'Meteor', b'\xf3M'),
    (b'Icicle', b'\xf3T'),
    (b'Choose', b'\xf3['),
    (b'short', b'\xf3b'),
    (b'lower', b'\xf3h'),
    (b'heavy', b'\xf3n'),
    (b'crest', b'\xf3t'),
    (b'Karma', b'\xf3z'),
    (b'Items', b'\xf3\x80'),
    (b'Blaze', b'\xf3\x86'),
    (b'&5You', b'\xf3\x8c'),
    (b'will', b'\xf3\x92'),
    (b'more', b'\xf3\x97'),
    (b'love', b'\xf3\x9c'),
    (b'have', b'\xf3\xa1'),
    (b'gold', b'\xf3\xa6'),
    (b'full', b'\xf3\xab'),
    (b'fire', b'\xf3\xb0'),
    (b'easy', b'\xf3\xb5'),
    (b'club', b'\xf3\xba'),
    (b'book', b'\xf3\xbf'),
    (b'arts', b'\xf3\xc4'),
    (b'This', b'\xf3\xc9'),
    (b'Name', b'\xf3\xce'),
    (b'Item', b'\xf3\xd3'),
    (b'Head', b'\xf3\xd8'),
    (b'Hand', b'\xf3\xdd'),
    (b'Boot', b'\xf3\xe2'),
    (b'Body', b'\xf3\xe7'),
    (b"&f's", b'\xf3\xec'),
    (b'gun', b'\xf3\xf1'),
    (b'gem', b'\xf3\xf5'),
    (b'art', b'\xf3\xf9'),
    (b'all', b'\xf3\xfd'),
    (b'Use', b'\xf4\x01'),
    (b'God', b'\xf4\x05'),
    (b'Fog', b'\xf4\t'),
    (b'Acc', b'\xf4\r'),
    (b'Conflagration', b'\xf4\x11'),
    (b'miniaturized', b'\xf4\x1f'),
    (b'manji-shaped', b'\xf4,'),
    (b'Stonebreaker', b'\xf49'),
    (b'embroidered', b'\xf4F'),
    (b'beautifully', b'\xf4R'),
    (b'Anti-Spirit', b'\xf4^'),
    (b'&frecovered', b'\xf4j'),
    (b'reinforced', b'\xf4v'),
    (b'mysterious', b'\xf4\x81'),
    (b'Permafrost', b'\xf4\x8c'),
    (b'salvation', b'\xf4\x97'),
    (b'recording', b'\xf4\xa1'),
    (b'increases', b'\xf4\xab'),
    (b'gauntlets', b'\xf4\xb5'),
    (b'admirable', b'\xf4\xbf'),
    (b'Transform', b'\xf4\xc9'),
    (b'Protected', b'\xf4\xd3'),
    (b'Furyquake', b'\xf4\xdd'),
    (b'Amaterasu', b'\xf4\xe7'),
    (b'warriors', b'\xf4\xf1'),
    (b'requires', b'\xf4\xfa'),
    (b'imported', b'\xf5\x03'),
    (b'headband', b'\xf5\x0c'),
    (b'fighting', b'\xf5\x15'),
    (b'efficacy', b'\xf5\x1e'),
    (b'crescent', b"\xf5'"),
    (b'acquired', b'\xf50'),
    (b'Manjusri', b'\xf59'),
    (b"Heaven's", b'\xf5B'),
    (b"Goemon's", b'\xf5K'),
    (b'Generate', b'\xf5T'),
    (b"Dragon's", b'\xf5]'),
    (b'samurai', b'\xf5f'),
    (b'restore', b'\xf5n'),
    (b'protect', b'\xf5v'),
    (b'polearm', b'\xf5~'),
    (b'icicles', b'\xf5\x86'),
    (b'defends', b'\xf5\x8e'),
    (b'clothes', b'\xf5\x96'),
    (b'agility', b'\xf5\x9e'),
    (b'against', b'\xf5\xa6'),
    (b'Silence', b'\xf5\xae'),
    (b'wisdom', b'\xf5\xb6'),
    (b"that's", b'\xf5\xbd'),
    (b'sturdy', b'\xf5\xc4'),
    (b'random', b'\xf5\xcb'),
    (b'proper', b'\xf5\xd2'),
    (b'plates', b'\xf5\xd9'),
    (b'normal', b'\xf5\xe0'),
    (b'mobile', b'\xf5\xe7'),
    (b'mirror', b'\xf5\xee'),
    (b'master', b'\xf5\xf5'),
    (b'forged', b'\xf5\xfc'),
    (b'famous', b'\xf6\x03'),
    (b'escape', b'\xf6\n'),
    (b'energy', b'\xf6\x11'),
    (b'elixir', b'\xf6\x18'),
    (b'effect', b'\xf6\x1f'),
    (b'cursed', b'\xf6&'),
    (b'collar', b'\xf6-'),
    (b'attack', b'\xf64'),
    (b'Talons', b'\xf6;'),
    (b'Summon', b'\xf6B'),
    (b'Poison', b'\xf6I'),
    (b'Escape', b'\xf6P'),
    (b'Attack', b'\xf6W'),
    (b'Appare', b'\xf6^'),
    (b'~~Who', b'\xf6e'),
    (b'times', b'\xf6k'),
    (b'their', b'\xf6q'),
    (b'surge', b'\xf6w'),
    (b'super', b'\xf6}'),
    (b'steel', b'\xf6\x83'),
    (b'spear', b'\xf6\x89'),
    (b'small', b'\xf6\x8f'),
    (b'sharp', b'\xf6\x95'),
    (b'rigid', b'\xf6\x9b'),
    (b'party', b'\xf6\xa1'),
    (b'ninja', b'\xf6\xa7'),
    (b'named', b'\xf6\xad'),
    (b'fully', b'\xf6\xb3'),
    (b'flesh', b'\xf6\xb9'),
    (b'flame', b'\xf6\xbf'),
    (b"don't", b'\xf6\xc5'),
    (b'demon', b'\xf6\xcb'),
    (b'cured', b'\xf6\xd1'),
    (b'cover', b'\xf6\xd7'),
    (b'break', b'\xf6\xdd'),
    (b'black', b'\xf6\xe3'),
    (b'armor', b'\xf6\xe9'),
    (b'apple', b'\xf6\xef'),
    (b'Storm', b'\xf6\xf5'),
    (b'Price', b'\xf6\xfb'),
    (b'Metal', b'\xf7\x01'),
    (b'Light', b'\xf7\x07'),
    (b'Level', b'\xf7\r'),
    (b'Gimme', b'\xf7\x13'),
    (b'15-40', b'\xf7\x19'),
    (b'10-20', b'\xf7\x1f'),
    (b'your', b'\xf7%'),
    (b'used', b'\xf7*'),
    (b'snow', b'\xf7/'),
    (b'over', b'\xf74'),
    (b'moon', b'\xf79'),
    (b'many', b'\xf7>'),
    (b'like', b'\xf7C'),
    (b'item', b'\xf7H'),
    (b'here', b'\xf7M'),
    (b'heal', b'\xf7R'),
    (b'feet', b'\xf7W'),
    (b'fall', b'\xf7\\'),
    (b'cold', b'\xf7a'),
    (b'bone', b'\xf7f'),
    (b'ball', b'\xf7k'),
    (b'back', b'\xf7p'),
    (b'away', b'\xf7u'),
    (b'Turn', b'\xf7z'),
    (b'Tabi', b'\xf7\x7f'),
    (b'Sake', b'\xf7\x84'),
    (b'Holy', b'\xf7\x89'),
    (b'Gale', b'\xf7\x8e'),
    (b'Call', b'\xf7\x93'),
    (b'&fHP', b'\xf7\x98'),
    (b'zen', b'\xf7\x9d'),
    (b'was', b'\xf7\xa1'),
    (b'too', b'\xf7\xa5'),
    (b'out', b'\xf7\xa9'),
    (b'ice', b'\xf7\xad'),
    (b'hot', b'\xf7\xb1'),
    (b'has', b'\xf7\xb5'),
    (b'are', b'\xf7\xb9'),
    (b'Has', b'\xf7\xbd'),
    (b'Buy', b'\xf7\xc1'),
]),

'ORBTL.EXE': OrderedDict([
    (b'~', b' '),
    (b'[BLANK]', b''),
    (b'[O]', b'O\x7e'),
    (b'[o]', b'o\x7e'),
    (b'[U]', b'U\x7e'),
    (b'[u]', b'u\x7e'),

    (b'the', b'\xf0\r'),
    (b'with', b'\xf0\x11'),
    (b'Dragon', b'\xf0\x16'),
    (b'True', b'\xf0\x1d'),
    (b'Ultimate', b'\xf0"'),
    (b'Happi', b'\xf0+'),
    (b'enemy', b'\xf01'),
    (b'Charm', b'\xf07'),
    (b'Tachi', b'\xf0='),
    (b'from', b'\xf0C'),
    (b'Bell', b'\xf0H'),
    (b'Appare', b'\xf0M'),
    (b'Staff', b'\xf0T'),
    (b'Claws', b'\xf0Z'),
    (b'that', b'\xf0`'),
    (b'Tabi', b'\xf0e'),
    (b'Zen', b'\xf0j'),
    (b'ZP:', b'\xf0n'),
    (b'HP:', b'\xf0r'),
    (b'Priest', b'\xf0v'),
    (b'into', b'\xf0}'),
    (b'Pipe', b'\xf0\x82'),
    (b'Pill', b'\xf0\x87'),
    (b'Holy', b'\xf0\x8c'),
    (b'Gold', b'\xf0\x91'),
    (b'Tanegashima', b'\xf0\x96'),
    (b'enemies', b'\xf0\xa2'),
    (b'element', b'\xf0\xaa'),
    (b'Hanging', b'\xf0\xb2'),
    (b'Blesses', b'\xf0\xba'),
    (b'weapon', b'\xf0\xc2'),
    (b'Spirit', b'\xf0\xc9'),
    (b'Rosary', b'\xf0\xd0'),
    (b'Collar', b'\xf0\xd7'),
    (b'Robes', b'\xf0\xde'),
    (b'Grail', b'\xf0\xe4'),
    (b'Ring', b'\xf0\xea'),
    (b'Frog', b'\xf0\xef'),
    (b'Fang', b'\xf0\xf4'),
    (b'and', b'\xf0\xf9'),
    (b'resistance', b'\xf0\xfd'),
    (b'lightning', b'\xf1\x08'),
    (b'Longevity', b'\xf1\x12'),
    (b'Lightning', b'\xf1\x1c'),
    (b'Increase', b'\xf1&'),
    (b"enemy's", b'\xf1/'),
    (b'breath', b'\xf17'),
    (b'Votive', b'\xf1>'),
    (b'Light', b'\xf1E'),
    (b'pill', b'\xf1K'),
    (b'holy', b'\xf1P'),
    (b'all', b'\xf1U'),
    (b'containing', b'\xf1Y'),
    (b'Transform', b'\xf1d'),
    (b'Snowflake', b'\xf1n'),
    (b'Ochimusha', b'\xf1x'),
    (b'Amaterasu', b'\xf1\x82'),
    (b'through', b'\xf1\x8c'),
    (b'Silver', b'\xf1\x94'),
    (b'Meteor', b'\xf1\x9b'),
    (b'Kimono', b'\xf1\xa2'),
    (b'Katana', b'\xf1\xa9'),
    (b'Icicle', b'\xf1\xb0'),
    (b'Golden', b'\xf1\xb7'),
    (b'Falcon', b'\xf1\xbe'),
    (b'Casual', b'\xf1\xc5'),
    (b'Benkei', b'\xf1\xcc'),
    (b'power', b'\xf1\xd3'),
    (b'lower', b'\xf1\xd9'),
    (b'White', b'\xf1\xdf'),
    (b'Vajra', b'\xf1\xe5'),
    (b'Tiger', b'\xf1\xeb'),
    (b'Tengu', b'\xf1\xf1'),
    (b'Stone', b'\xf1\xf7'),
    (b'Mochi', b'\xf1\xfd'),
    (b'Earth', b'\xf2\x03'),
    (b'Death', b'\xf2\t'),
    (b'Blaze', b'\xf2\x0f'),
    (b'Blade', b'\xf2\x15'),
    (b'Type', b'\xf2\x1b'),
    (b'Soul', b'\xf2 '),
    (b'Koma', b'\xf2%'),
    (b'Gale', b'\xf2*'),
    (b'Fire', b'\xf2/'),
    (b'Evil', b'\xf24'),
    (b'The', b'\xf29'),
    (b'Old', b'\xf2='),
    (b'Cat', b'\xf2A'),
    (b'Conflagration', b'\xf2E'),
    (b'Stonebreaker', b'\xf2S'),
    (b'Anti-Spirit', b'\xf2`'),
    (b'Permafrost', b'\xf2l'),
    (b'Neutralize', b'\xf2w'),
    (b'Hallelujah', b'\xf2\x82'),
    (b'spiritual', b'\xf2\x8d'),
    (b'Tsukuyomi', b'\xf2\x97'),
    (b'Moonlight', b'\xf2\xa1'),
    (b'Furyquake', b'\xf2\xab'),
    (b'protects', b'\xf2\xb5'),
    (b'fighting', b'\xf2\xbe'),
    (b'Training', b'\xf2\xc7'),
    (b'Recovery', b'\xf2\xd0'),
    (b'Masamune', b'\xf2\xd9'),
    (b'Judgment', b'\xf2\xe2'),
    (b'Headband', b'\xf2\xeb'),
    (b'Generate', b'\xf2\xf4'),
    (b'Gauntlet', b'\xf2\xfd'),
    (b"Dragon's", b'\xf3\x06'),
    (b'Silence', b'\xf3\x0f'),
    (b'Samurai', b'\xf3\x17'),
    (b'Leather', b'\xf3\x1f'),
    (b'Induces', b"\xf3'"),
    (b'Defense', b'\xf3/'),
    (b'Breaker', b'\xf37'),
    (b'spirit', b'\xf3?'),
    (b'random', b'\xf3F'),
    (b'mirror', b'\xf3M'),
    (b'enough', b'\xf3T'),
    (b'elixir', b'\xf3['),
    (b'Thread', b'\xf3b'),
    (b'Summon', b'\xf3i'),
    (b'Shogun', b'\xf3p'),
    (b'Scroll', b'\xf3w'),
    (b'Sacred', b'\xf3~'),
    (b'Poison', b'\xf3\x85'),
    (b'Leaves', b'\xf3\x8c'),
    (b'Helper', b'\xf3\x93'),
    (b'Hanzou', b'\xf3\x9a'),
    (b'Elixir', b'\xf3\xa1'),
    (b'Copper', b'\xf3\xa8'),
    (b'Choice', b'\xf3\xaf'),
    (b'Broken', b'\xf3\xb6'),
    (b'Bashou', b'\xf3\xbd'),
    (b'Attack', b'\xf3\xc4'),
    (b'surge', b'\xf3\xcb'),
    (b'space', b'\xf3\xd1'),
    (b'party', b'\xf3\xd7'),
    (b'dulls', b'\xf3\xdd'),
    (b'Water', b'\xf3\xe3'),
    (b'Storm', b'\xf3\xe9'),
    (b'Santa', b'\xf3\xef'),
    (b'Manji', b'\xf3\xf5'),
    (b'Lucia', b'\xf3\xfb'),
    (b'Haori', b'\xf4\x01'),
    (b'Grass', b'\xf4\x07'),
    (b'Gimme', b'\xf4\r'),
    (b'Flute', b'\xf4\x13'),
    (b'Dress', b'\xf4\x19'),
    (b'Demon', b'\xf4\x1f'),
    (b'text', b'\xf4%'),
    (b'soul', b'\xf4*'),
    (b'fire', b'\xf4/'),
    (b'dark', b'\xf44'),
    (b'body', b'\xf49'),
    (b'ball', b'\xf4>'),
    (b'away', b'\xf4C'),
    (b'Turn', b'\xf4H'),
    (b'Sake', b'\xf4M'),
    (b'Pray', b'\xf4R'),
    (b'Name', b'\xf4W'),
    (b'Moon', b'\xf4\\'),
    (b'Mask', b'\xf4a'),
    (b'Item', b'\xf4f'),
    (b'Hell', b'\xf4k'),
    (b'Gear', b'\xf4p'),
    (b'Dark', b'\xf4u'),
    (b'Crow', b'\xf4z'),
    (b'Call', b'\xf4\x7f'),
    (b'Book', b'\xf4\x84'),
    (b'Arms', b'\xf4\x89'),
    (b'out', b'\xf4\x8e'),
    (b'one', b'\xf4\x92'),
    (b'fog', b'\xf4\x96'),
    (b'Six', b'\xf4\x9a'),
    (b'Red', b'\xf4\x9e'),
    (b'Not', b'\xf4\xa2'),
    (b'Ice', b'\xf4\xa6'),
    (b'Fog', b'\xf4\xaa'),

  ]),

'ORTITLE.EXE': [],
}

WAITS = [b'}01', b'}02', b'}03', b'}04', b'}05', b'}06',]

MAX_LENGTH = {
    'Item Name': 19,
    'Item Description': 28,          # Not finalized. Can be longer if I can move the window
    # TODO: Item and Equipment descriptions can be longer if they are not in any shops.
        # Need to figure out what's in every shop...
    'Equipment (Left) Name': 18,     # hand, head, boot
    'Equipment (Right) Name': 17,    # body, arms, acc
    'Equipment Description': 33,     # Not finalized. Can be longer if I can move the window
    'Zen Name': 19,
    'Zen Description': 36,   # 40 in battle screen

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
                POINTERS_TO_REASSIGN, FD_EDITS)
