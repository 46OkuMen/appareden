"""
    Info on Appareden CD rom structure and project directory layout.
"""

import os
from collections import OrderedDict

SRC_DISK = os.path.join('original_CD', 'Appareden (CD-UPDATED).HDI')
DEST_DISK = os.path.join('patched_CD', 'Appareden (CD-UPDATED).HDI')

DUMP_XLS_PATH = 'appareden_sys_dump.xlsx'
POINTER_XLS_PATH = 'appareden_pointer_dump.xlsx'

# These are done
POINTER_CONSTANT = {
    'ORTITLE.EXE': 0x40b0,
    'ORFIELD.EXE': 0x26530,
    'ORBTL.EXE': 0x25330,
}

# Tables are (start, stop, stride) tuples.
POINTER_TABLES = {
    #'ORTITLE.EXE': [
    #    (0x3ee4, 0x3f16, 2),
    #],
    'ORBTL.EXE': [
        (0x25364, 0x25388, 2),    # done
        (0x2619e, 0x261a2, 2),    # done
        (0x26c3c, 0x26c42, 2),    # done
        (0x26c44, 0x26c4a, 4),    # done
        (0x274ae, 0x27830, 0xe),  # done
        (0x27830, 0x278ae, 2),    # done
        (0x278ae, 0x27b4e, 0x10), # done
        (0x27bc8, 0x27bd8, 2),    # done
        (0x28720, 0x28abc, 12),   # done
        (0x28abc, 0x28b56, 2),    # done
        (0x28b66, 0x29796, 16),   # done
        (0x2af1c, 0x2af2d, 2),    # done
        (0x2af2d, 0x2b1fe, 0x28), # done
        (0x2b224, 0x2cd08, 0x28), # done

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