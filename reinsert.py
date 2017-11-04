"""
    Text reinserter for Appareden.
    Replaces text, adjusts pointers, and implements manual assembly hacks.
"""

import os
from math import floor
from rominfo import FILE_BLOCKS, SHADOFF_COMPRESSED_EXES, SRC_DISK, DEST_DISK, SPARE_BLOCK, CONTROL_CODES, POSTPROCESSING_CONTROL_CODES
from rominfo import DUMP_XLS_PATH, MSG_XLS_PATH, POINTER_XLS_PATH, SYS_DUMP_GOOGLE_SHEET, MSG_DUMP_GOOGLE_SHEET
from pointer_info import POINTERS_TO_REASSIGN
from asm import SPACECODE_ASM, OVERLINE_ASM, SHADOFF_ASM
from utils import typeset, shadoff_compress, replace_control_codes
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel, update_google_sheets

#update_google_sheets(DUMP_XLS_PATH, SYS_DUMP_GOOGLE_SHEET)
#update_google_sheets(MSG_XLS_PATH, MSG_DUMP_GOOGLE_SHEET)
# The current method won't work for the MSG dump; too many requests.
# Need to condense it into one sheet after draft is done.

# TODO: Calculate these, don't hardcode them
STRING_COUNTS = {'ORTITLE.EXE': 18,
                 'ORMAIN.EXE': 202,
                 'ORFIELD.EXE': 1169,
                 'ORBTL.EXE': 780,
                 'NEKORUN.EXE': 4,
                 'SFIGHT.EXE': 15,
                 'all_msgs': 13078,
                 }

TOTAL_STRING_COUNT = sum(list(STRING_COUNTS.values()))

Dump = DumpExcel(DUMP_XLS_PATH)
MsgDump = DumpExcel(MSG_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)


FILES_TO_REINSERT = ['ORFIELD.EXE', ]

#FILES_TO_REINSERT = ['ORFIELD.EXE', 'ORBTL.EXE', 'ORTITLE.EXE']

#                      Gento,  Benimaru, Goemon, WeaponShop, ArmorShop,    Samurai, Hanzou, Innkeeper, ItemShop,
portrait_characters = ['幻斗', 'ベニマル', 'ゴエモン', '宿屋の主人', '防具屋の主人', '武士', 'ハンゾウ', '宿屋の主人', '道具屋の娘',
                      # Master,
                       'マスター',]

HIGHEST_SCN = 2400
# Problems in 5103, 6100 due to fullwidth text from Haley

msg_files = [f for f in os.listdir(os.path.join('original', 'OR')) if f.endswith('MSG') and not f.startswith('ENDING')]
print(msg_files)
msgs_to_reinsert = [f for f in msg_files if int(f.lstrip('SCN').rstrip('.MSG')) <= HIGHEST_SCN]
valid_msgs = []
for m in msgs_to_reinsert:
    print(m)
    try:
        sheet = MsgDump.get_translations(m)
        valid_msgs.append(m)
    except KeyError:
        continue

FILES_TO_REINSERT += valid_msgs

total_reinserted_strings = 0

for filename in FILES_TO_REINSERT:
    gamefile_path = os.path.join('original', filename)
    if not os.path.isfile(gamefile_path):
        OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
    gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)

    reinserted_string_count = 0

    if filename == 'ORFIELD.EXE':
        # TODO: Spin this off into asm.py.
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

        # Expand space for status ailments in menu
        # ac = limit of 6, and we want 12 for Petrified
        gamefile.edit(0x1ab14, b'\xb2')

    if filename in POINTERS_TO_REASSIGN:
        reassignments = POINTERS_TO_REASSIGN[filename]
        for src, dest in reassignments:
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

        portrait_window_counter = 0

        for t in MsgDump.get_translations(filename):

            for cc in CONTROL_CODES:
                t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                t.english = t.english.replace(cc, CONTROL_CODES[cc])

            # If any portraited characters show up in this line, 
            # this line and next line are narrower
            for name in portrait_characters:
                if name.encode('shift-jis') in t.japanese:
                    portrait_window_counter = 2
                    break

            if portrait_window_counter > 0:
                t.english = typeset(t.english, 37)
            else:
                t.english = typeset(t.english, 57)
            t.english = shadoff_compress(t.english)

            try:
                i = gamefile.filestring.index(t.japanese)
                gamefile.filestring = gamefile.filestring.replace(t.japanese, t.english, 1)
                reinserted_string_count += 1
            except ValueError:
                print("Couldn't find this one:", t.japanese, t.english)

            if portrait_window_counter > 0:
                portrait_window_counter -= 1


    if filename.endswith('.EXE'):
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
            for t in Dump.get_translations(block):

                if overflowing:
                    break

                if t.english == b'':
                    not_translated = True
                    t.english = t.japanese

                for cc in CONTROL_CODES:
                    t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                    t.english = t.english.replace(cc, CONTROL_CODES[cc])

                if filename in SHADOFF_COMPRESSED_EXES:
                    t.english = shadoff_compress(t.english)
                for cc in POSTPROCESSING_CONTROL_CODES:
                    t.english = t.english.replace(cc, POSTPROCESSING_CONTROL_CODES[cc])

                loc_in_block = t.location - block.start + diff

                this_diff = len(t.english) - len(t.japanese)

                i = block.blockstring.index(t.japanese)

                print(hex(t.location), t.english)

                if i <= last_i:
                    after_slice = block.blockstring[last_i+last_len:]
                    print("Looking for", t.japanese)
                    i = after_slice.index(t.japanese)
                    assert i != -1
                    i += last_i + last_len
                print("text at", i)

                this_string_end = t.location + diff + len(t.english) + this_diff

                if this_string_end > block.stop and not overflowing:
                    overflowing = True
                    # Need to get the location of where it began to overflow
                    #overflow_start = t.location - block.start + diff + this_diff
                    # overflow_start = i         # was too conservative, sometimes left a block too long
                    overflow_start = last_i
                    overflow_original_location = t.location
                    print("It's overflowing at %s" % hex(block.start + loc_in_block))
                    break


                # Can't do translations if it's overflowing, Those will come later
                if not not_translated:
                    block.blockstring = block.blockstring[:i] + t.english + block.blockstring[i+len(t.japanese):]
                    reinserted_string_count += 1

                gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                previous_text_offset = t.location
                last_i = i
                last_len = len(t.english)

                diff += this_diff


            block_diff = len(block.blockstring) - len(block.original_blockstring)

            print(block_diff)

            if overflowing:
                overflow_string = block.blockstring[overflow_start:]
                print(overflow_string)
                print("Overflow begins at:", hex(block.start + overflow_start))
                absolute_overflow_start = overflow_start + block.start
                overflow_strings.append((absolute_overflow_start, overflow_string, block, overflow_original_location))

                # Remove the overflow string from the block entirely
                block.blockstring = block.blockstring[:overflow_start]
                block_diff = len(block.blockstring) - len(block.original_blockstring)
                assert block_diff <= 0, (block, block_diff)

            block_diff = len(block.blockstring) - len(block.original_blockstring)

            if block_diff < 0:
                #block.blockstring += (-1)*block_diff*b'\x20'
                spares.append((block.stop, block.stop-block_diff, block))

        spares.sort(key=lambda x: x[1] - x[0])  # sort by size
        spares = spares[::-1]  # largest first

        for s in spares:
            print("spare:", s, s[1] - s[0])

        for o in overflow_strings:
            # o[0] is location, o[1] is the string, o[2] is the parent block, o[3] is the first string's original location
            print("overflows:", hex(o[0]), o[1], "size:", len(o[1]))
            spare_to_use = spares[0]

            # s[0] is the start, s[1] is the end, s[2] is the parent block

            #print(hex(o[0]), hex(o[0]+len(o[1])))
            translations = [t for t in Dump.get_translations(o[2]) if o[3] <= t.location]
            #print(translations)
            overflow_len_diff = sum([len(t.english) - len(t.japanese) for t in translations])
            #print(overflow_len_diff)
            final_overflow_len = len(o[1]) + overflow_len_diff
            for s in spares:
                spare_len = s[1] - s[0]
                if spare_len >= final_overflow_len:
                    spare_to_use = s
            print(spare_to_use, " is the snuggest fit, with size", spare_to_use[1]-spare_to_use[0])

            receiving_block = spare_to_use[2]
            receiving_block.blockstring += o[1]

            # TODO: Move each translation into a spare individually, so large overflows can be distributed

            # Need to translate all the stuff in the overflow now.
            # Time to repeat tons of code, oops

            #previous_text_offset = spare_to_use[0]-1
            print("o3:", hex(o[3]))
            print("s0:", hex(spare_to_use[0]))
            #diff = spare_to_use[0] - o[3]
            not_translated = False
            last_i = receiving_block.start - spare_to_use[0] - 1
            last_len = 1
            previous_text_offset = o[3] - 1
            for t in translations:
                if t.english == b'':
                    not_translated = True
                    t.english = t.japanese

                for cc in CONTROL_CODES:
                    t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                    t.english = t.english.replace(cc, CONTROL_CODES[cc])

                if filename in SHADOFF_COMPRESSED_EXES:
                    t.english = shadoff_compress(t.english)
                for cc in POSTPROCESSING_CONTROL_CODES:
                    t.english = t.english.replace(cc, POSTPROCESSING_CONTROL_CODES[cc])

                this_diff = len(t.english) - len(t.japanese)

                i = receiving_block.blockstring.index(t.japanese)

                print(hex(t.location), t.english)

                if i <= last_i:
                    after_slice = receiving_block.blockstring[last_i+last_len:]
                    i = after_slice.index(t.japanese)
                    assert i != -1
                    i += last_i + last_len

                if not not_translated:
                    receiving_block.blockstring = receiving_block.blockstring[:i] + t.english + receiving_block.blockstring[i+len(t.japanese):]
                    reinserted_string_count += 1

                # Edit the pointers of where the string originally was!
                # Need to edit the pointers even if the length hasn't changed, too. diff should be initialized to the inter-block jump
                #for p in gamefile.pointers:
                #    print(hex(p.text_location))
                if t == translations[0]:
                    print(gamefile.pointers[o[3]])
                    #gamefile.pointers[o[3]][0].edit(diff)
                    diff = (receiving_block.start + i) - o[3]
                    print("Here's the diff:", diff)
                    gamefile.edit_pointers_in_range((o[3]-1, o[3]), diff)
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

            print(o[2], "overflowed", s[2], "is the receiving block")

        for s in spares:
            print("spare:", s, s[1] - s[0])


        # Incorporate after handling spares
        for block in block_objects:
            block_diff = len(block.blockstring) - len(block.original_blockstring)
            assert block_diff <= 0, (block, block_diff)
            block.blockstring += (-1)*block_diff*b'\x20'
            block.incorporate()

        percentage = int(floor((reinserted_string_count / STRING_COUNTS[filename] * 100)))
        print(filename, str(percentage), "% complete", "(%s / %s)" % (reinserted_string_count, STRING_COUNTS[filename]))

    total_reinserted_strings += reinserted_string_count
    print("Total reinserted strings is", total_reinserted_strings)
        #print ("(%s / %s)\n" % (self.translated_strings, self.total_strings))

    gamefile.write(path_in_disk='TGL\\OR')

percentage = int(floor((total_reinserted_strings / TOTAL_STRING_COUNT * 100)))
print("Appareden", "%s" % str(percentage), "%", "complete (%s / %s)" % (total_reinserted_strings, TOTAL_STRING_COUNT))