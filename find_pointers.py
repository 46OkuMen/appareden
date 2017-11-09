import os
import re
from rominfo import FILES, FILE_BLOCKS, POINTER_CONSTANT, SRC_DISK, POINTER_TABLES
from pointer_info import POINTER_DISAMBIGUATION
from romtools.dump import BorlandPointer, DumpExcel, PointerExcel
from romtools.disk import Gamefile, Block, Disk

strings_to_skip = ['ポインタが使われました', '      体', '       心', 'ＥＭＳ']
garbage_pointer_values = [0x0, 0xff, 0x8, 0x4, 0x100, 0x200, 0x400, 0x800, 0xd00, 0x900, 0x1, 0x2, 0x3]

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

DUMP_XLS_PATH = 'appareden_sys_dump.xlsx'
Dump = DumpExcel(DUMP_XLS_PATH)

MSG_DUMP_XLSX_PATH = 'appareden_msg_dump.xlsx'
MsgDump = DumpExcel(MSG_DUMP_XLSX_PATH)


OriginalAp = Disk(SRC_DISK, dump_excel=Dump)
#files_to_search = ['ORTITLE.EXE', 'ORMAIN.EXE', 'ORFIELD.EXE', 'ORBTL.EXE', 'SFIGHT.EXE']
files_to_search = ['ORFIELD.EXE', 'ORBTL.EXE', 'ORTITLE.EXE', 'ORMAIN.EXE']

# NEKORUN.EXE might not have pointers. Edit it manually? Mostly error messages anyway.
# ENDING.EXE is only error messages...?

problem_count = 0

try:
    os.remove('appareden_pointer_dump.xlsx')
except WindowsError:
    pass
PtrXl = PointerExcel('appareden_pointer_dump.xlsx')

for f in files_to_search:

    found_text_locations = []
    print(f)
    GF = Gamefile(os.path.join('original', f), disk=OriginalAp)
    previous_pointer_locations = []
    try:
        worksheet = PtrXl.add_worksheet(GF.filename)
    except AttributeError:
        _ = input("You have the sheet open, close it and hit Enter")
        worksheet = PtrXl.add_worksheet(GF.filename)
    row = 1
    #for block in FILE_BLOCKS[f]:
    #    blk = Block(GF, block)
    #    #last_pointer_location = POINTER_CONSTANT[f]
    #    pointer_location = POINTER_CONSTANT[f]

    for table in POINTER_TABLES[f]:
        print(hex(table[0]), hex(table[1]))
        stride = table[2]
        table_bytes = GF.filestring[table[0]:table[1]]
        pointer_location = table[0]
        #print(table_bytes)
        while table_bytes:
            possible_value = int.from_bytes(table_bytes[0:2], byteorder='little')
            if possible_value in garbage_pointer_values:
                # Prepare next iteration and skip this one
                table_bytes = table_bytes[stride:]
                pointer_location += stride
                continue

            text_location = possible_value + POINTER_CONSTANT[f]
            found_text_locations.append(text_location)
            #print(hex(text_location))

            if pointer_location in previous_pointer_locations:
                print("%s was skipped since it's a duplicate" % hex(pointer_location))
            else:

                obj = BorlandPointer(GF, pointer_location, text_location)
                worksheet.write(row, 0, hex(text_location))
                worksheet.write(row, 1, hex(pointer_location))
                worksheet.write(row, 2, obj.text())

                previous_pointer_locations.append(pointer_location)
                row += 1 

            # Prepare the next iteration of the loop
            table_bytes = table_bytes[stride:]
            pointer_location += stride

    # Now look in the code blocks.
    for block in FILE_BLOCKS[f]:
        blk = Block(GF, block)
        for t in Dump.get_translations(blk, include_blank=True):
            #print(t)
            if t.location in found_text_locations:
                #print("skipping that one")
                continue

            all_locs = []
            pointer_location = '?'
            if any([s in t.japanese.decode('shift_jis') for s in strings_to_skip]):
                continue
            text_location = t.location
            look_for_int = t.location - POINTER_CONSTANT[f]
            look_for = look_for_int.to_bytes(2, byteorder='little')
            #codeblock_look_for = b'\x68' + look_for

            if GF.filestring[:POINTER_CONSTANT[f]].count(look_for) == 1:
                pointer_location = GF.filestring[:POINTER_CONSTANT[f]].find(look_for)
            else:
                all_locs = sorted(list(find_all(GF.filestring[:POINTER_CONSTANT[f]], look_for)))
                if text_location in POINTER_DISAMBIGUATION:
                    pointer_location = POINTER_DISAMBIGUATION[text_location]
                else:
                    for a in all_locs:
                        if a > POINTER_CONSTANT[f]:
                            # Skipping these for now, since they'll hopefully be in a table
                            continue

                        if len(all_locs) == 1:
                            pointer_location = all_locs[0]
                        #elif last_pointer_location < a < last_pointer_location + 0x100:
                        else:
                            pointer_location = a

            # Need to test its pointer_location against all other previous pointer_locations to avoid duplicates
            #print([hex(t) for t in previous_pointer_locations])
            #print(0x26ad8 in previous_pointer_locations)
            #print(hex(pointer_location))
            if pointer_location in previous_pointer_locations:
                print("Duplicate detected at %s, skipping" % hex(pointer_location))
                continue 

            obj = BorlandPointer(GF, pointer_location, text_location)
            worksheet.write(row, 0, hex(text_location))
            try:
                worksheet.write(row, 1, hex(pointer_location))
            except TypeError:
                problem_count += 1
                if len(all_locs) == 0:
                    print("Problem finding %s" % t.japanese.decode('shift_jis'), "not found")
                elif len(all_locs) == 1:
                    print(t.japanese.decode('shift_jis'), 'seems fine')
                else:
                    print("Problem finding %s" % t.japanese.decode('shift_jis'), "multiple found")

                worksheet.write(row, 1, '?')
            if len(all_locs) > 0:
                worksheet.write(row, 3, "%s" % ([hex(a) for a in all_locs]))

            worksheet.write(row, 2, obj.text())
            row += 1

            previous_pointer_locations.append(pointer_location)


PtrXl.workbook.close()

print("%s problems found" % problem_count)

# While we have all these variables, get a count of all the lines in the msg files
#count = 0
#for w in MsgDump.workbook.worksheets:
#    rows = list(w.rows)[1:]
#    for r in rows:
#        if r[0].value is not None:
#            count += 1
#    #print(w, count)
#print(count)
