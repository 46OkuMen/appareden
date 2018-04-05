"""
    Info on Appareden rom structure and project directory layout.
"""

import os
from collections import OrderedDict

SRC_DISK = os.path.join('original', 'Appareden (UPDATED).HDI')
DEST_DISK = os.path.join('patched', 'Appareden (UPDATED).HDI')

DUMP_XLS_PATH = 'appareden_sys_dump.xlsx'
POINTER_XLS_PATH = 'appareden_pointer_dump.xlsx'

# Rows to be displayed in the progress section of the README.
PROGRESS_ROWS = ['ORTITLE.EXE', 'ORMAIN.EXE', 'ORFIELD.EXE', 'ORBTL.EXE', 'SFIGHT.EXE', 'Dialogue', 'Images']

MSGS = ['SCN02400.MSG', 'SCN02401.MSG', 'SCN02402.MSG', 'SCN02403.MSG',
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
        'SCN12803.MSG',
        ]

SHADOFF_COMPRESSED_EXES = ['ORFIELD.EXE',]

# First bytes in SJIS Japanese strings.
SJIS_FIRST_BYTES = [0x81, 0x82, 0x83, 0x84, 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0xad, 0x8e, 0x8f, 0x90, 0x91, 0x92,
                    0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f, 0xe0, 0xe1,
                    0xe2, 0xe3, 0xe4, 0x35, 0xe6, 0xe7, 0xe8, 0xe9, 0xea]
"""
#                      Gento,  Benimaru, Goemon, WeaponShop, ArmorShop,    Samurai, Hanzou, Innkeeper, ItemShop,
portrait_characters = ['幻斗', 'ベニマル', 'ゴエモン', '宿屋の主人', '防具屋の主人', '武士', 'ハンゾウ', '宿屋の主人', '道具屋の娘',
                      # Master, Koro Elder, WeaponsGeezer, Elder, AntiquesShop, Shikai, Tamamo, Nobunaga, Old Man,
                       'マスター', 'コロ長老',  '武器屋のオヤジ', '長老', '骨董品屋の主人', '四界王', 'タマモ', 'ノブナガ', '老人',
                       # Mitsukuni, Izunokami, O-Toki, Gennai, Benkei, Ginpei, Shirou, Meiling, ThDragon, Sougen,
                       'ミツクニ', 'イズノカミ',      'お時', '源内', 'ベンケイ' 'ギンペー', 'シロウ',  'メイリン', '雷竜', 'ソウゲン',
                       # O-Kuni, Okitsugu, IceDragon, FlameDragon, Kuukai, Masamune, Genpaku,
                       'お国',    'オキツグ', '氷竜',         '炎竜', 'クウカイ',   'マサムネ',  '玄白',
                       ]
"""

FILE_BLOCKS = {
    'ENDING.EXE': [(0x64bb, 0x6512), ],  # memory error texts
    'NEKORUN.EXE': [(0xa840, 0xa8aa),   # error text + scene text
                    (0xacc0, 0xacda),   # memory error text
                    (0xaecc, 0xaf00), ],  # ems driver version text"
    'ORBTL.EXE': [(0x251d2, 0x2524c),  # battle commands
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
                    (0x26641, 0x26777),  # save and ui texts
                    (0x267ef, 0x267ff),
                    (0x26855, 0x2694f),  # ui texts
                    (0x26a0b, 0x26a8f),  # places
                    (0x26b28, 0x26bbd),            # TODO: Item shop slots can go here
                    (0x26e16, 0x26f1c),            # TODO: Armor shop slots can go here
                    (0x2718d, 0x27557),
                    (0x275f0, 0x275fe),  # death msg
                    (0x2760e, 0x27626),  # ship msg
                    (0x28044, 0x28851),  # Equip screen
                    (0x2894e, 0x29020), # Equipment and such
                    (0x29020, 0x290be),  # menu msgs
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
                    (0x407b, 0x4104),   # release dates?
                    (0x5000, 0x501a), ],   # memory error"
    'SFIGHT.EXE': [(0xd090, 0xd135),   # null pointer msgs
                   (0xd4ea, 0xd586),   # names and things
                   (0xd6c6, 0xd6fa)],    # ems driver msgs"
}

# The constant added to a pointer's value to get its dereference.
POINTER_CONSTANT = {
    'ORTITLE.EXE': 0x3eb0,
    'ORMAIN.EXE': 0x1570,
    'ORFIELD.EXE': 0x25f10,
    'ORBTL.EXE': 0x25120,
    'SFIGHT.EXE': 0xd080,
}

# Location of the compression dictionary, where applicable.
DICT_LOCATION = {
    'ORFIELD.EXE': 0x2a2ba,
    'ORBTL.EXE':  0x29d38,
    'ORTITLE.EXE': None,
}

# Tables are (start, stop, stride) tuples.
POINTER_TABLES = {
    'ORMAIN.EXE': [
        (0x15a6, 0x15ac, 2),
        (0x20d4, 0x20e5, 2),
        (0x2274, 0x3ebf, 0x28),
    ],
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
  b'[ff]': bytes([0xff]),
  b'[sysLN]': b'\r\n',

}

# (??)
POSTPROCESSING_CONTROL_CODES = {

'ORFIELD.EXE': OrderedDict([
    (b'~', b' '),
    (b'[BLANK]', b''),

    (b'^The', b'\xfe\x0e'),
    (b'The', b'\xfe\x0f'),
    (b'With', b'\xfe\x13'),
    (b'That', b'\xfe\x18'),
    (b'From', b'\xfe\x1d'),
    (b'Power', b'\xfe"'),
    (b'^Katana', b'\xfe('),
    (b'Katana', b'\xfe)'),
    (b'For', b'\xfe0'),
    (b'^Zen', b'\xfe4'),
    (b'Zen', b'\xfe5'),
    (b'^Dragon', b'\xfe9'),
    (b'Dragon', b'\xfe:'),
    (b'Sword', b'\xfeA'),
    (b'^Blade', b'\xfeG'),
    (b'Blade', b'\xfeH'),
    (b'^Claws', b'\xfeN'),
    (b'Claws', b'\xfeO'),
    (b'^True', b'\xfeU'),
    (b'True', b'\xfeV'),
    (b'Enemy', b'\xfe['),
    (b'^Happi', b'\xfea'),
    (b'Happi', b'\xfeb'),
    (b'Into', b'\xfeh'),
    (b'^Holy', b'\xfem'),
    (b'Holy', b'\xfen'),
    (b'^Ultimate', b'\xfes'),
    (b'Ultimate', b'\xfet'),
    (b'^Spirit', b'\xfe}'),
    (b'Spirit', b'\xfe~'),
    (b'Battle', b'\xfe\x85'),
    (b'^Made', b'\xfe\x8c'),
    (b'Made', b'\xfe\x8d'),
    (b'^Bell', b'\xfe\x92'),
    (b'Bell', b'\xfe\x93'),
    (b'^Gold', b'\xfe\x98'),
    (b'Gold', b'\xfe\x99'),
    (b'^Tanegashima', b'\xfe\x9e'),
    (b'Tanegashima', b'\xfe\x9f'),
    (b'Containing', b'\xfe\xab'),
    (b'Through', b'\xfe\xb6'),
    (b'Spells', b'\xfe\xbe'),
    (b'^Tachi', b'\xfe\xc5'),
    (b'Tachi', b'\xfe\xc6'),
    (b'^Body', b'\xfe\xcc'),
    (b'Body', b'\xfe\xcd'),
    (b'^Use', b'\xfe\xd2'),
    (b'Use', b'\xfe\xd3'),
    (b'And', b'\xfe\xd7'),
    (b'Protects', b'\xfe\xdb'),
    (b'Enemies', b'\xfe\xe4'),
    (b'^Journal', b'\xfe\xec'),
    (b'Journal', b'\xfe\xed'),
    (b'Powers', b'\xfe\xf5'),
]),

'ORBTL.EXE': OrderedDict([
    (b'~', b' '),
    (b'[BLANK]', b''),

    (b'the', b'\xfe\r'),
    (b'text', b'\xfe\x11'),
    (b'Dragon', b'\xfe\x16'),
    (b'with', b'\xfe\x1d'),
    (b'that', b'\xfe"'),
    (b'from', b"\xfe'"),
    (b'Happi', b'\xfe,'),
    (b'Tachi', b'\xfe2'),
    (b'Charm', b'\xfe8'),
    (b'Pill', b'\xfe>'),
    (b'dragon', b'\xfeC'),
    (b'Gold', b'\xfeJ'),
    (b'Bell', b'\xfeO'),
    (b'Increase', b'\xfeT'),
    (b'Appare', b'\xfe]'),
    (b'Staff', b'\xfed'),
    (b'Claws', b'\xfej'),
    (b'Tabi', b'\xfep'),
    (b'ZP:', b'\xfeu'),
    (b'HP:', b'\xfey'),
    (b'Priest', b'\xfe}'),
    (b'Pipe', b'\xfe\x84'),
    (b'Holy', b'\xfe\x89'),
    (b'Frog', b'\xfe\x8e'),
    (b'supernatural', b'\xfe\x93'),
    (b'Tanegashima', b'\xfe\xa0'),
    (b'protection', b'\xfe\xac'),
    (b'element', b'\xfe\xb7'),
    (b'Missive', b'\xfe\xbf'),
    (b'Hanging', b'\xfe\xc7'),
    (b'Blesses', b'\xfe\xcf'),
    (b'weapon', b'\xfe\xd7'),
    (b'powers', b'\xfe\xde'),
    (b'letter', b'\xfe\xe5'),
    (b'Scroll', b'\xfe\xec'),
    (b'Rosary', b'\xfe\xf3'),

  ]),

'ORTITLE.EXE': [],
}
# TODO: Caps are a little tricky here... ^ always breaks the compressed word since it adds 20 to ef.

WAITS = [b'}01', b'}02', b'}03', b'}04', b'}05', b'}06',]

MAX_LENGTH = {
    'Item Name': 21,
    'Item Description': 43,
    'Equipment (Left) Name': 18,
    'Equipment (Right) Name': 17,
    'Equipment Description': 43,   # Not verified
    'Zen Name': 19,
    'Zen Description': 36,   # 40 in battle screen

    'Dictionary': 1000,
}