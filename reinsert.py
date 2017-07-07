"""Appareden reinserter.
   Replaces text, adjusts pointers, and implements manual assembly hacks.
"""

import os

from rominfo import FILE_BLOCKS, SRC_DISK, DEST_DISK
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel

DUMP_XLS_PATH = 'appareden_sys_dump.xlsx'
#POINTER_XLS_PATH = 'crw_pointer_dump.xlsx'

Dump = DumpExcel(DUMP_XLS_PATH)
#PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump)
TargetAp = Disk(DEST_DISK)

FILES_TO_REINSERT = ['ORFIELD.EXE', 'ORTITLE.EXE']

for filename in FILES_TO_REINSERT:
    gamefile_path = os.path.join('original', filename)
    if not os.path.isfile(gamefile_path):
        OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
    gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)
    #pointers = PtrDump.get_pointers(gamefile)

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

    if filename == 'ORTITLE.EXE':
        pass
        #gamefile.edit(0x3efa, b'\x4e')       # testing pointers

    if filename == 'ORTITLE.EXE':
        for block in FILE_BLOCKS[filename]:
            print(block)
            block = Block(gamefile, block)
            previous_text_offset = block.start
            diff = 0
            #print(repr(block.blockstring))
            for t in Dump.get_translations(block):
                print(t)
                if t.en_bytestring != t.jp_bytestring and len(t.en_bytestring) - len(t.jp_bytestring) == 0:   # TODO: Obviously temporary
                    print(t)
                    loc_in_block = t.location - block.start + diff

                    #print(t.jp_bytestring)
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
