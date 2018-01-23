import sys
import os
from shutil import copyfile
from romtools.disk import Disk
from rominfo import DEST_DISK

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python replace_title.py ImageToView.GEM")
    gem_filename = sys.argv[1]

    #gem_filename = os.path.join("original", "OR", gem_filename)
    #gem_filename = os.path.join("original", "CD", gem_filename)
    gem_filename = os.path.join("patched", gem_filename)

    copyfile(gem_filename, "ORTITLE.GEM")

    d = Disk(DEST_DISK)
    d.insert("ORTITLE.GEM", path_in_disk='TGL/OR')