"""
    Info on Appareden rom structure and project directory layout.
"""


import os

SRC_DISK = os.path.join('original', 'Appareden.HDI')
DEST_DISK = os.path.join('patched', 'Appareden.HDI')

DUMP_XLS_PATH = 'appareden_sys_dump.xlsx'
MSG_XLS_PATH = 'appareden_msg_dump.xlsx'
POINTER_XLS_PATH = 'appareden_pointer_dump.xlsx'

SYS_DUMP_GOOGLE_SHEET = 'Appareden Sys Dump v4'
MSG_DUMP_GOOGLE_SHEET = 'Appareden Msg Dump v3'

FILES = ['ORTITLE.EXE', 'ORMAIN.EXE', 'ORFIELD.EXE', 'ORBTL.EXE', 'NEKORUN.EXE', 'SFIGHT.EXE', 'ENDING.EXE',]

MSGS = ['SCN02400.MSG', 'SCN02601.MSG', 'SCN02700.MSG', 'SCN02701.MSG',
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
        'SCN10803.MSG', 'SCN10900.MSG', 'SCN11000.MSG', 'SCN11001.MSG']

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
                (0x267ef, 0x267ff),
                (0x26855, 0x2694e),  # ui texts
                (0x26a0b, 0x26a8f),  # places
                (0x26b28, 0x26bbd),
                (0x26e16, 0x26e8a),
                (0x26e94, 0x26ef9),
                (0x26ef9, 0x26f1c),
                (0x2718d, 0x271ac),
                (0x271c1, 0x271e6),
                (0x271f8, 0x27557),
                (0x275f0, 0x275fe),  # death msg
                (0x2760e, 0x27676),  # ship msg
                (0x28044,  0x281c9),
                (0x281c9, 0x283c0),  # /, status names, status screen equipment slots
                (0x283c0, 0x2847d),  # Settings
                (0x2847d, 0x2853f),  # Equip screen header, "whose"
                (0x2853f, 0x28568),
                (0x286b1, 0x28851),  # Equip screen
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
                (0x2e9b2, 0x2ea85),
                (0x2eb4d, 0x2ef13),],  # result msgs"
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

# TODO: These are probably not usable...
SPARE_BLOCK = {
  'ORMAIN.EXE': (0x1765, 0x1f6b),
  'ORBTL.EXE': (0x26303, 0x26b54),
  'ORFIELD.EXE': (0x2f570, 0x30570),
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

S_CONTROL_CODES = {
  'w': '}',
  'c': '$',
  'n': '/'
}

B_CONTROL_CODES = {
  b'w': b'}',
  b'c': b'$',
  b'n': b'/'
}

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
}

POSTPROCESSING_CONTROL_CODES = {
    b'~': b' ',
    b'[BLANK]': b'',
}

WAITS = [b'}01', b'}02', b'}03', b'}04', b'}05', b'}06',]
