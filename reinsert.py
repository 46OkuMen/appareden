"""
    Text reinserter for Appareden.
    Replaces text, adjusts pointers, and implements manual assembly hacks.
"""

import os
from math import floor

from appareden.rominfo import PROGRESS_ROWS, MSGS, SRC_DISK, DEST_DISK, SRC_DIR, DEST_DIR, CONTROL_CODES, B_CONTROL_CODES, POSTPROCESSING_CONTROL_CODES, WAITS
from appareden.rominfo import DUMP_XLS_PATH, POINTER_XLS_PATH, ITEM_NAME_CATEGORIES
from appareden.rominfo import FdRom
from appareden.cd_rominfo import CdRom, CD_SRC_DISK, CD_DEST_DISK, CD_SRC_DIR, CD_DEST_DIR
from appareden.utils import replace_control_codes

from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel

# TODO: Calculate these, don't hardcode them
STRING_COUNTS = {'ORTITLE.EXE': 18,
                 'ORFIELD.EXE': 1326,
                 'ORBTL.EXE': 810,
                 'Dialogue': 5592,
                 'Images': 55,
                 }

TOTAL_STRING_COUNT = sum(list(STRING_COUNTS.values()))

REINSERTED_STRING_COUNTS = {'ORTITLE.EXE': 0,
                            'ORMAIN.EXE': 0,
                            'ORFIELD.EXE': 0,
                            'ORBTL.EXE': 0,
                            'NEKORUN.EXE': 0,
                            'SFIGHT.EXE': 0,
                            'Dialogue': 0,
                            'Images': 0}

Dump = DumpExcel(DUMP_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)

FILES_TO_REINSERT = ['ORFIELD.EXE', 'ORBTL.EXE', 'ORTITLE.EXE']
#FILES_TO_REINSERT = ['ORFIELD.EXE',]

gems_to_reinsert =    ['TMAP_00.gem', 'TMAP_00A.gem', 'TMAP_01A.gem', 'TMAP_01B.gem', 'TMAP_03A.gem', 'TMAP_06A.gem',
                       'TMAP_10B.gem', 'TMAP_11A.gem', 'TMAP_12B.gem', 'TMAP_14A.gem', "TMAP_16B.gem",
                       'TMAP_27A.gem', 'TMAP_29B.gem', 'TMAP_32A.gem',
                       'ORTITLE.gem', 'GENTO.gem', 'BENIMARU.gem', 'HANZOU.gem', 'TAMAMO.gem', 'GOEMON.gem',
                       'HEILEE.gem', 'SHIROU.gem', 'MEIRIN.gem', 'GENNAI.gem', 'OUGI.gem',
                       'GENNAIJ.gem', 'GOEMONJ.gem', 'SHIROUJ.gem', 'HANZOJ.gem']
other_files_to_reinsert = ['SCN12307.COD',]

FILES_TO_REINSERT += MSGS

def results_table():
    """
        Calculate, report, and update the reinsertion progress table.
    """
    """
    | Segment      | %    |  Strings            | 
    | -------------|-----:|:-------------------:|
    | Title        | 100% |    (18 / 18)        |
    | Field        | 100% |  (1194 / 1194)      |
    | Battle       | 100% |   (786 / 786)       |
    | Dialogue     |  83% |  (4653 / 5594)      |
    | Images       |   2% |     (1 / 44?)       |
    | Total        |  85% |  (6662 / 7845)      |
    """

    result =  '| Segment      | %    |  Strings            |\n'
    result += '| -------------|-----:|:-------------------:|\n'

    for filename in PROGRESS_ROWS:
        name_padding = 13 - len(filename)
        percentage = int(floor((REINSERTED_STRING_COUNTS[filename] / STRING_COUNTS[filename] * 100)))
        percentage_padding = 5 - len(str(percentage))
        fraction = "(%s / %s)" % (REINSERTED_STRING_COUNTS[filename], STRING_COUNTS[filename])
        fraction_padding = 20 - len(fraction)
        result += '| %s' % filename + ' '*name_padding
        result += '| %s' % percentage + '%' + ' '*percentage_padding
        result += '| %s' % fraction + ' '*fraction_padding
        result += '|\n'

    # Now handle the totals row

    total_reinserted_strings = sum(list(REINSERTED_STRING_COUNTS.values()))

    total_percentage = str(int(floor((total_reinserted_strings / TOTAL_STRING_COUNT * 100)))) + "%"
    total_fraction = "(%s / %s)" % (total_reinserted_strings, TOTAL_STRING_COUNT)

    result += '| **Total**    |**%s**|  **%s**  |\n\n' % (total_percentage, total_fraction)

    return result

def write_table_to_readme(table):
    """
        Replace the results in the readme file.
    """
    with open('readme.md', 'r+', encoding='utf-8') as f:
        readme = f.read()

        old_table_start = readme.find('| Segment')
        old_table_stop = readme.find('### Requirements')

        readme = readme.replace(readme[old_table_start:old_table_stop], table)
        f.seek(0)
        f.write(readme)

def final_overflow_length(o, translations):
    # The length a string will have when its J strings are replaced by E strings.
    filename = translations[0].gamefile.gamefile.filename

    final_overflow_len = len(o[1])   # THIS GETS USED LATER SO IT NEEDS ACCURACY
    for t in translations:
        jp = t.japanese
        en = t.english
        for cc in CONTROL_CODES:
            jp = jp.replace(cc, CONTROL_CODES[cc])
            en = en.replace(cc, CONTROL_CODES[cc])

        #if filename in SHADOFF_COMPRESSED_EXES:
        #    en = shadoff_compress(en)
        for cc in FdRom.compression_dictionary[filename]:
            en = en.replace(cc, FdRom.compression_dictionary[filename][cc])

        this_diff = len(en) - len(jp)
        final_overflow_len += this_diff
    return final_overflow_len

def is_nametag(s):
    return s.count(b"/") == 1 and s.strip(b"/") == s.split(b'/')[0]

def reinsert(version):

    if version == 'FD':
        OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
        TargetAp = Disk(DEST_DISK)
        src_dir = SRC_DIR
        Rom = FdRom
    elif version == 'CD':
        OriginalAp = Disk(CD_SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
        TargetAp = Disk(CD_DEST_DISK)
        src_dir = CD_SRC_DIR
        Rom = CdRom

    missing_string_count = 0
    for filename in FILES_TO_REINSERT:
        gamefile_path = os.path.join(src_dir, filename)
        if not os.path.isfile(gamefile_path):
            OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path=src_dir)

        if version == 'FD':
            gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)
        elif version == 'CD':
            gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp, pointer_sheet_name='CD ' + filename)

        if filename in Rom.asm_edits:
            for loc, code in Rom.asm_edits[filename]:
                gamefile.edit(loc, code)

        if filename in Rom.pointers_to_reassign:
            reassignments = Rom.pointers_to_reassign[filename]
            for src, dest in reassignments:
                #print(hex(src), hex(dest))
                if src not in gamefile.pointers or dest not in gamefile.pointers:
                    print("Skipping this one: %s, %s" % (hex(src), hex(dest)))
                    continue
                assert src in gamefile.pointers
                assert dest in gamefile.pointers
                diff = dest - src
                assert dest == src + diff
                for p in gamefile.pointers[src]:
                    p.edit(diff)
                gamefile.pointers[dest] += gamefile.pointers[src]
                gamefile.pointers.pop(src)

        if filename.endswith('.MSG'):
            # First, gotta replace all the control codes.
            if filename != 'ENDING.MSG':
                gamefile.filestring = replace_control_codes(gamefile.filestring)

            last_i = 0
            last_nametag = b''

            for t in Dump.get_translations(filename, sheet_name='MSG'):

                if filename != 'ENDING.MSG':
                    for cc in CONTROL_CODES:
                        t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                        t.english = t.english.replace(cc, CONTROL_CODES[cc])

                # Replace overline characters too, which are not control codes
                t.english = t.english.replace(b'[o]', b'o\x7e')
                t.english = t.english.replace(b'[u]', b'u\x7e')
                t.english = t.english.replace(b'[O]', b'O\x7e')
                t.english = t.english.replace(b'[U]', b'U\x7e')

                # All typesetting has been moved to typeset.py, which modifies the excel sheet.

                # Update the last nametag
                if is_nametag(t.english):
                    #print(t.english.strip(b"/"))
                    last_nametag = t.english.strip(b'/')

                # Handle the SPLIT control coddes
                if b'[SPLIT]' in t.english:
                    t.english = t.english.replace(b'[SPLIT]', b'/>k@%s/' % last_nametag, 1)
                    #print(t.english)
                    #input()

                try:
                    i = gamefile.filestring.index(t.japanese)
                    if last_i > i:
                        print("That was before the previous one")
                    last_i = i
                    gamefile.filestring = gamefile.filestring.replace(t.japanese, t.english, 1)


                    if Rom == FdRom:
                        REINSERTED_STRING_COUNTS['Dialogue'] += 1
                except ValueError:
                    print()
                    print("Couldn't find this one:", t.japanese, t.english)
                    missing_string_count += 1
                    for b in t.japanese:
                        print("%s " % hex(b)[2:], end="\t")


        if filename.endswith('.EXE'):
            block_objects = [Block(gamefile, block) for block in Rom.file_blocks[filename]]
            overflow_strings = []
            spares = []

            for block in block_objects:
                print(block)
                previous_text_offset = block.start
                overflowing = False
                overflow_start = 0
                overflowlets = []
                overflowlet_original_locations = []
                diff = 0
                not_translated = False
                last_i = -1
                last_len = 1
                last_string_original_location = 0

                if version == 'FD':
                    translations = Dump.get_translations(block)
                elif version == 'CD':
                    translations = Dump.get_translations(block, use_cd_location=True)
                for t in translations:

                    if version == 'CD':
                        t.location = t.cd_location
                    print(t)

                    if overflowing:
                        # each overflowlet is a location in the blockstring where a new string begins.
                        overflowlets.append(t.location - block.start + diff)
                        overflowlet_original_locations.append(t.location)
                        continue

                    if t.english == b'':
                        not_translated = True
                        t.english = t.japanese

                    for cc in CONTROL_CODES:
                        t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                        t.english = t.english.replace(cc, CONTROL_CODES[cc])

                    t.english = t.english.replace(b'[o]', b'o\x7e')
                    t.english = t.english.replace(b'[u]', b'u\x7e')
                    t.english = t.english.replace(b'[O]', b'O\x7e')
                    t.english = t.english.replace(b'[U]', b'U\x7e')

                    #if filename in SHADOFF_COMPRESSED_EXES:
                    #    t.english = shadoff_compress(t.english)
                    for cc in POSTPROCESSING_CONTROL_CODES[filename]:
                        #if cc == b'[o]' and filename == 'ORBTL.EXE':
                        #    if cc in t.english:
                        #        print(cc, t.english)
                        #        input()
                        t.english = t.english.replace(cc, POSTPROCESSING_CONTROL_CODES[filename][cc])
                        #print(t.english)

                    if t.location != Rom.dictionary_location[filename]:
                        if t.category == "Don't Compress":
                            pass
                        elif filename == 'ORFIELD.EXE' and t.category in ITEM_NAME_CATEGORIES:
                            pass
                        else:
                            for cc in Rom.compression_dictionary[filename]:
                                t.english = t.english.replace(cc, Rom.compression_dictionary[filename][cc])


                    loc_in_block = t.location - block.start + diff

                    this_diff = len(t.english) - len(t.japanese)

                    i = block.blockstring.index(t.japanese)


                    if i <= last_i:
                        after_slice = block.blockstring[last_i+last_len:]
                        i = after_slice.index(t.japanese)
                        assert i != -1
                        i += last_i + last_len

                    this_string_start = block.start + i
                    this_string_end = block.start + i + len(t.english)

                    if this_string_end >= block.stop and not overflowing:
                        overflowing = True
                        overflow_start = i

                        overflowlets.append(t.location - block.start + diff)
                        overflowlet_original_locations.append(t.location)
                        #print("T location was %s" % hex(t.location))

                        # Avoid adjusting pointers
                        continue

                    # Can't do translations if it's overflowing, Those will come later
                    if not not_translated:
                        block.blockstring = block.blockstring[:i] + t.english + block.blockstring[i+len(t.japanese):]
                        if Rom == FdRom:
                            REINSERTED_STRING_COUNTS[filename] += 1

                    gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                    previous_text_offset = t.location
                    last_i = i
                    last_len = len(t.english)

                    diff += this_diff

                    print(t.english)


                block_diff = len(block.blockstring) - len(block.original_blockstring)

                if overflowing:
                    overflow_string = block.blockstring[overflow_start:]
                    #print("Overflow string: %s" % overflow_string, hex(overflow_start + block.start))
                    cursor = 0

                    #assert len(overflowlet_original_locations) == len(overflowlets)
                    #for ool in overflowlet_original_locations:
                    #    print(hex(ool))

                    #for o in overflowlets:
                    #    print(o)

                    #if not overflowlets:
                    #    print("Need to append overflow start?")
                    #    overflowlets.append(overflow_start)

                    overflowlet_original_locations.append(block.stop)

                    for i, o in enumerate(overflowlets):
                        #print(o, overflow_start, o-overflow_start)

                        this_overflowlet_length = overflowlet_original_locations[i+1] - overflowlet_original_locations[i]
                        overflowlet_string = overflow_string[cursor:cursor+this_overflowlet_length]

                        if len(overflowlet_string) < 1:
                            print("That overflowlet is empty")
                            continue
                        #cursor = o-overflow_start
                        cursor += this_overflowlet_length
                        absolute_overflowlet_start = o + block.start
 
                        overflow_strings.append((absolute_overflowlet_start, overflowlet_string, block, overflowlet_original_locations[i]))

                    # Remove the overflow string from the block entirely
                    block.blockstring = block.blockstring[:overflow_start]
                    block_diff = len(block.blockstring) - len(block.original_blockstring)
                    assert block_diff <= 0, (block, block_diff)

                block_diff = len(block.blockstring) - len(block.original_blockstring)

                if block_diff < 0:
                    #block.blockstring += (-1)*block_diff*b'\x20'
                    spares.append((block.stop+block_diff, block.stop, block))

            spares.sort(key=lambda x: x[1] - x[0])  # sort by size
            spares = spares[::-1]  # largest first

            for o in overflow_strings:
                print(o)

            for o in overflow_strings:
                # Catch the spares problems as soon as they arise
                for s in spares:
                    assert s[1] - s[0] >= 0

                print()
                if len(o[1]) < 1:
                    continue
                #print("Length is", len(o[1]))
                #print([s[1]-s[0] for s in spares])
                # o[0] is location, o[1] is the string, o[2] is the parent block, o[3] is the first string's original location
                spare_to_use = spares[0]

                # s[0] is the start, s[1] is the end, s[2] is the parent block
                if version == 'FD':
                    translations = [t for t in Dump.get_translations(o[2]) if t.location == o[3]]
                elif version == 'CD':
                    translations = [t for t in Dump.get_translations(o[2], use_cd_location=True) if t.cd_location == o[3]]

                assert translations[0].japanese in o[1]
                if version == 'CD':
                    assert o[3] == translations[0].cd_location
                else:
                    assert o[3] == translations[0].location

                final_overflow_len = final_overflow_length(o, translations)

                spare_to_use = None
                for s in spares:
                    spare_len = s[1] - s[0]
                    if spare_len > final_overflow_len + 3:
                        spare_to_use = s
                assert spare_to_use is not None
                print(hex(spare_to_use[0]), hex(spare_to_use[1]), spare_to_use[2], " is the snuggest fit, with size", spare_to_use[1]-spare_to_use[0], "for overflow size", final_overflow_len)

                receiving_block = spare_to_use[2]
                receiving_block.blockstring += o[1]
                assert o[1] in receiving_block.blockstring


                # Need to translate all the stuff in the overflow now.
                # Time to repeat tons of code, oops

                not_translated = False
                last_i = receiving_block.start - spare_to_use[0] - 1
                last_len = 1
                previous_text_offset = o[3] - 1
                for t in translations:
                    already_translated = False
                    if t.english == b'':
                        not_translated = True
                        t.english = t.japanese

                    for cc in CONTROL_CODES:
                        t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                        t.english = t.english.replace(cc, CONTROL_CODES[cc])

                    t.english = t.english.replace(b'[o]', b'o\x7e')
                    t.english = t.english.replace(b'[u]', b'u\x7e')
                    t.english = t.english.replace(b'[O]', b'O\x7e')
                    t.english = t.english.replace(b'[U]', b'U\x7e')

                    #if filename in SHADOFF_COMPRESSED_EXES:
                    #    t.english = shadoff_compress(t.english)

                    # Don't dictionary compress item names in ORFIELD.EXE.
                    if filename == 'ORFIELD.EXE' and t.category in ITEM_NAME_CATEGORIES:
                        pass
                    else:
                        for cc in Rom.compression_dictionary[filename]:
                            t.english = t.english.replace(cc, Rom.compression_dictionary[filename][cc])

                    this_diff = len(t.english) - len(t.japanese)
                    final_overflow_len = len(o[1]) + this_diff
                    #print(t.english)

                    try:
                        i = receiving_block.blockstring.index(t.japanese)
                    except ValueError:
                        if t == translations[0]:
                            already_translated = True
                            i = spare_to_use[0] - receiving_block.start
                        else:
                            raise ValueError

                    if not already_translated:
                        if i <= last_i and last_i != spare_to_use[0] - receiving_block.start:
                            after_slice = receiving_block.blockstring[last_i+last_len:]
                            i = after_slice.index(t.japanese)
                            assert i != -1
                            i += last_i + last_len

                        if not not_translated:
                            receiving_block.blockstring = receiving_block.blockstring[:i] + t.english + receiving_block.blockstring[i+len(t.japanese):]
                            REINSERTED_STRING_COUNTS[filename] += 1

                    # Edit the pointers of where the string originally was!
                    # Need to edit the pointers even if the length hasn't changed, too. diff should be initialized to the inter-block jump
                    if t == translations[0]:
                        diff = spare_to_use[0] - o[3]
                        gamefile.edit_pointers_in_range((o[3]-1, o[3]), diff)
                        print(t.english, "should now be at", hex(spare_to_use[0]))
                    else:
                        gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                    previous_text_offset = t.location
                    last_i = i                   # offset in the receiving block
                    last_len = len(t.english)

                    diff += this_diff

                # Update that spare to reflect the new string
                spares[spares.index(spare_to_use)] = (spare_to_use[0]+final_overflow_len, spare_to_use[1], receiving_block)

                # Re-sort the spares
                spares.sort(key=lambda x: x[1] - x[0])  # sort by size
                spares = spares[::-1]  # largest first

                #print(o[2], "overflowed", spare_to_use[2], "is the receiving block")


            # Incorporate after handling spares
            for block in block_objects:
                block_diff = len(block.blockstring) - len(block.original_blockstring)
                assert block_diff <= 0, (block, block_diff)
                if block_diff <= -1:
                    block.blockstring += b'\x00'
                    block_diff += 1
                block.blockstring += (-1)*block_diff*b'\x20'
                block.incorporate()

            percentage = int(floor((REINSERTED_STRING_COUNTS[filename] / STRING_COUNTS[filename] * 100)))
            print(filename, str(percentage), "% complete", "(%s / %s)" % (REINSERTED_STRING_COUNTS[filename], STRING_COUNTS[filename]))

        gamefile.write(path_in_disk='TGL\\OR')

    if missing_string_count > 0:
        print("Strings missing in MSGs: %s" % missing_string_count)

    for g in gems_to_reinsert:
        # This doesn't encode any of them, just inserts what's already there
        print("Inserting", g)
        TargetAp.insert(os.path.join(DEST_DIR, g), path_in_disk='TGL/OR')
        if version == 'FD':
            REINSERTED_STRING_COUNTS['Images'] += 1

    for o in other_files_to_reinsert:
        TargetAp.insert(os.path.join(DEST_DIR, o), path_in_disk='TGL/OR')

if __name__ == '__main__':
    reinsert('FD')
    reinsert('CD')
    table = results_table()
    write_table_to_readme(table)