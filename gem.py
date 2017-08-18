"""
    Utilities for encoding images as .GEM files, as used in Appareden.
"""

from romtools.disk import Disk
from rominfo import DEST_DISK
from PIL import Image
from bitstring import BitArray

d = Disk(DEST_DISK)
d.insert('ORTITLE.GEM', path_in_disk='TGL/OR')


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

img = Image.open('test.png')
width, height = img.size
blocks = img.size[0]//8
total_rows = blocks*height
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
        #elif pattern == b'\x00\x00\x00\x00':
        #    pass
        else:
            unique_patterns.append(pattern)
            pattern_locations[pattern] = [row_cursor,]

        row_cursor += 1

"""
parsed_pattern_locations = {}
for p in pattern_locations:
    # TODO: Detect stuff like: X in a row (0x41+), X in a row every other row (0x21+), X in a row every 4 rows (0x11+)
    # Find some way to store them in parsed_pattern_locations...
    pass

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

    row_cursor = 0
    starting_row_cursor = 0

    for i, pattern in enumerate(unique_patterns):
        row_cursor = starting_row_cursor
        print("Starting new pattern. row_cursor:", row_cursor)
        for loc in pattern_locations[pattern]:
            if pattern == unique_patterns[0] and loc == 0:
                row_cursor += 1
                continue
            elif pattern == b'\x00\x00\x00\x00':
                continue

            print(loc, row_cursor)

            while loc - row_cursor > 1279:
                skip_code = 0x80
                row_cursor += 1280
                f.write(skip_code.to_bytes(1, byteorder='little'))

            while loc - row_cursor > 63:
                skip_code = 0xc0
                row_cursor += 64
                f.write(skip_code.to_bytes(1, byteorder='little'))

            if loc == row_cursor:
                f.write(b'\x41')
            elif loc - row_cursor <= 63:
                skip_and_write_code = 0x81 + ((loc - row_cursor) % total_rows)
                if loc == pattern_locations[pattern][0]:
                    starting_row_cursor += (loc - row_cursor)
                f.write(skip_and_write_code.to_bytes(1, byteorder='little'))
                row_cursor = loc
            else:
                raise Exception

            row_cursor += 1
        
            print(pattern, loc)
        f.write(b'\x00')
        starting_row_cursor += 1

    f.write(b'\x00'*20)


    # Checkerboard first pattern: 41 83 41 83...   (starting row_cursor: 0)
    # Checkerboard second pattern: 82 41 83 41 83 41...  (starting row_cursor: 1)

# Why does the first instance of the first pattern (41) always want to write it twice, while 41 writes it just once the rest of the time??
    # It seems to write one instances of the first pattern even if you put 00's...

# Looks like the cursor does not reset itself between patterns...??
    # I need to get this straight. Seems like it resets itself sometimes and not other times.
    # It seems to reset for the checkerboard pattern, but not the smiley face pattern?
    # Maybe each one just starts with row_cursor = the index  in unique_patterns?

# Stick figure test:
    # 00: 00 (Correct...?)  (starting row_cursor: 0)
    # 28: 41 41 (Correct)   (starting row_cursor: 1)
    # 42: 83 41 (Correct)   (starting row_cursor: 2)  (81: write 1; 82: skip 1, write 1; 83: skip 2, write 1)
    # 7e: 82 (Correct)      (starting row_currsor: 5 (prev + 1 + (83-81)))
    # 08: 83 41 82 41 41 (Correct)  (starting row_cursor: 7 (prev + 1 + (82-81)))
    # 7c: 41 (Incorrect, should be 82)  (starting row_cursor: 10? but calculation says 11... (prev + 1 + (83-81) + (82-81)))
        # The 80 control codes only advance the starting_row_cursor when they're the first byte of the segment???
    # 1c: 84
    # 34:
    # 24:

# Maybe I just misunderstand how the 80 control codes work...
    # It looks like 80s advance the cursor for all further patterns.

d = Disk(DEST_DISK)
d.insert('ORTITLE.GEM', path_in_disk='TGL/OR')
"""

# TODO: I think the key to breaking the 64-row barrier is in the blocks that start with 09, 0a, 0b, etc.
