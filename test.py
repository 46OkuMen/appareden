import os, sys, re
from .rominfo import FILE_BLOCKS, SHADOFF_COMPRESSED_EXES, SRC_DISK, DEST_DISK, CONTROL_CODES, POSTPROCESSING_CONTROL_CODES
from .rominfo import DUMP_XLS_PATH, MSG_XLS_PATH, POINTER_XLS_PATH, POINTER_CONSTANT, MSGS
from .pointer_info import POINTERS_TO_REASSIGN
from .utils import shadoff_compress
from romtools.disk import Gamefile
from romtools.dump import DumpExcel, PointerExcel

FILES_TRANSLATED = ['ORFIELD.EXE', 'ORBTL.EXE', 'ORMAIN.EXE']

Dump = DumpExcel(DUMP_XLS_PATH)
#MsgDump = DumpExcel(MSG_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)

# Make sure all the pointers point to the right text.
# This would be responsible for identifying 90% of errors.

def test_no_duplicate_pointers():
    for f in FILES_TRANSLATED:
        gf = Gamefile(os.path.join('original', f))

        pointers = PtrDump.get_pointers(gf)

        for pointer_list in pointers.values():
            #print(pointer_list)
            if len(pointer_list) > 1:
                print(pointer_list)
                for p in pointer_list[1:]:
                    assert pointer_list[0].location != p.location

# TODO: Test all files' pointers

def pointertest(f):
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

            #t = t.replace(b'~', b' ')

            # Ignore terminal b'\x00' control code, since the result is split there anyway
            if len(t) > 0:
                if t[-1] == 0:
                    t = t[:-1]

            if f in SHADOFF_COMPRESSED_EXES:
                target_english = shadoff_compress(t)
            else:
                target_english = t

            for cc in POSTPROCESSING_CONTROL_CODES[f]:
                target_english = target_english.replace(cc, POSTPROCESSING_CONTROL_CODES[f][cc])

            # Finally, look at the new pointer location in the patched file
            new_bytes = gf.filestring[p.location:p.location+2]
            new_value = int.from_bytes(new_bytes, byteorder='little')
            new_loc = new_value + constant
            p.text_location = new_loc

            result_english = gf.filestring[new_loc:new_loc+80].split(b'\x00')[0]

            if target_english != result_english:
                print("Expected:", hex(trans[0].location), target_english)
                print("Result:  ", hex(new_loc), result_english)
                print()
                pass
            else:
                successes += 1

    print(successes, " / ", total)
    assert successes == total

def test_orfield_pointers():
    pointertest('ORFIELD.EXE')

def test_orbtl_pointers():
    pointertest('ORBTL.EXE')


# Make sure all the blocks contain mutually exclusive, monotonically increasing intervals
def test_block_integrity():
    for f in FILE_BLOCKS:
        last_block = (0, 0)
        for block in FILE_BLOCKS[f]:
            #print(block)
            # Block is from a lower to a higher number
            assert block[0] < block[1]

            # Block is above the last one
            assert block[0] >= last_block[1]
            last_block = block

def test_MSG_end_linebreaks():
    # Make sure that if t.japanese ends in [LN], t.english should also end in [LN].
    failures = 0
    for m in MSGS:
        gf = Gamefile(os.path.join('original', m))
        translations = Dump.get_translations(m, sheet_name='MSG')
        for t in translations:
            if t.japanese.endswith(b'[LN]') and not t.english.endswith(b'[LN]'):
                failures += 1
                print(m, hex(t.location), t.english, "needs an LN")
    assert failures == 0, "Lines need [LN]s: %s" % failures

# TDOO: Can't get this to be useful enough
"""
def test_MSG_double_spaces():
    # Make sure that wherever the string b'  ' appears in a MSG, it is also two spaces in the MSG sheet.

    for m in MSGS:
        gf = Gamefile(os.path.join('original', m))
        # TODO: Agh, this is still slow
        translations = Dump.get_translations(m, sheet_name='MSG')
        for t in translations:
            string_in_file = gf.filestring[t.location:t.location+len(t.japanese)]

            print(t.japanese.count(b'  '))
            print(string_in_file.count(b'  '))

        #locs = [m.start() for m in re.finditer(b' ', gf.filestring)]

        #for loc in locs:
        #    print(gf.filestring[loc-2:loc+4])

    assert False
"""

# Typesetting testing?