import os, sys
from rominfo import FILE_BLOCKS, SHADOFF_COMPRESSED_EXES, SRC_DISK, DEST_DISK, SPARE_BLOCK, CONTROL_CODES, POSTPROCESSING_CONTROL_CODES
from rominfo import DUMP_XLS_PATH, MSG_XLS_PATH, POINTER_XLS_PATH, SYS_DUMP_GOOGLE_SHEET, MSG_DUMP_GOOGLE_SHEET, POINTER_CONSTANT
from pointer_info import POINTERS_TO_REASSIGN
from utils import typeset, shadoff_compress, replace_control_codes
from romtools.disk import Disk, Gamefile, Block, Overflow
from romtools.dump import DumpExcel, PointerExcel

FILES_TRANSLATED = ['ORFIELD.EXE',]

Dump = DumpExcel(DUMP_XLS_PATH)
#MsgDump = DumpExcel(MSG_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)

# Make sure all the pointers point to the right text.
# This would be responsible for identifying 90% of errors.

for f in FILES_TRANSLATED:
    successes = 0
    constant = POINTER_CONSTANT[f]
    gf = Gamefile(os.path.join('patched', f))
    #print(gf)

    translations = Dump.get_translations(gf)
    pointers = PtrDump.get_pointers(gf)
    #print(translations)

    # Get the new locations the pointers point to.
    total = len(pointers)
    for pointer_list in pointers.values():
        for p in pointer_list:
            trans = [t for t in translations if t.location == p.text_location]

            # Some don't have a corresponding translation.
            if not trans:
                total -= 1
                continue

            t = trans[0]

            # Reassigned pointers should have the donor text, so consider that
            for src, dest in POINTERS_TO_REASSIGN[f]:
                if src == t.location:
                    t = [t for t in translations if t.location == dest][0]

            t = t.english

            for cc in CONTROL_CODES:
                t = t.replace(cc, CONTROL_CODES[cc])

            t = t.replace(b'~', b' ')

            # Ignore terminal b'\x00' control code, since the result is split there anyway
            if len(t) > 0:
                if t[-1] == 0:
                    t = t[:-1]

            if f in SHADOFF_COMPRESSED_EXES:
                target_english = shadoff_compress(t)
            else:
                target_english = t

            for cc in POSTPROCESSING_CONTROL_CODES:
                target_english = target_english.replace(cc, POSTPROCESSING_CONTROL_CODES[cc])

            # Finally, look at the new pointer location in the patched file
            new_bytes = gf.filestring[p.location:p.location+2]
            new_value = int.from_bytes(new_bytes, byteorder='little')
            new_loc = new_value + constant
            p.text_location = new_loc

            result_english = gf.filestring[new_loc:new_loc+80].split(b'\x00')[0]

            if target_english != result_english:
                print(hex(trans[0].location), target_english)
                print(hex(new_loc), result_english)
                print()
                pass
            else:
                successes += 1

            #if b'WhatWillYouDo?' in target_english:
            #    sys.exit()

    print(successes, " / ", total)
    # TODO: total is less than the successes currently. Still 12 left in ORFIELD

# Make sure all the blocks contain mutually exclusive, monotonically increasing intervals
for f in FILE_BLOCKS:
    last_block = (0, 0)
    for block in FILE_BLOCKS[f]:
        #print(block)
        # Block is from a lower to a higher number
        assert block[0] < block[1]

        # Block is above the last one
        assert block[0] >= last_block[1]
        last_block = block