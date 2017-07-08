"""Appareden reinserter.
   Replaces text, adjusts pointers, and implements manual assembly hacks.
"""

import os
from math import floor

from rominfo import FILE_BLOCKS, SRC_DISK, DEST_DISK
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel

STRING_COUNTS = {'ORTITLE.EXE': 18,
                 'ORMAIN.EXE': 202,
                 'ORFIELD.EXE': 1050,
                 'ORBTL.EXE': 780,
                 'NEKORUN.EXE': 4,
                 'SFIGHT.EXE': 15,
                 }

TOTAL_STRING_COUNT = sum(list(STRING_COUNTS.values()))


DUMP_XLS_PATH = 'appareden_sys_dump.xlsx'
POINTER_XLS_PATH = 'appareden_pointer_dump.xlsx'

Dump = DumpExcel(DUMP_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)

FILES_TO_REINSERT = ['ORTITLE.EXE', 'ORMAIN.EXE', 'ORBTL.EXE']

total_reinserted_strings = 0

for filename in FILES_TO_REINSERT:
    gamefile_path = os.path.join('original', filename)
    if not os.path.isfile(gamefile_path):
        OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
    gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)

    reinserted_string_count = 0

    if filename == 'ORFIELD.EXE':
        gamefile.edit(0x151b7, b'\x7d')      # w = "}"
        gamefile.edit(0x15519, b'\x2f')      # n = "/"
        gamefile.edit(0x15528, b'\x2f')      # n = "/"
        gamefile.edit(0x155df, b'\x2f')      # n = "/"
        gamefile.edit(0x155ee, b'\x2f')      # n = "/"
        gamefile.edit(0x15b0f, b'\x7d')      # w = "}"
        gamefile.edit(0x15b16, b'\x24')      # c = "$"
        gamefile.edit(0x15b1d, b'\x2f')      # n = "/"
        gamefile.edit(0x15b5f, b'\x2f')      # n = "/"
        gamefile.edit(0x15b6c, b'\x24')      # c = "$"
        gamefile.edit(0x15b99, b'\x7d')      # w = "}"
        gamefile.edit(0x2551b, b'\x24')      # c = "$"

    for block in FILE_BLOCKS[filename]:
        block = Block(gamefile, block)
        previous_text_offset = block.start
        diff = 0
        for t in Dump.get_translations(block):
            if t.en_bytestring != t.jp_bytestring:
                loc_in_block = t.location - block.start + diff
                i = block.blockstring.index(t.jp_bytestring)
                j = block.blockstring.count(t.jp_bytestring)

                index = 0
                while index < len(block.blockstring):
                    index = block.blockstring.find(t.jp_bytestring, index)
                    if index == -1:
                        break
                    #print('jp bytestring found at', index)
                    index += len(t.jp_bytestring) # +2 because len('ll') == 2

                #if j > 1:
                #    print("%s multiples of this string found" % j)
                assert loc_in_block == i, (hex(loc_in_block), hex(i))

                block.blockstring = block.blockstring.replace(t.jp_bytestring, t.en_bytestring, 1)
                reinserted_string_count += 1

                gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                previous_text_offset = t.location

                this_diff = len(t.en_bytestring) - len(t.jp_bytestring)
                diff += this_diff


        block_diff = len(block.blockstring) - len(block.original_blockstring)
        if block_diff < 0:
            block.blockstring += (-1)*block_diff*b'\x00'
        block_diff = len(block.blockstring) - len(block.original_blockstring)
        assert block_diff == 0, block_diff

        block.incorporate()

    gamefile.write(path_in_disk='TGL\\OR')
    percentage = int(floor((reinserted_string_count / STRING_COUNTS[filename] * 100)))
    print(filename, str(percentage), "% complete", "(%s / %s)" % (reinserted_string_count, STRING_COUNTS[filename]))

    total_reinserted_strings += reinserted_string_count
    #print ("(%s / %s)\n" % (self.translated_strings, self.total_strings))

percentage = int(floor((total_reinserted_strings / TOTAL_STRING_COUNT * 100)))
print("Appareden System %s percent complete (%s / %s)" % (str(percentage), total_reinserted_strings, TOTAL_STRING_COUNT))