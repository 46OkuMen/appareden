import os

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
    'ORFIELD.EXE': [(0x25f20, 0x25f40),  # null pointer error
                (0x25f72, 0x25fba),  # ems driver version texts
                (0x26120, 0x26195),  # names and memory error text
                (0x26368, 0x26444),  # memory and disk switches
                (0x26641, 0x26776),  # save and ui texts
                (0x267ef, 0x2694e),  # ui texts
                (0x26a0b, 0x26a8f),  # places
                (0x26b28, 0x27557),  # shops and inns
                (0x275f0, 0x275fe),  # death msg
                (0x2760e, 0x27676),  # ship msg
                (0x28044, 0x290bc),  # menu msgs
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

SPARE_BLOCKS = {
  'ORMAIN.EXE': (0x1765, 0x1f6b),
}