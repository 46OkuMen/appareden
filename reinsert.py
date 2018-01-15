"""
    Text reinserter for Appareden.
    Replaces text, adjusts pointers, and implements manual assembly hacks.
"""

import os
from math import floor
from rominfo import MSGS, FILE_BLOCKS, SHADOFF_COMPRESSED_EXES, SRC_DISK, DEST_DISK, SPARE_BLOCK, CONTROL_CODES, B_CONTROL_CODES, WAITS, POSTPROCESSING_CONTROL_CODES
from rominfo import DUMP_XLS_PATH, MSG_XLS_PATH, POINTER_XLS_PATH, SYS_DUMP_GOOGLE_SHEET, MSG_DUMP_GOOGLE_SHEET
from pointer_info import POINTERS_TO_REASSIGN
import asm
from utils import typeset, shadoff_compress, replace_control_codes
from romtools.disk import Disk, Gamefile, Block, Overflow
from romtools.dump import DumpExcel, PointerExcel, update_google_sheets

#update_google_sheets(DUMP_XLS_PATH, SYS_DUMP_GOOGLE_SHEET)
#update_google_sheets(MSG_XLS_PATH, MSG_DUMP_GOOGLE_SHEET)
# The current method won't work for the MSG dump; too many requests.
# Need to condense it into one sheet after draft is done.

# TODO: Calculate these, don't hardcode them
STRING_COUNTS = {'ORTITLE.EXE': 25,
                 'ORMAIN.EXE': 204,
                 'ORFIELD.EXE': 1193,
                 'ORBTL.EXE': 785,
                 'NEKORUN.EXE': 3,
                 'SFIGHT.EXE': 15,
                 'all_msgs': 5592,
                 }

TOTAL_STRING_COUNT = sum(list(STRING_COUNTS.values()))

Dump = DumpExcel(DUMP_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)


#FILES_TO_REINSERT = ['ORFIELD.EXE', ]

FILES_TO_REINSERT = ['ORFIELD.EXE', 'ORBTL.EXE', 'ORTITLE.EXE']

#                      Gento,  Benimaru, Goemon, WeaponShop, ArmorShop,    Samurai, Hanzou, Innkeeper, ItemShop,
portrait_characters = ['幻斗', 'ベニマル', 'ゴエモン', '宿屋の主人', '防具屋の主人', '武士', 'ハンゾウ', '宿屋の主人', '道具屋の娘',
                      # Master, Koro Elder, WeaponsGeezer, Elder, AntiquesShop, Shikai, Tamamo, Nobunaga, Old Man,
                       'マスター', 'コロ長老',  '武器屋のオヤジ', '長老', '骨董品屋の主人', '四界王', 'タマモ', 'ノブナガ', '老人',
                       # Mitsukuni, Izunokami, O-Toki, Gennai, Benkei, Ginpei, Shirou, Meiling,
                       'ミツクニ', 'イズノカミ',      'お時', '源内', 'ベンケイ' 'ギンペー', 'シロウ',  'メイリン',
                       ]

#HIGHEST_SCN = 1
HIGHEST_SCN = 11001

#msg_files = [f for f in os.listdir(os.path.join('original', 'OR')) if f.endswith('MSG') and not f.startswith('ENDING')]
msgs_to_reinsert = [f for f in MSGS if int(f.lstrip('SCN').rstrip('.MSG')) <= HIGHEST_SCN]
"""
valid_msgs = []
# TODO: Cache the list of real ones
for m in msgs_to_reinsert:
    try:
        sheet = Dump.get_translations(m, sheet_name='MSG')
        valid_msgs.append(m)
    except KeyError:
        continue
print(valid_msgs)
"""

FILES_TO_REINSERT += msgs_to_reinsert

total_reinserted_strings = 0

for filename in FILES_TO_REINSERT:
    gamefile_path = os.path.join('original', filename)
    if not os.path.isfile(gamefile_path):
        OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
    gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)

    reinserted_string_count = 0

    if filename == 'ORFIELD.EXE':

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

        # Apply ORFIELD asm hacks
        asm_cursor = 0
        for code in asm.ORFIELD_CODE:
            gamefile.edit(0x8c0b+asm_cursor, code)
            asm_cursor += len(code)

        # Wait, what is this again?
        gamefile.edit(0x8c4d, b'\x90\x90\x90\x90\x90\x90\x90\xb4\x09')

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

        for t in Dump.get_translations(filename, sheet_name='MSG'):

            #if b'Hakodate' in t.english:
            #    print(t.english)

            for cc in CONTROL_CODES:
                t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                t.english = t.english.replace(cc, CONTROL_CODES[cc])

            # If any portraited characters show up in this line, 
            # this line (nametag) and next line (entire dialogue box) are narrower
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

        # temporarily replace all the waits with nothing
        #for w in WAITS:
        #    gamefile.filestring = gamefile.filestring.replace(w, b'')


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
            last_string_original_location = 0
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
                #print(t.english)


                loc_in_block = t.location - block.start + diff

                this_diff = len(t.english) - len(t.japanese)

                i = block.blockstring.index(t.japanese)

                #print(hex(t.location), t.english)

                if i <= last_i:
                    after_slice = block.blockstring[last_i+last_len:]
                    #print("Looking for", t.japanese)
                    i = after_slice.index(t.japanese)
                    assert i != -1
                    i += last_i + last_len

                this_string_start = block.start + i
                this_string_end = block.start + i + len(t.english)
                #print("String starts at %s and ends at %s" % (hex(this_string_start), hex(this_string_end)))

                if this_string_end >= block.stop and not overflowing:
                    overflowing = True
                    overflow_start = i
                    overflow_original_location = t.location
                    print("It's overflowing starting with string %s" % t)
                    #print("Absolute location:", hex(block.start + i))
                    #print("Block is", block)
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

            #print(block_diff)

            if overflowing:
                overflow_string = block.blockstring[overflow_start:]
                #print(overflow_string)
                #print("Overflow begins at:", hex(block.start + overflow_start))
                absolute_overflow_start = overflow_start + block.start
                overflow_strings.append((absolute_overflow_start, overflow_string, block, overflow_original_location))

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

        for s in spares:
            print("spare:", hex(s[0]), hex(s[1]), s[1] - s[0], "belongs to", s[2])

        print("Everything that's overflowing:")
        for o in overflow_strings:
            translations = [t for t in Dump.get_translations(o[2]) if o[3] <= t.location]
            for t in translations:
                print(t)

        for o in overflow_strings:
            # o[0] is location, o[1] is the string, o[2] is the parent block, o[3] is the first string's original location
            #print("overflows:", hex(o[0]), o[1], "size:", len(o[1]))
            spare_to_use = spares[0]

            # s[0] is the start, s[1] is the end, s[2] is the parent block


            translations = [t for t in Dump.get_translations(o[2]) if o[3] <= t.location]

            overflow_len_diff = sum([len(t.english) - len(t.japanese) for t in translations])
            final_overflow_len = len(o[1]) + overflow_len_diff
            for s in spares:
                spare_len = s[1] - s[0]
                if spare_len >= final_overflow_len:
                    spare_to_use = s
            print(hex(spare_to_use[0]), hex(spare_to_use[1]), spare_to_use[2], " is the snuggest fit, with size", spare_to_use[1]-spare_to_use[0])

            receiving_block = spare_to_use[2]
            receiving_block.blockstring += o[1]

            # TODO: Move each translation into a spare individually, so large overflows can be distributed

            # Need to translate all the stuff in the overflow now.
            # Time to repeat tons of code, oops

            #previous_text_offset = spare_to_use[0]-1
            #print("o3:", hex(o[3]))
            #print("s0:", hex(spare_to_use[0]))
            #diff = spare_to_use[0] - o[3]
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
                for cc in POSTPROCESSING_CONTROL_CODES:
                    t.english = t.english.replace(cc, POSTPROCESSING_CONTROL_CODES[cc])

                this_diff = len(t.english) - len(t.japanese)

                print(hex(t.location), t.english)

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
                        reinserted_string_count += 1

                # Edit the pointers of where the string originally was!
                # Need to edit the pointers even if the length hasn't changed, too. diff should be initialized to the inter-block jump
                #for p in gamefile.pointers:
                #    print(hex(p.text_location))
                if t == translations[0]:
                    diff = spare_to_use[0] - o[3]
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

            print(o[2], "overflowed", spare_to_use[2], "is the receiving block")

        for s in spares:
            #print("spare:", s, s[1] - s[0])
            assert s[1] - s[0] >= 0


        # Incorporate after handling spares
        for block in block_objects:
            block_diff = len(block.blockstring) - len(block.original_blockstring)
            assert block_diff <= 0, (block, block_diff)
            if block_diff <= -1:
                block.blockstring += b'\x00'
                block_diff += 1
            block.blockstring += (-1)*block_diff*b'\x20'
            block.incorporate()

        percentage = int(floor((reinserted_string_count / STRING_COUNTS[filename] * 100)))
        print(filename, str(percentage), "% complete", "(%s / %s)" % (reinserted_string_count, STRING_COUNTS[filename]))

    total_reinserted_strings += reinserted_string_count
    print("Total reinserted strings is", total_reinserted_strings)

    gamefile.write(path_in_disk='TGL\\OR')

percentage = int(floor((total_reinserted_strings / TOTAL_STRING_COUNT * 100)))
print("Appareden", "%s" % str(percentage), "%", "complete (%s / %s)" % (total_reinserted_strings, TOTAL_STRING_COUNT))