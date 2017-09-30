"""
    Calculates differences of string locations in FD and CD versions of Appareden.
"""

import os
from rominfo import FILE_BLOCKS, SHADOFF_COMPRESSED_EXES, SRC_DISK, DEST_DISK, SPARE_BLOCK, CONTROL_CODES, POSTPROCESSING_CONTROL_CODES
from rominfo import DUMP_XLS_PATH, MSG_XLS_PATH, POINTER_XLS_PATH
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel

Dump = DumpExcel(DUMP_XLS_PATH)
MsgDump = DumpExcel(MSG_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)

FILES_TO_CHECK = ['ORFIELD.EXE', 'ORBTL.EXE', 'ORTITLE.EXE', 'ORMAIN.EXE']

total_reinserted_strings = 0

FD_OFFSETS = []
CD_OFFSETS = []

for filename in FILES_TO_CHECK:
    fd_file_path = os.path.join('original', filename)
    cd_file_path = os.path.join('original', 'cd', filename)
    #if not os.path.isfile(gamefile_path):
    #    OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
    for gamefile_path in (fd_file_path, cd_file_path):
        print("Looking at %s now\n\n\n\n\n" % gamefile_path)

        gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)

        # TODO: Whoops, I can't use blocks at all in the CD files. Need to search the entire file...
        previous_text_offset = 0
        for t in Dump.get_translations(gamefile):
            #print(hex(t.location), t.english)
            if t.english == b'':
                not_translated = True
                t.english = t.japanese

            for cc in CONTROL_CODES:
                t.japanese = t.japanese.replace(cc, CONTROL_CODES[cc])
                t.english = t.english.replace(cc, CONTROL_CODES[cc])

            for cc in POSTPROCESSING_CONTROL_CODES:
                t.english = t.english.replace(cc, POSTPROCESSING_CONTROL_CODES[cc])

            #i = block.blockstring.index(t.japanese)
            j = gamefile.filestring.count(t.japanese)

            try:
                i = gamefile.filestring[previous_text_offset:].index(t.japanese) + previous_text_offset
            except ValueError:
                print(t, "not found")
                #CD_OFFSETS.append(-1)
                continue

            if gamefile_path == fd_file_path:
                FD_OFFSETS.append(i)
            elif gamefile_path == cd_file_path:
                CD_OFFSETS.append(i)
            else:
                raise Exception
            #print(hex(i), t.english)
            previous_text_offset = i
            print(hex(previous_text_offset))

assert len(FD_OFFSETS) == len(CD_OFFSETS)

for i in range(len(FD_OFFSETS)):
    print(hex(CD_OFFSETS[i] - FD_OFFSETS[i]))

#for o in FD_OFFSETS:
#    print(hex(o))