import os
import re
from rominfo import FILES, FILE_BLOCKS, POINTER_CONSTANT, SRC_DISK
from romtools.dump import BorlandPointer, DumpExcel, PointerExcel
from romtools.disk import Gamefile, Block, Disk

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
            text_location = t.location
            look_for_int = t.location - POINTER_CONSTANT[f]
            look_for = look_for_int.to_bytes(2, byteorder='little')
            if GF.filestring.count(look_for) == 1 and GF.filestring.find(look_for) > POINTER_CONSTANT[f]:
                pointer_location = GF.filestring.find(look_for)
                #print("%s: %s" % (hex(t.location), hex(pointer_location)))
            else:
                all_locs = list(find_all(GF.filestring, look_for))
                all_locs = [l for l in all_locs if l > POINTER_CONSTANT[f] ]
                for a in all_locs:
                    if last_pointer_location < a < last_pointer_location + 0x100:
                        pointer_location = a
                #pointer_location = "Not found"

            if pointer_location == last_pointer_location:
                pointer_location = "?"

            obj = BorlandPointer(GF, pointer_location, text_location)
            worksheet.write(row, 0, hex(text_location))
            try:
                worksheet.write(row, 1, hex(pointer_location))
            except TypeError:
                worksheet.write(row, 1, pointer_location)
                worksheet.write(row, 3, "%s" % ([hex(a) for a in all_locs]))

            worksheet.write(row, 2, obj.text())
            #try:
            #    worksheet.write(row, 2, obj.text())
            #except:
            #    worksheet.write(row, 2, '')
            row += 1
            if pointer_location != "?":
                last_pointer_location = pointer_location
PtrXl.workbook.close()

# While we have all these variables, get a count of all the lines in the msg files
#count = 0
#for w in MsgDump.workbook.worksheets:
#    rows = list(w.rows)[1:]
#    for r in rows:
#        if r[0].value is not None:
#            count += 1
#    #print(w, count)
#print(count)
