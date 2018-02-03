"""
    Text reinserter for Appareden.
    Replaces text, adjusts pointers, and implements manual assembly hacks.
"""

import os
from rominfo import FILE_BLOCKS, SRC_DISK, DEST_DISK
from rominfo import DUMP_XLS_PATH, POINTER_XLS_PATH
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel


Dump = DumpExcel(DUMP_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)

words = {}


FILES_TO_REINSERT = ['ORFIELD.EXE',]

for filename in FILES_TO_REINSERT:
    gamefile_path = os.path.join('original', filename)
    if not os.path.isfile(gamefile_path):
        OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
    gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)

    block_objects = [Block(gamefile, block) for block in FILE_BLOCKS[filename]]
    overflow_strings = []
    spares = []

    for block in block_objects:
        previous_text_offset = block.start
        overflowing = False
        overflow_start = 0
        diff = 0
        not_translated = False
        last_i = -1
        last_len = 1
        last_string_original_location = 0
        for t in Dump.get_translations(block):
            for w in t.english.split():
                if len(w) > 2:
                    if w in words:
                        words[w] += 1
                    else:
                        words[w] = 1

for i in sorted(words.items(), key=lambda x:x[1]):
    print(i)

# TODO: Find the 255 chars with the most repeats, then stick them in the dict
#       and calculate their offsets, then replace text with [fe offset].
# Also ignore [BLANK]s and ~s.

# Also, might want to do this with kuoushi translations and not mine.