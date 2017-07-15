import os
import re
from rominfo import FILES, FILE_BLOCKS, POINTER_CONSTANT, SRC_DISK, POINTER_DISAMBIGUATION
from romtools.dump import BorlandPointer, DumpExcel, PointerExcel
from romtools.disk import Gamefile, Block, Disk

strings_to_skip = ['ポインタが使われました', '      体', '       心', 'ＥＭＳ']

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
files_to_search = ['ORTITLE.EXE', 'ORMAIN.EXE', 'ORFIELD.EXE', 'ORBTL.EXE', 'SFIGHT.EXE']

# NEKORUN.EXE might not have pointers. Edit it manually? Mostly error messages anyway.
# ENDING.EXE is only error messages...?

problem_count = 0

try:
    os.remove('appareden_pointer_dump.xlsx')
except WindowsError:
    pass
PtrXl = PointerExcel('appareden_pointer_dump.xlsx')

for f in files_to_search:
    print(f)
    GF = Gamefile(os.path.join('original', f), disk=OriginalAp)
    try:
        worksheet = PtrXl.add_worksheet(GF.filename)
    except AttributeError:
        _ = input("You have the sheet open, close it and hit Enter")
        worksheet = PtrXl.add_worksheet(GF.filename)
    row = 1
    for block in FILE_BLOCKS[f]:
        blk = Block(GF, block)
        last_pointer_location = POINTER_CONSTANT[f]
        pointer_location = last_pointer_location
        for t in Dump.get_translations(blk, include_blank=True):
            all_locs = []
            if any([s in t.japanese.decode('shift_jis') for s in strings_to_skip]):
                continue
            text_location = t.location
            look_for_int = t.location - POINTER_CONSTANT[f]
            look_for = look_for_int.to_bytes(2, byteorder='little')
            if GF.filestring.count(look_for) == 1: #and GF.filestring.find(look_for) > POINTER_CONSTANT[f]:
                pointer_location = GF.filestring.find(look_for)
            else:
                all_locs = sorted(list(find_all(GF.filestring, look_for)))
                if text_location in POINTER_DISAMBIGUATION:
                    pointer_location = POINTER_DISAMBIGUATION[text_location]
                else:
                    for a in all_locs:
                        if len(all_locs) == 1:
                            pointer_location = all_locs[0]
                        elif last_pointer_location < a < last_pointer_location + 0x100:
                            pointer_location = a

            if pointer_location == last_pointer_location:
                pointer_location = "?"

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
            if pointer_location != "?":
                last_pointer_location = pointer_location
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
