"""
    Utilities for encoding images as .GEM files, as used in Appareden.
"""

from romtools.disk import Disk
from rominfo import DEST_DISK
from PIL import Image
from bitstring import BitArray

NAMETAG_PALETTE = b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xfb\xac\xb9\xfd\x80\x21\x57\xd0\x66\x87\x3a\xcf\x8b\xff\xff\xff\x00'

RGB_PALETTE = [(0x00, 0x00, 0x00),
               (0x33, 0x33, 0x33),
               (0x88, 0x44, 0x33),
               (0xff, 0x44, 0x00),
               (0xdd, 0x99, 0x44),
               (0xff, 0xbb, 0x44),
               (0xcc, 0xbb, 0xaa),
               (0xff, 0xdd, 0x99),
               (0x00, 0x22, 0x88),
               (0x55, 0x77, 0x11),
               (0x00, 0x66, 0xdd),
               (0x88, 0x77, 0x66),
               (0xaa, 0xcc, 0x33),
               (0x88, 0xbb, 0xff),
               (0x00, 0x77, 0x88),
               (0xff, 0xff, 0xff),]

# 00 0 = (0000) black
# 3 33 = (1000) grey
# 38 4 = (0100) darkish brown (136 68 51 = 88 44 33)
# 0 f4 = (1100) burnt orange
# 4d 9 = (0010) brown (221 153 68 = dd 99 44)
# 4 fb = (1010) goldenrod
# ac b = (0110) orangish grey
# 9 fd = (1110) pale orange
# 80 2 = (0001) dark blue
# 1 57 = (1001) green
# d0 6 = (0101) cornflower blue
# 6 87 = (1101) mid grey    - when 00 ff ff ff / ff 00 aa ff, the first columns of the second one...
# 3a c = (0011) light green
# f 8b = (1011) periwinkle
# f ff = (0111) white
# 80 7 = (1111)?? teal    (color 0e? 0f?)

# Plane activation for each color in the palette.
PLANE_COLORS = [(1, 3, 5, 7, 9, 0xb, 0xd, 0xf),
                (2, 3, 6, 7, 0xa, 0xb, 0xe, 0xf),
                (4, 5, 6, 7, 0xc, 0xd, 0xe, 0xf),
                (8, 9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf)]

def RGB_to_nybblebrg(color):
    # Convert an (R, G, B) integer tuple to the b'\xBR\xG0' bytestring used in GEM.
    red, blue, green = color
    b = blue & 0xf0
    r = red >> 4
    g = green & 0xf0
    return (b+r).to_bytes(1, byteorder='little') + g.to_bytes(1, byteorder='little')
    # TODO: The nybblebrgs are actually stored in 3 nybbles, so need to take an even-numbered list of RGB tuples instead of one...

print(RGB_to_nybblebrg((221, 153, 68)))

img = Image.open('test.png')
width, height = img.size
blocks = img.size[0]//8
pix = img.load()

unique_patterns = []
pattern_locations = {}

row_cursor = 0
for b in range(blocks):
    for row in range(height):
        rowdata =[pix[col, row][0:3] for col in range(b*8, (b*8)+8)]
        #print(rowdata)
        #unique_patterns.add(tuple(rowdata))

        pattern = []

        for plane in range(4):

            for p in rowdata:
                palette_index = RGB_PALETTE.index(p)
                pattern.append(palette_index in PLANE_COLORS[plane])

        pattern = BitArray(pattern).bytes

        if pattern in unique_patterns:
            pattern_locations[pattern].append(row_cursor)
        else:
            unique_patterns.append(pattern)
            pattern_locations[pattern] = [row_cursor,]

        row_cursor += 1


for p in pattern_locations:
    print(p)

IMAGE_DATA_LOCATION = 0x29 + (len(unique_patterns)*4)    # where pattern data ends and image data begins.

with open('ORTITLE.GEM', 'wb') as f:
    f.write(b'Gem')
    f.write(b'\x02\x04\x00\x0e\x00')
    f.write(b'\x18\x00') # not sure what these bytes do
    f.write(height.to_bytes(2, byteorder='little'))
    f.write(IMAGE_DATA_LOCATION.to_bytes(2, byteorder='little'))
    f.write(b'\x00\x00') # not sure about these either
    f.write(NAMETAG_PALETTE)   # for now
    for p in unique_patterns:
        f.write(p)

    for pattern in unique_patterns:
        row_cursor = 0
        for loc in pattern_locations[pattern]:
            print(loc, row_cursor)
            if loc == row_cursor:
                f.write(b'\x41')
                row_cursor += 1
            elif loc - row_cursor <= 47:
                skip_and_write_code = 0x80 + (loc - row_cursor)
                f.write(skip_and_write_code.to_bytes(1, byteorder='little'))
                row_cursor = loc
            else:
                raise Exception
        
            print(pattern, loc)
        f.write(b'\x00')
    """# PATTERN 0
    f.write(b'\x41')  # draw pattern 1 time
    f.write(b'\x41')  # draw pattern 1 time
    f.write(b'\x41')  # draw pattern 1 time
    f.write(b'\x41')  # draw pattern 1 time
    f.write(b'\x41')  # draw pattern 1 time
    f.write(b'\x41')  # draw pattern 1 time
    f.write(b'\x41')  # draw pattern 1 time
    f.write(b'\x41')  # draw pattern 1 time

    f.write(b'\x00')
    # PATTERN 1
    f.write(b'\x88')  # skip 1 line
    f.write(b'\x48')  # draw pattern 8 times
    f.write(b'\x00')
    f.write(b'\x00')
    """


d = Disk(DEST_DISK)
d.insert('ORTITLE.GEM', path_in_disk='TGL/OR')