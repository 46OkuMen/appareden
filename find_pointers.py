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


OriginalAp = Disk(SRC_DISK, dump_excel=Dump)
files_to_search = ['ORTITLE.EXE', 'ORMAIN.EXE']

try:
    os.remove('appareden_pointer_dump.xlsx')
except WindowsError:
    pass
PtrXl = PointerExcel('appareden_pointer_dump.xlsx')

for f in files_to_search:
    print(f)
    GF = Gamefile(os.path.join('original', f), disk=OriginalAp)
    worksheet = PtrXl.add_worksheet(GF.filename)
    row = 1
    for block in FILE_BLOCKS[f]:
        blk = Block(GF, block)
        last_pointer_location = 0
        for t in Dump.get_translations(blk, include_blank=True):
            text_location = t.location
            look_for_int = t.location - POINTER_CONSTANT[f]
            look_for = look_for_int.to_bytes(2, byteorder='little')
            if GF.filestring.count(look_for) == 1:
                pointer_location = GF.filestring.find(look_for)
            else:
                pointer_location = "Not found"

            print("%s: %s" % (hex(t.location), pointer_location))
            obj = BorlandPointer(GF, pointer_location, text_location)
            worksheet.write(row, 0, hex(text_location))
            try:
                worksheet.write(row, 1, hex(pointer_location))
            except TypeError:
                worksheet.write(row, 1, pointer_location)
            #try:
            #    worksheet.write(row, 2, obj.text())
            #except:
            #    worksheet.write(row, 2, '')
            row += 1
PtrXl.workbook.close()
