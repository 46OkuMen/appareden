"""
    Info on Appareden CD rom structure and project directory layout.
"""

import os
import rominfo
import pointer_info

SRC_DISK = os.path.join('original_CD', 'Appareden (CD-UPDATED).HDI')
DEST_DISK = os.path.join('patched_CD', 'Appareden (CD-UPDATED).HDI')

DUMP_XLS_PATH = 'appareden_sys_dump.xlsx'
POINTER_XLS_PATH = 'appareden_pointer_dump.xlsx'


def orfield_fd_to_cd(n):
    """
        Given an offset in ORFIELD.EXE FD, return the CD offset.
    """
    if n < 0x2663e:
        return n + 1568
    else:
        return n + 1606


def orbtl_fd_to_cd(n):
    """
        Given an offset in ORBTL.EXE FD, return the CD offset.
    """
    if 0x151d2 <= n < 0x2715a:
        return n + 528
    elif 0x2715a <= n < 0x28178:
        return n - 1470
    else:
        return n - 1442

FILE_BLOCKS = {
    'ORFIELD.EXE': [(0x26740, 0x267b6),
                    (0x26988, 0x26a64),
                    (0x26c84, 0x26dbd),
                    (0x26e35, 0x26e45),
                    (0x26e9b, 0x26f95),
                    (0x27051, 0x270d6),
                    (0x2716e, 0x27204),
                    (0x2745c, 0x27563),
                    (0x277d3, 0x27b9e),
                    (0x27c33, 0x27c45),
                    (0x27c54, 0x27c6d),
                    (0x2868a, 0x28da7),
                    (0x28f94, 0x29667),
                    (0x29667, 0x29704),
                    (0x2a900, 0x2d28c),
                    (0x2d668, 0x2da0c),
                    (0x2e0ba, 0x2ecd8),
                    (0x2eff8, 0x2f0cb),
                    (0x2f193, 0x2f55a)],
    'ORBTL.EXE': [],
}

#for fb in rominfo.FILE_BLOCKS['ORFIELD.EXE']:
#    FILE_BLOCKS['ORFIELD.EXE'].append((orfield_fd_to_cd(fb[0]), orfield_fd_to_cd(fb[1])))

for fb in rominfo.FILE_BLOCKS['ORBTL.EXE']:
    FILE_BLOCKS['ORBTL.EXE'].append((orbtl_fd_to_cd(fb[0]), orbtl_fd_to_cd(fb[1])))

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
        (0x2b0bc, 0x2b1fe, 0x28), # done
        (0x2b224, 0x2cd07, 0x28), # done
    ],
    'SFIGHT.EXE': [],
    'ORFIELD.EXE': [
        (0x266c8, 0x266dc, 2),    # done
        (0x26982, 0x26988, 2),    # done
        (0x26c34, 0x26c84, 2),    # done
        (0x27028, 0x27040, 2),    # done
        (0x270d6, 0x270dc, 2),    # done
        (0x270e6, 0x270f0, 2),    # done
        (0x27116, 0x27140, 2),    # done
        (0x2714a, 0x2716c, 2),    # done
        (0x28546, 0x285d6, 2),    # done
        (0x285ea, 0x28687, 2),    # done
        (0x29704, 0x29a8a, 0xc),  # done
        (0x29a94, 0x29b3a, 2),    # done
        (0x29b4a, 0x2a77c, 0x10), # done
        (0x2a77c, 0x2a900, 2),    # done     # problems
        (0x2da0c, 0x2dd8c, 0xe),  # done
        (0x2dd8c, 0x2de0a, 2),    # done
        (0x2de0c, 0x2e0ae, 0x10), # done
        (0x2e0ac, 0x2e0ba, 2),
    ]
}

POINTER_DISAMBIGUATION  = {
    0x27527: 0x16ef7,
    0x2752c: 0x16f06,
    0x27818: 0x176a0,
    0x27b30: 0x17bd2,
    0x27b77: 0x17de4,
    0x28d35: 0x1c6da,
    0x28fad: 0x1d935,
    0x2d698: 0x217d6,
    0x2d698: 0x217d6,
    0x2d798: 0x21edb,
    0x2d7b1: 0x21f83,
    0x2eff8: 0x23484,
    0x2f028: 0x23595,
    0x2f041: 0x23602,
    0x2f2ea: 0x23b7d,
}

POINTERS_TO_REASSIGN = {
    'ORFIELD.EXE': [],
    'ORBTL.EXE': []
}


for src, dest in pointer_info.POINTERS_TO_REASSIGN['ORFIELD.EXE']:
    POINTERS_TO_REASSIGN = (orfield_fd_to_cd(src), orfield_fd_to_cd(dest))

for src, dest in pointer_info.POINTERS_TO_REASSIGN['ORBTL.EXE']:
    POINTERS_TO_REASSIGN = (orbtl_fd_to_cd(src), orbtl_fd_to_cd(dest))
