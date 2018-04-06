"""
    Calculates differences of string locations in FD and CD versions of Appareden.
"""

import os
from rominfo import FILE_BLOCKS, SHADOFF_COMPRESSED_EXES, SRC_DISK, DEST_DISK, CONTROL_CODES, POSTPROCESSING_CONTROL_CODES
from rominfo import DUMP_XLS_PATH, POINTER_XLS_PATH, POINTER_TABLES
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel
import cd_rominfo

Dump = DumpExcel(DUMP_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalAp = Disk(SRC_DISK, dump_excel=Dump, pointer_excel=PtrDump)
TargetAp = Disk(DEST_DISK)

FILES_TO_CHECK = ['ORFIELD.EXE', 'ORBTL.EXE', 'ORTITLE.EXE']

total_reinserted_strings = 0

FD_OFFSETS = []
CD_OFFSETS = []

for filename in FILES_TO_CHECK:
    fd_file_path = os.path.join('original', filename)
    cd_file_path = os.path.join('original_cd', 'CD', filename)
    #if not os.path.isfile(gamefile_path):
    #    OriginalAp.extract(filename, path_in_disk='TGL/OR', dest_path='original')
    #for gamefile_path in (fd_file_path, cd_file_path):
    #    print("Looking at %s now\n\n" % gamefile_path)

    #    gamefile = Gamefile(gamefile_path, disk=OriginalAp, dest_disk=TargetAp)

    print("\nLooking at %s now" % filename)
    with open(cd_file_path, 'rb') as f:
        cd_file = f.read()

        cursor = 0

        for t in Dump.get_translations(filename, include_blank=True):
            if b'[sysLN]' in t.japanese:
                t.japanese = t.japanese.replace(b'[sysLN]', b'\r\n')
            try:
                i = cd_file.index(t.japanese, cursor)
                print(t, i - t.location)
                cursor = i + len(t.japanese)
                pass
            except:
                print("Couldn't find %s" % t)

print()
for i, pt in enumerate(cd_rominfo.POINTER_TABLES['ORBTL.EXE']):
    fd_pt = POINTER_TABLES['ORBTL.EXE'][i]
    cd_start, cd_stop = cd_rominfo.orbtl_fd_to_cd(fd_pt[0]), cd_rominfo.orbtl_fd_to_cd(fd_pt[1])

    print(hex(cd_start), hex(pt[0]), cd_start - pt[0])
    print(hex(cd_stop),  hex(pt[1]), cd_stop - pt[1])

