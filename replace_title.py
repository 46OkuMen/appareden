"""
    Replaces the title screen with a GEM image provided as a CL argument.
    Useful for quick viewing, and works better than MLD.
"""

import sys
import os
from shutil import copyfile
from romtools.disk import Disk
from rominfo import DEST_DISK

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python replace_title.py ImageToView.GEM")
    gem_filename = sys.argv[1]

    # View an image from the FD game
    #gem_filename = os.path.join("original", "OR", gem_filename)

    # View an image from the CD game
    #gem_filename = os.path.join("original", "CD", gem_filename)

    # View an edited image
    gem_filename = os.path.join("patched", gem_filename)

    copyfile(gem_filename, "ORTITLE.GEM")

    #with open("ORTITLE.GEM", 'rb+') as f:
    #    # Red/grey   are between 4000-5000
    #    # Green/blue are between 5000-6000.
    #    N = 0x5504
    #    f.seek(N)
    #    f.write(b'\x00'*(0x8721 - N))

    d = Disk(DEST_DISK)
    d.insert("ORTITLE.GEM", path_in_disk='TGL/OR')

   #d.insert(gem_filename, path_in_disk='TGL/OR')