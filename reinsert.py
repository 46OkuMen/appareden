"""Appareden reinserter.
   Replaces text, adjusts pointers, and implements manual assembly hacks.
"""

import os
import re
from math import floor
from rominfo import FILE_BLOCKS, SRC_DISK, DEST_DISK, SPARE_BLOCK, typeset, CONTROL_CODES, ORIGINAL_CONTROL_CODES, shadoff_compress
from rominfo import SPACECODE_ASM, OVERLINE_ASM, SHADOFF_ASM
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
MSG_XLS_PATH = 'appareden_msg_dump.xlsx'
POINTER_XLS_PATH = 'appareden_pointer_dump.xlsx'

Dump = DumpExcel(DUMP_XLS_PATH)
MsgDump = DumpExcel(MSG_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)

FILES_TO_REINSERT = ['ORFIELD.EXE']

FILES_TO_REINSERT += ['SCN%s.MSG' % str(t).zfill(5) for t in range(2400, 2405)]

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

        # ORFIELD.EXE text handling ASM
        gamefile.edit(0x8c0a, SPACECODE_ASM)
        gamefile.edit(0x8c0a+len(SPACECODE_ASM), OVERLINE_ASM)
        gamefile.edit(0x8c0a+len(SPACECODE_ASM)+len(OVERLINE_ASM), SHADOFF_ASM)

    if filename.endswith('.MSG'):
        # First, gotta replace all the control codes.

        # How to replace the ones with no > in front of them?
        #plain_control_code_regex = rb'/[^>]([cnw])'
        #pattern = re.compile(plain_control_code_regex)

        #print(pattern.match(gamefile.filestring))

        #gamefile.filestring = gamefile.filestring.replace(b'\x83\x6e', b'QQ')
        #gamefile.filestring = gamefile.filestring.replace(b'\x83\x63', b'RR')
        #gamefile.filestring = gamefile.filestring.replace(b'\x81\x63', b'RW')
        #gamefile.filestring = gamefile.filestring.replace(b'\x93\x6e', b'QR')


        gamefile.filestring = gamefile.filestring.replace(b'>n', b'NN')
        gamefile.filestring = gamefile.filestring.replace(b'>c', b'CC')


        gamefile.filestring = gamefile.filestring.replace(b'w', b'}')
        gamefile.filestring = gamefile.filestring.replace(b'n', b'/')
        gamefile.filestring = gamefile.filestring.replace(b'c', b'$')

        #gamefile.filestring = gamefile.filestring.replace(b'WW', b'>w')
        gamefile.filestring = gamefile.filestring.replace(b'NN', b'>n')
        gamefile.filestring = gamefile.filestring.replace(b'CC', b'>c')


        #gamefile.filestring = gamefile.filestring.replace(b'QQ', b'\x83\x6e')
        #gamefile.filestring = gamefile.filestring.replace(b'RR', b'\x83\x63')
        #gamefile.filestring = gamefile.filestring.replace(b'RW', b'\x81\x63')
        #gamefile.filestring = gamefile.filestring.replace(b'QR', b'\x93\x6e')

        # TODO: The issue is that replacing w, n, c, etc. also replaces it as a part of 2-byte SJIS sequences.
        # Manually doing this (QQ, RR, etc.) above isn't going to work out. Too many things to escape...
        # My idea is to use a regex that finds n, w, and c where the preceding character isn't > or 8x or 9x.



        for t in MsgDump.get_translations(filename):
            for cc in ORIGINAL_CONTROL_CODES:
                t.japanese = t.japanese.replace(cc, ORIGINAL_CONTROL_CODES[cc])

            for cc in CONTROL_CODES:
                #t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                t.english = t.english.replace(cc, CONTROL_CODES[cc])

            t.english = typeset(t.english)
            t.english = shadoff_compress(t.english)

            #j = gamefile.filestring.count(t.japanese)

            #print(t.japanese.decode('shift_jis'))

            #print(t)

            try:
                i = gamefile.filestring.index(t.japanese)
                gamefile.filestring = gamefile.filestring.replace(t.japanese, t.english, 1)
            except ValueError:
                print ("Couldn't find this one:", t.english)


    if filename.endswith('.EXE'):
        for block in FILE_BLOCKS[filename]:
            block = Block(gamefile, block)
            previous_text_offset = block.start
            overflowing = False
            overflow_start = 0
            diff = 0
            not_translated = False
            for t in Dump.get_translations(block):
                if t.english == b'':
                    not_translated = True
                    t.english = t.japanese

                for cc in CONTROL_CODES:
                    t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                    t.english = t.english.replace(cc, CONTROL_CODES[cc])

                t.english = shadoff_compress(t.english)

                loc_in_block = t.location - block.start + diff

                this_diff = len(t.english) - len(t.japanese)

                this_string_end = t.location + diff + len(t.english) + this_diff
                #print(hex(this_string_end), hex(block.stop))
                if this_string_end > block.stop and not overflowing:
                    overflowing = True
                    overflow_start = loc_in_block
                    inter_block_diff = SPARE_BLOCK[filename][0] - (block.start + overflow_start)
                    diff += inter_block_diff
                    print("It's overflowing at %s" % hex(block.start + loc_in_block))

                #print(hex(t.location), t.jp_bytestring)
                i = block.blockstring.index(t.japanese)
                j = block.blockstring.count(t.japanese)

                index = 0
                while index < len(block.blockstring):
                    index = block.blockstring.find(t.japanese, index)
                    if index == -1:
                        break
                    #print('jp bytestring found at', index)
                    index += len(t.japanese) # +2 because len('ll') == 2

                #if j > 1:
                #    print("%s multiples of this string found" % j)
                #print(t.english)
                if loc_in_block == i:
                    print("Warning: String not where expected")

                #block.blockstring = block.blockstring.replace(t.jp_bytestring, t.en_bytestring, 1)
                if not not_translated:
                    block.blockstring = block.blockstring.replace(t.japanese, t.english, 1)
                    reinserted_string_count += 1

                gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                previous_text_offset = t.location

                diff += this_diff


            block_diff = len(block.blockstring) - len(block.original_blockstring)

            print(block_diff)

            #if block_diff > 0 and SPARE_BLOCK[filename]:
            #    overflow_string = block.blockstring[overflow_start:]
                #print(overflow_string)

                #print("Overflow begins at:", hex(block.start + overflow_start))


                #inter_block_diff = SPARE_BLOCK[filename][0] - (block.start + overflow_start)
                #print("Editing pointers between %s and %s" % (hex(block.start+overflow_start), hex(block.stop+diff)))
                #gamefile.edit_pointers_in_range((block.start+overflow_start, block.stop+diff), inter_block_diff)
            #    gamefile.edit(SPARE_BLOCK[filename][0], overflow_string)
            #    block.blockstring = block.blockstring[:overflow_start]

            block_diff = len(block.blockstring) - len(block.original_blockstring)

            if block_diff < 0:
                #print(block.blockstring)
                block.blockstring += (-1)*block_diff*b'\x20'
            block_diff = len(block.blockstring) - len(block.original_blockstring)
            assert block_diff == 0, block_diff

            block.incorporate()

    gamefile.write(path_in_disk='TGL\\OR')
    if filename.endswith('.EXE'):
        percentage = int(floor((reinserted_string_count / STRING_COUNTS[filename] * 100)))
        print(filename, str(percentage), "% complete", "(%s / %s)" % (reinserted_string_count, STRING_COUNTS[filename]))

        total_reinserted_strings += reinserted_string_count
        #print ("(%s / %s)\n" % (self.translated_strings, self.total_strings))

percentage = int(floor((total_reinserted_strings / TOTAL_STRING_COUNT * 100)))
print("Appareden System", "%s" % str(percentage), "%", "complete (%s / %s)" % (total_reinserted_strings, TOTAL_STRING_COUNT))