"""
    Compression dictionary generator for the Appareden English translation.
"""

import os
from collections import OrderedDict
from rominfo import FILE_BLOCKS, SRC_DISK, DEST_DISK, SHADOFF_COMPRESSED_EXES
from rominfo import DUMP_XLS_PATH, POINTER_XLS_PATH
from rominfo import ITEM_NAME_CATEGORIES, DICTIONARY_LOCATION
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel


Dump = DumpExcel(DUMP_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)

DICTIONARY_FILES = ['ORFIELD.EXE', 'ORBTL.EXE']

for filename in DICTIONARY_FILES:

    print('\n', filename, '\n\n')

    gamefile_path = os.path.join('original', filename)
    if not os.path.isfile(gamefile_path):
        OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
    gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)

    block_objects = [Block(gamefile, block) for block in FILE_BLOCKS[filename]]
    words = {}

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
            # Ignore the dictionary slot itself
            if t.location == DICTIONARY_LOCATION[filename]:
                continue 
            if filename == 'ORFIELD.EXE':
                if t.category in ITEM_NAME_CATEGORIES:
                    continue
            for w in t.english.split():
                if len(w) > 2:
                    if w in words:
                        words[w] += 1
                    else:
                        words[w] = 1

    ctrl_codes = OrderedDict()

    # Tertiary sort to get consistent results: alphabetical sort
    words = list((sorted(words.items(), key=lambda x: x[0])))
    # Secondary sort, sort it by the length of the word
    words = list((sorted(words, key=lambda x: len(x[0]))))
    #print(words)
    # Primary sort, sort by frequency
    candidates = list(reversed(sorted(words, key=lambda x: x[1])))
    #print(candidates)
    if filename in SHADOFF_COMPRESSED_EXES:
        dictstring = b'^Restore ^Pill[00]'
        cursor = 14
    else:
        dictstring = b'Restore Pill[00]'
        cursor = 13
    for c in candidates[:100]:
        upper_present, lower_present = False, False
        if c[0].capitalize() in ctrl_codes and filename in SHADOFF_COMPRESSED_EXES:
            continue
        if c[0] != b'[BLANK]' and c[0].strip(b'~') != b'':
            if len(dictstring.replace(b'[ff]', b'0').replace(b'[00]', b'0')) + len(c[0]) + 2 > 3893:
                print("Couldn't fit %s next" % c[0])
                break

            # TODO: Also need to include if a capitalized version is in a substring somewhere.
            # IE battle -> Auto-Battle, for -> Forged

            if filename in SHADOFF_COMPRESSED_EXES:
                if c[0].capitalize() in [w[0] for w in words]:
                    upper_present = True

                if upper_present:
                    dictstring += b'^'
                    ctrl_codes[b'^' + c[0].capitalize()] = (cursor + 0xf000).to_bytes(2, byteorder='big')
                    cursor += 1
                    
                dictstring += c[0].capitalize()
                dictstring += b'[ff]'

                ctrl_codes[c[0].capitalize()] = (cursor + 0xf000).to_bytes(2, byteorder='big')
                cursor += len(c[0])
                cursor += 1

            # If we're not doing Shadoff compression, just ignore caps
            else:
                ctrl_codes[c[0]] = (cursor + 0xf000).to_bytes(2, byteorder='big')
                cursor += len(c[0])
                cursor += 1
                print(cursor)

                dictstring += c[0]
                dictstring += b'[ff]'



    print(dictstring)
    for c in ctrl_codes:
        print("    (%s, %s)," % (c, ctrl_codes[c]))

