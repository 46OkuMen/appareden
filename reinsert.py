"""
    Text reinserter for Appareden.
    Replaces text, adjusts pointers, and implements manual assembly hacks.
"""

import os
import re
from math import floor

from appareden import asm
from appareden.rominfo import PROGRESS_ROWS, MSGS, FILE_BLOCKS, SHADOFF_COMPRESSED_EXES, SRC_DISK, DEST_DISK, CONTROL_CODES, B_CONTROL_CODES, WAITS, POSTPROCESSING_CONTROL_CODES
from appareden.rominfo import DUMP_XLS_PATH, POINTER_XLS_PATH, DICT_LOCATION
from appareden.pointer_info import POINTERS_TO_REASSIGN
from appareden.utils import shadoff_compress, replace_control_codes

from romtools.disk import Disk, Gamefile, Block, Overflow
from romtools.dump import DumpExcel, PointerExcel

#update_google_sheets(DUMP_XLS_PATH, SYS_DUMP_GOOGLE_SHEET)
#update_google_sheets(MSG_XLS_PATH, MSG_DUMP_GOOGLE_SHEET)
# The current method won't work for the MSG dump; too many requests.
# Need to condense it into one sheet after draft is done.

# TODO: Calculate these, don't hardcode them
STRING_COUNTS = {'ORTITLE.EXE': 25,
                 'ORMAIN.EXE': 204,
                 'ORFIELD.EXE': 1205,
                 'ORBTL.EXE': 785,
                 'NEKORUN.EXE': 3,
                 'SFIGHT.EXE': 15,
                 'Dialogue': 5592,
                 'Images': 37,
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
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)


#FILES_TO_REINSERT = ['ORFIELD.EXE', ]

FILES_TO_REINSERT = ['ORFIELD.EXE', 'ORBTL.EXE', 'ORTITLE.EXE']

gems_to_reinsert = ['ORTITLE.GEM']

FILES_TO_REINSERT += MSGS

def results_table():
    """
        Calculate, report, and update the reinsertion progress table.
    """
    """
    | Segment      | %    |  Strings            | 
    | -------------|-----:|:-------------------:|
    | Title        | 100% |    (18 / 18)        |
    | Main         |   0% |     (0 / 202)       |
    | Field        | 100% |  (1194 / 1194)      |
    | Battle       | 100% |   (786 / 786)       |
    | Cat Minigame |   0% |     (0 / 7)         |
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

        if filename in SHADOFF_COMPRESSED_EXES:
            en = shadoff_compress(en)
        for cc in POSTPROCESSING_CONTROL_CODES[filename]:
            en = en.replace(cc, POSTPROCESSING_CONTROL_CODES[filename][cc])

        this_diff = len(en) - len(jp)
        final_overflow_len += this_diff
    return final_overflow_len

def reinsert():
    missing_string_count = 0
    for filename in FILES_TO_REINSERT:
        gamefile_path = os.path.join('original', filename)
        if not os.path.isfile(gamefile_path):
            OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
        gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)

        if filename == 'ORFIELD.EXE':

            # Apply ORFIELD asm hacks

            # TODO: Spin this off into asm.py.
            gamefile.edit(0x151b7, B_CONTROL_CODES[b'w'])         # w = "{"
            gamefile.edit(0x15b0f, B_CONTROL_CODES[b'w'])         # w = "{"
            gamefile.edit(0x15b99, B_CONTROL_CODES[b'w'])         # w = "{"

            gamefile.edit(0x15519, B_CONTROL_CODES[b'n'])         # n = "/"
            gamefile.edit(0x15528, B_CONTROL_CODES[b'n'])         # n = "/"
            gamefile.edit(0x155df, B_CONTROL_CODES[b'n'])         # n = "/"
            gamefile.edit(0x155ee, B_CONTROL_CODES[b'n'])         # n = "/"
            gamefile.edit(0x15b1d, B_CONTROL_CODES[b'n'])         # n = "/"
            gamefile.edit(0x15b5f, B_CONTROL_CODES[b'n'])         # n = "/"

            gamefile.edit(0x15b16, B_CONTROL_CODES[b'c'])         # c = "$"
            gamefile.edit(0x15b6c, B_CONTROL_CODES[b'c'])         # c = "$"
            gamefile.edit(0x2551b, B_CONTROL_CODES[b'c'])         # c = "$"

            # Longer, more complex text handling ASM
            asm_cursor = 0

            for code in asm.ORFIELD_CODE:
                gamefile.edit(0x8c0b+asm_cursor, code)
                asm_cursor += len(code)
                print(hex(asm_cursor), "of ASM written")

            # Expand space for status ailments in menu
            # ac = limit of 6, and we want 12 for Petrified
            gamefile.edit(0x1ab14, b'\xb2')

        elif filename == 'ORBTL.EXE':
            # Text handling ASM
            asm_cursor = 0
            for code in asm.ORBTL_CODE:
                gamefile.edit(0x3647+asm_cursor, code)
                asm_cursor += len(code)


        if filename in POINTERS_TO_REASSIGN:
            reassignments = POINTERS_TO_REASSIGN[filename]
            for src, dest in reassignments:
                #print(hex(src), hex(dest))
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
            gamefile.filestring = replace_control_codes(gamefile.filestring)

            last_i = 0

            for t in Dump.get_translations(filename, sheet_name='MSG'):

                for cc in CONTROL_CODES:
                    t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                    t.english = t.english.replace(cc, CONTROL_CODES[cc])

                # All typesetting has been moved to typeset.py, which modifies the excel sheet.

                if filename != 'ENDING.MSG':
                    t.english = shadoff_compress(t.english)

                try:
                    i = gamefile.filestring.index(t.japanese)
                    if last_i > i:
                        print("That was before the previous one")
                    last_i = i
                    gamefile.filestring = gamefile.filestring.replace(t.japanese, t.english, 1)
                    REINSERTED_STRING_COUNTS['Dialogue'] += 1
                except ValueError:
                    print()
                    print("Couldn't find this one:", t.japanese, t.english)
                    missing_string_count += 1
                    for b in t.japanese:
                        print("%s " % hex(b)[2:], end="\t")


        if filename.endswith('.EXE'):
            block_objects = [Block(gamefile, block) for block in FILE_BLOCKS[filename]]
            overflow_strings = []
            spares = []

            for block in block_objects:
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
                for t in Dump.get_translations(block):

                    if t.location == 0x252f3:
                        print("It's happening")

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

                    if filename in SHADOFF_COMPRESSED_EXES:
                        t.english = shadoff_compress(t.english)
                    if t.location !=  DICT_LOCATION[filename]:
                        for cc in POSTPROCESSING_CONTROL_CODES[filename]:
                            t.english = t.english.replace(cc, POSTPROCESSING_CONTROL_CODES[filename][cc])


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
                        #overflow_original_location = t.location
                        print("It's overflowing starting with string %s" % t)

                        overflowlets.append(t.location - block.start + diff)
                        overflowlet_original_locations.append(t.location)
                        print("T location was %s" % hex(t.location))

                        # Avoid adjusting pointers
                        continue

                    # Can't do translations if it's overflowing, Those will come later
                    if not not_translated:
                        block.blockstring = block.blockstring[:i] + t.english + block.blockstring[i+len(t.japanese):]
                        REINSERTED_STRING_COUNTS[filename] += 1

                    gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                    previous_text_offset = t.location
                    last_i = i
                    last_len = len(t.english)

                    diff += this_diff


                block_diff = len(block.blockstring) - len(block.original_blockstring)

                if overflowing:
                    overflow_string = block.blockstring[overflow_start:]
                    print("Overflow string: %s" % overflow_string, hex(overflow_start + block.start))
                    cursor = 0

                    #assert len(overflowlet_original_locations) == len(overflowlets)
                    #for ool in overflowlet_original_locations:
                    #    print(hex(ool))

                    for o in overflowlets:
                        print(o)

                    #if not overflowlets:
                    #    print("Need to append overflow start?")
                    #    overflowlets.append(overflow_start)

                    overflowlet_original_locations.append(block.stop)

                    for i, o in enumerate(overflowlets):
                        print(o, overflow_start, o-overflow_start)

                        this_overflowlet_length = overflowlet_original_locations[i+1] - overflowlet_original_locations[i]
                        overflowlet_string = overflow_string[cursor:cursor+this_overflowlet_length]
                        print(overflowlet_string)
                        
                        #overflowlet_string = overflow_string[cursor:o-overflow_start]
                        if len(overflowlet_string) < 1:
                            print("That overflowlet is empty")
                            continue
                        #cursor = o-overflow_start
                        cursor += this_overflowlet_length
                        absolute_overflowlet_start = o + block.start
                        #print("Here's an overflow string that was part of that:")
                        #print((absolute_overflowlet_start, overflowlet_string, block, hex(overflowlet_original_locations[i])))
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
                translations = [t for t in Dump.get_translations(o[2]) if t.location == o[3]]

                assert translations[0].japanese in o[1]
                assert o[3] == translations[0].location

                final_overflow_len = final_overflow_length(o, translations)

                spare_to_use = None
                for s in spares:
                    spare_len = s[1] - s[0]
                    if spare_len > final_overflow_len:
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

                    if filename in SHADOFF_COMPRESSED_EXES:
                        t.english = shadoff_compress(t.english)
                    for cc in POSTPROCESSING_CONTROL_CODES[filename]:
                        t.english = t.english.replace(cc, POSTPROCESSING_CONTROL_CODES[filename][cc])

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

    print("Strings missing in MSGs: %s" % missing_string_count)

    for g in gems_to_reinsert:
        # This doesn't encode any of them, just inserts what's already there
        TargetAp.insert(os.path.join('patched', g), path_in_disk='TGL/OR')
        REINSERTED_STRING_COUNTS['Images'] += 1

if __name__ == '__main__':
    reinsert()
    table = results_table()
    write_table_to_readme(table)