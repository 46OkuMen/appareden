"""
    Utilities for encoding images as .GEM files, as used in Appareden.
    Possibly useful for other TGL/GIGA games (Farland Story? Edge?) but untested.
"""

from romtools.disk import Disk
from rominfo import DEST_DISK
from PIL import Image
from bitstring import BitArray

NAMETAG_PALETTE = b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xfb\xac\xb9\xfd\x80\x21\x57\xd0\x66\x87\x3a\xcf\x8b\xff\xff\xff\x00'
MAP_PALETTE =     b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xeb\xac\xb9\xfd\x60\x31\x77\xb0\x76\x87\x3c\xcd\x6c\x6a\x7f\xff\x00'
SHIP_PALETTE =    b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xfb\xac\xb9\xfd\x60\x31\x77\xb0\x76\x87\x3c\xcd\x6c\xda\xcf\xff\x00'
TITLE_PALETTE =   b'\x00\x01\x11\x38\x40\xD4\x5C\x94\xFC\xAC\xB9\xEC\x80\x21\x57\xE1\x76\x87\x29\xBC\x7C\xFF\xFF\xFF\x00'
TEFF_PALETTE =    b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xfb\xac\xb9\xfd\x80\x21\x57\xd0\x66\x87\x3a\xcf\x8b\xa6\xaf\xff\x32\x33\x00'
                  # TODO: Why is this longer than the others??

NAMETAG_PALETTE_RGB = [(0x00, 0x00, 0x00),
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


MAP_PALETTE_RGB =    [(0x00, 0x00, 0x00),   # black 10-11
                      (0x33, 0x33, 0x33),   # darkGrey 11-12
                      (0x88, 0x44, 0x33),   # darkBrown 13-14
                      (0xff, 0x44, 0x00),   # orange 14-15
                      (0xdd, 0x99, 0x44),   # lightBrown 16-17
                      (0xee, 0xbb, 0x44),   # lighterBrown 17-18
                      (0xcc, 0xbb, 0xaa),   # lightGrey 19-1a
                      (0xff, 0xdd, 0x99),   # peach 1a-1b
                      (0x00, 0x33, 0x66),   # darkBlue 1c-1d
                      (0x77, 0x77, 0x11),   # olive 1d-1e
                      (0x00, 0x77, 0xbb),   # blue 1f-20
                      (0x88, 0x77, 0x66),   # midGrey 20-21
                      (0xcc, 0xcc, 0x33),   # lightGreen 22-23
                      (0x66, 0xcc, 0xdd),   # lightBlue 23-24
                      (0xaa, 0x77, 0x66),   # redBrown 25-26
                      (0xff, 0xff, 0xff)]   # white 26-27

# Plane activation for each color in the palette.
# Which bit is active there
PLANE_COLORS = [(1, 3, 5, 7, 9, 0xb, 0xd, 0xf),
                (2, 3, 6, 7, 0xa, 0xb, 0xe, 0xf),
                (4, 5, 6, 7, 0xc, 0xd, 0xe, 0xf),
                (8, 9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf)]

MAP_PALETTE_COLORS = ['black', 'darkGrey', 'darkBrown', 'orange',
                      'lightBrown', 'lighterBrown', 'lightGrey', 'peach',
                      'darkBlue', 'olive', 'blue', 'midGrey',
                      'lightGreen', 'lightBlue', 'redBrown', 'white']

# TMAP_32A
SHIP_PALETTE_RGB = [
    (0x00, 0x00, 0x00),
    (0x33, 0x33, 0x33),
    (0x88, 0x44, 0x33),
    (0xff, 0x44, 0x00),
    (0xdd, 0x99, 0x44),
    (0xff, 0xbb, 0x44),
    (0xcc, 0xbb, 0xaa),
    (0xff, 0xdd, 0x99),
    (0x00, 0x33, 0x66),
    (0x77, 0x77, 0x11),
    (0x00, 0x77, 0xbb),
    (0x88, 0x77, 0x66),
    (0xcc, 0xcc, 0x33),
    (0x66, 0xcc, 0xdd),
    (0xaa, 0xcc, 0xdd),
    (0xff, 0xff, 0xff)
]

TITLE_PALETTE_RGB = [(0x00, 0x00, 0x00),
               (0x11, 0x11, 0x11),
               (0x88, 0x44, 0x33),     # also 88 44 33,  84 46 38
               (0xdd, 0x44, 0x00),
               (0xcc, 0x99, 0x55),
               (0xff, 0xcc, 0x44),
               (0xcc, 0xbb, 0xaa),
               (0xee, 0xcc, 0x99),
               (0x00, 0x22, 0x88),
               (0x55, 0x77, 0x11),
               (0x11, 0x77, 0xee),
               (0x88, 0x77, 0x66),
               (0x99, 0xbb, 0x22),
               (0x77, 0xcc, 0xcc),
               (0xfa, 0xfa, 0xfa),
               (0xff, 0xff, 0xff),]

TEFF_PALETTE_RGB = [(0x00, 0x00, 0x00),
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
               (0x66, 0xaa, 0xaa),
               (0xff, 0xff, 0xff),]

def get_closest_color_index(palette, rgb):
    hammings = [255]*16
    for i, color in enumerate(palette):
        hamming = 0
        for val in range(3):
            hamming += abs(color[val] - rgb[val])
        hammings[i] = hamming
    return hammings.index(min(hammings))



NAMETAG_PALETTE_IMAGES = ['BENIMARU', 'GENNAI', 'GENTO', 'HANZOU', 'HEILEE', 'MEIRIN', 'OUGI', 'TAMAMO', 'GOEMON', 'SHIROU']
MAP_PALETTE_IMAGES = ['TMAP_00', 'TMAP_00A', 'TMAP_01A', 'TMAP_01B', 'TMAP_03A', 'TMAP_06A', 'TMAP_10B', 'TMAP_11A',
                      'TMAP_12B', 'TMAP_14A', 'TMAP_16B', 'TMAP_27A', 'TMAP_29B', ]
SHIP_PALETTE_IMAGES = ['TMAP_32A',]
TITLE_PALETTE_IMAGES = ['ORTITLE', 'GENNAIJ', 'GOEMONJ', 'HANZOJ', 'SHIROUJ']
TEFF_PALETTE_IMAGES = ['TEFF_00A', 'TEFF_0AA', 'TEFF_0BA', 'TEFF_01A', 'TEFF_02A', 'TEFF_03A', 'TEFF_04A', 'TEFF_05A',
                       'TEFF_06A', 'TEFF_07A', 'TEF_08A', 'TEFF_09A', 'TEFF_12A', 'TEFF_13A', 'TEFF_14A', 'TEFF_15A',
                       'TEFF_16A', 'TEFF_17A',]




class Pattern:
    def __init__(self, bytestring):
        self.bytestring = bytestring
        self.first = bytestring[0]
        self.second = bytestring[1]
        self.third = bytestring[2]
        self.fourth = bytestring[3]

    def color_sequence(self):
        #print(self.first)
        b1 = BitArray("0x{:02x}".format(self.first), length=8).bin
        b2 = BitArray("0x{:02x}".format(self.second), length=8).bin
        b3 = BitArray("0x{:02x}".format(self.third), length=8).bin
        b4 = BitArray("0x{:02x}".format(self.fourth), length=8).bin

        #print(self)
        #print(b1, b2, b3, b4)

        result = ''

        for i in range(8):
            #this_color = b1[i] + b2[i] + b3[i] + b4[i]
            this_color = b4[i] + b3[i] + b2[i] + b1[i]
            #print(this_color)
            color = BitArray('0b' + this_color)

            # Hmm. Can't just get the color with that index in MAP_PALETTE_COLORS.
            # (More accurately, they're in reverse order. First plane is the ones place, 
            # second plane is the twos place, third plane is the fours place, and fourth plane is the eights place.)
            ##print(color.uint)
            #result += '%s (%s) ' % (MAP_PALETTE_COLORS[color.uint], this_color)
            result += '%s ' % (MAP_PALETTE_COLORS[color.uint])

        return result

    def has_sequence(self, colors):
        return colors in self.color_sequence()

    def __repr__(self):
        return "%s %s %s %s" % (hex(self.first)[2:], hex(self.second)[2:], hex(self.third)[2:], hex(self.fourth)[2:])

    def __eq__(self, other):
        return self.bytestring == other.bytestring

def decode(filename):
    with open(filename, 'rb') as f:
        gem = f.read()

    start_writing = int.from_bytes(gem[0xc:0xe], 'little')
    print(hex(start_writing))
    pattern_bytes = gem[0x29:start_writing]
    patterns = []
    for i in range(0, len(pattern_bytes), 4):
        patterns.append(pattern_bytes[i:i+4])
    #print(patterns)

    pattern_sequence = []
    sequence = b''
    sentinel = start_writing
    original_index = 0x29
    while sentinel < len(gem):
        while gem[sentinel] != 0:
            sequence += gem[sentinel].to_bytes(1, 'little')
            sentinel += 1
        pat = Pattern(patterns[0])
        pattern_sequence.append((pat, sequence, original_index))

        #print(pat.color_sequence())

        if pat.has_sequence('darkGrey darkGrey darkGrey darkGrey midGrey midGrey midGrey midGrey'):
            # Not found...?
            print(pat, sequence)

        #print(pat, sequence)
        #if sentinel < 0x9000:
        #    print(pat.color_sequence())

        sequence = b''
        patterns.pop(0)
        original_index += 4
        sentinel += 1

    print(len(pattern_sequence), "unique patterns in GEM")

    # Open TMAP_00A.PNG and get some regions to search for

    #img = Image.open('TMAP_00A_shopsigns.PNG')
    img = Image.open('TMAP_00A.PNG')
    width, height = img.size
    pix = img.load()
    blocks = img.size[0]//8
    png_patterns = []
    for b in range(blocks):
        for row in range(height):
            rowdata =[pix[col, row][0:3] for col in range(b*8, (b*8)+8)]
            pattern = []

            for plane in range(4):
                for p in rowdata:
                    try:
                        palette_index = MAP_PALETTE_RGB.index(p)
                    except ValueError:
                        palette_index = get_closest_color_index(MAP_PALETTE_RGB, p)
                    pattern.append(palette_index in PLANE_COLORS[plane])
            pattern = Pattern(BitArray(pattern).bytes)
            #print(Pattern(pattern).color_sequence())
            #print(Pattern(pattern).color_sequence())

            if pattern not in png_patterns:
                png_patterns.append(pattern)

    print(len(png_patterns), "unique patterns in PNG")

    # Looking for shop sign patterns in the .GEM pattern list.
    # Not very many at all!
    # Something is wrong.
    #for u in png_patterns:
        #print(Pattern(u).color_sequence())
        #for i in pattern_sequence:
        #    print(i[0])
        #    if i[0] == Pattern(u):
        #        print(Pattern(u), Pattern(u).color_sequence(), i[1])

    # Let's try looking for .GEM patterns in the entire image patterns list.
    #for p, q in pattern_sequence:
    #    if p not in png_patterns:
    #        print(p, q)
    # Every GEM pattern is present in the PNG pattern sequence.


    #for p in pattern_sequence:
    #    print(p[0].color_sequence())

    for q in png_patterns:
        print(q.color_sequence())

    print("Every shop-sign pattern that's present in the GEM patterns:")
    shop_patterns = []
    for p in png_patterns:
        for q in pattern_sequence:
            if p == q[0]:
                shop_patterns.append(q)
                print(p.color_sequence())
                print(q[2])
    # It appears to just be a mix of the different black, white, and grey colors.
    # Nothing useful for the interior of the shop signs...


    print()
    target = 1
    for s in shop_patterns[target:target+1]:
        print(s[0].bytestring)
        print(s[1])
        #gem = gem.replace(s[0].bytestring, b'\xff\xff\xff\xff')

    with open('patched/' + filename, 'wb') as f:
        f.write(gem)

    # TODO: Replace one of these patterns with something else in a new GEM, see what happens.
        # (Down the line I should get a PIL script that mentions all the differences between two images.
            # Wouldn't automate the taking of screenshots but might help in the harder-to-notice diffs.)


    # Hmm. 4402 unique patterns in GEM, 8637 unique patterns in PNG...
    # What's going on here?

    # There are likely control codes that take previous patterns and modify them.



def encode(filename, dest_disk=DEST_DISK):
    """Encode an image file as GEM and reinsert it."""
    just_filename = filename.split('.')[0]
    gem_filename = just_filename + '.GEM'
    print("Encoding", gem_filename)

    # "Polymorphism"
    if just_filename in NAMETAG_PALETTE_IMAGES:
        print("Using nametag palette")
        palette_bytes = NAMETAG_PALETTE
        palette_rgb = NAMETAG_PALETTE_RGB
    elif just_filename in MAP_PALETTE_IMAGES:
        print("Using map palette")
        palette_bytes = MAP_PALETTE
        palette_rgb = NAMETAG_PALETTE_RGB
    elif just_filename in SHIP_PALETTE_IMAGES:
        print("Using ship palette")
        palette_bytes = SHIP_PALETTE
        palette_rgb = SHIP_PALETTE_RGB
    elif just_filename in TITLE_PALETTE_IMAGES:
        print("Using title palette")
        palette_bytes = TITLE_PALETTE
        palette_rgb = TITLE_PALETTE_RGB
    elif just_filename in TEFF_PALETTE_IMAGES:
        print("Using text effect palette")
        palette_bytes = TEFF_PALETTE
        palette_rgb = TEFF_PALETTE_RGB
    else:
        print(filename)
        raise Exception

    img = Image.open(filename)
    width, height = img.size
    pix = img.load()

    blocks = img.size[0]//8
    total_rows = blocks*height
    unique_patterns = []
    pattern_locations = {}

    row_cursor = 0
    for b in range(blocks):
        for row in range(height):
            rowdata =[pix[col, row][0:3] for col in range(b*8, (b*8)+8)]

            pattern = []

            for plane in range(4):

                for p in rowdata:
                    try:
                        palette_index = palette_rgb.index(p)
                    except ValueError:
                        palette_index = get_closest_color_index(palette_rgb, p)
                    pattern.append(palette_index in PLANE_COLORS[plane])

            pattern = BitArray(pattern).bytes

            if pattern in unique_patterns:
                pattern_locations[pattern].append(row_cursor)
            else:
                unique_patterns.append(pattern)
                pattern_locations[pattern] = [row_cursor,]

            row_cursor += 1

    IMAGE_DATA_LOCATION = 0x10 + len(palette_bytes) + (len(unique_patterns)*4)

    with open(gem_filename, 'wb') as f:
        f.write(b'Gem')
        f.write(b'\x02\x04\x00\x0e\x00')
        f.write(b'\x30\x00') # not sure what these bytes do. 18 for nametag, 30 for teff, doesn't seem to matter
        f.write(height.to_bytes(2, byteorder='little'))
        f.write(IMAGE_DATA_LOCATION.to_bytes(2, byteorder='little'))
        f.write(b'\x00\x00') # not sure about these either
        f.write(palette_bytes)
        for p in unique_patterns:
            #print(p)
            f.write(p)

        row_cursor = 0
        starting_row_cursor = 0

        for i, pattern in enumerate(unique_patterns):
            row_cursor = starting_row_cursor
            chain_count = 0
            skip_past = -1
            #print("Start pattern %s. row_cursor: %s" % (pattern, row_cursor))

            for i, loc in enumerate(pattern_locations[pattern]):
                # First pattern gets placed in the upper left corner automatically
                if pattern == unique_patterns[0] and loc == 0:
                    row_cursor += 1
                    row_cursor %= total_rows
                    continue
                """

                if i <= skip_past:
                    continue

                # Look for patterns that alternate every two rows. i.e. two-chains
                two_chain = 0
                # Only one per pattern?
                if skip_past == -1:
                    #while pattern_locations[pattern][i+two_chain] == loc + (2 * two_chain):
                    while loc + (two_chain*2) in pattern_locations[pattern] and loc + ((two_chain*2)-1) not in pattern_locations[pattern]:
                        two_chain += 1
                        skip_past = i + two_chain

                        if i+two_chain >= len(pattern_locations[pattern]):
                            break
                    if two_chain > 1:
                        two_chain_byte = 0x20 + two_chain
                        f.write(two_chain_byte.to_bytes(1, byteorder='little'))
                        row_cursor = pattern_locations[pattern][i+two_chain-1]
                        continue
                """

                """
                if i <= skip_past:
                    print("Skipping past", loc)

                    #if i == len(pattern_locations[pattern])-1:
                        #f.write(b'\x00')
                        #starting_row_cursor += 1
                        #starting_row_cursor %= total_rows
                        #break
                    continue

                if skip_past == -1:
                    if loc + 1 not in pattern_locations[pattern] and loc + 2 in pattern_locations[pattern] and loc + 3 not in pattern_locations[pattern]:
                        print(pattern_locations[pattern])
                        print("writing a 21")
                        print("Chain count is", chain_count)
                        f.write(b'\x82\x82')
                        #f.write(b'\x21')
                        skip_past = i + 1
                        row_cursor = loc + 3
                        continue
                """

                #print("Row cursor is now", row_cursor)
                # Look for patterns that repeat every row.
                if loc == row_cursor:
                    chain_count += 1
                else:
                    while chain_count > 255:
                        repeat_byte = 0x18
                        while chain_count > 255 and repeat_byte < 0x1f:
                            repeat_byte += 1
                            chain_count -= 256

                        f.write(repeat_byte.to_bytes(1, 'little'))
                        #print(gem_filename, "uses the 256x repeat byte", hex(repeat_byte))
                    while chain_count > 31:
                        f.write(b'\x5f')
                        chain_count -= 31
                    while chain_count > 0:
                        chain = 0x40 + chain_count
                        f.write(chain.to_bytes(1, byteorder='little'))
                        chain_count = 0

                    if loc - row_cursor > 16065: # above far skip "ff ff"
                        first_byte = 0x80
                        second_byte = ((loc - row_cursor) + 1) // 256
                        third_byte = ((loc - row_cursor) + 1) % 256
                        f.write(first_byte.to_bytes(1, byteorder='little'))
                        f.write(second_byte.to_bytes(1, byteorder='little'))
                        f.write(third_byte.to_bytes(1, byteorder='little'))


                        if loc == pattern_locations[pattern][0]:
                            starting_row_cursor = loc
                        row_cursor = loc
                        #print("Ultra skip: %s %s %s, row_cursor after: %s" % (hex(first_byte), hex(second_byte), hex(third_byte), row_cursor))

                    elif loc - row_cursor >= 63:
                        first_byte = 0xc0 + ((loc - row_cursor) + 1) // 256
                        second_byte = ((loc - row_cursor) + 1) % 256
                        f.write(first_byte.to_bytes(1, byteorder='little'))
                        f.write(second_byte.to_bytes(1, byteorder='little'))

                        if loc == pattern_locations[pattern][0]:
                            starting_row_cursor = loc
                        row_cursor = loc
                        #print("Far skip: %s %s, row_cursor after: %s" % (hex(first_byte), hex(second_byte), row_cursor))
                        assert row_cursor == loc
                    elif loc - row_cursor < 63:
                        skip_and_write_code = 0x81 + ((loc - row_cursor) % total_rows)
                        if loc == pattern_locations[pattern][0]:
                            starting_row_cursor = loc
                        f.write(skip_and_write_code.to_bytes(1, byteorder='little'))
                        #print("Short skip: %s, row_cursor after: %s" % (hex(skip_and_write_code), row_cursor))
                        row_cursor = loc
                    else:
                        raise Exception

                row_cursor += 1
                row_cursor %= total_rows

            # Catch the last chain
            while chain_count > 31:
                f.write(b'\x5f')
                chain_count -= 31
            while chain_count > 0:
                chain = 0x40 + chain_count
                f.write(chain.to_bytes(1, byteorder='little'))
                chain_count = 0

            #print("Writing 00")
            f.write(b'\x00')
            starting_row_cursor += 1
            starting_row_cursor %= total_rows

        f.write(b'\x00'*80)  # for good measure. TODO: Still necessary?

    d = Disk(dest_disk)
    d.insert(gem_filename, path_in_disk='TGL/OR')

def write_spz(filename, n):
    """Write a SPZ sprite-sheet-spec for an image, with n sprites."""
    just_filename = filename.split('.')[0]
    spz_filename = just_filename + '.SPZ'

    # TODO: Any way I can programatically guess the n value from the image size?

    with open(spz_filename, 'wb') as f:
        f.write(b'FSPR')
        f.write(n.to_bytes(2, byteorder='little'))
        f.write(bytes(just_filename, encoding='ascii'))
        f.write(b'\x00'*0x12)

        # TODO: This is configured for simple 32x32 sprites. More flexibility comes later.

        top_cursor = 0
        bottom_cursor = n*2
        pointer_start = 0x20 + (n*2)

        for sprite in range(n):
            f.write(pointer_start.to_bytes(2, byteorder='little'))
            pointer_start +=0xf

        for sprite in range(n):
            f.write(b'\x04')     # number of 16x16 tiles in sprite
            f.write(b'\x14\x13') # which columns are used??

            f.write(b'\x13\x44')
            f.write(top_cursor.to_bytes(1, byteorder='little'))
            top_cursor += 1

            f.write(b'\x14\x44')
            f.write(top_cursor.to_bytes(1, byteorder='little'))
            top_cursor += 1

            f.write(b'\x13\x48')
            f.write(bottom_cursor.to_bytes(1, byteorder='little'))
            bottom_cursor += 1

            f.write(b'\x14\x48')
            f.write(bottom_cursor.to_bytes(1, byteorder='little'))
            bottom_cursor += 1*8 # TODO: ????

    d = Disk(DEST_DISK)
    d.insert(spz_filename, path_in_disk='TGL/OR')

def get_tile(img, n):
    # TODO: Not sure I have the right idea here. What about the larger images?
    # There are more than 255 tiles in them, so clearly it can't just be one byte...
    width, height = img.size
    #pix = img.load()

    x = (n*16) % width
    y = ((n*16) // width) * 16

    assert x < width
    if y >= height:
        y = 0
    assert y < height

    #$print(n, x, y)

    rect = (x, y, x+16, y+16)

    region = img.crop(rect)

    return region



def decode_spz(filename, image):
    just_filename = filename.split('.')[0]

    image_output_filename = image.replace('.png', '_sheet.png')

    with open(filename, 'rb') as f:
        file_contents = f.read()
    n = file_contents[4]

    img = Image.open(image)

    SPRITESHEET_MAX_X = 1280
    SPRITESHEET_MAX_Y = 4000

    dest_img = Image.new("RGB", (SPRITESHEET_MAX_X, SPRITESHEET_MAX_Y), "white")

    sprite_offsets = []
    cursor = 0x20
    for x in range(n):
        loc = int.from_bytes(file_contents[cursor:cursor+2], byteorder='little')
        cursor += 2
        #print(loc)
        sprite_offsets.append(loc)

    sprite_offsets.append(len(file_contents))

    # Starting points of the output sprite in the output image
    dest_x, dest_y = 0, 64

    # Trying to understand how high/low these can go
    tile_xs = []
    tile_ys = []

    for i, s in enumerate(sprite_offsets):
        #dest_x = (i * 256) % 1280
        #dest_y = 256 + (i // 5) * 256
        #print('')

        #tile_constant = 0

        try:
            next_s = sprite_offsets[i+1]
        except IndexError:
            break
        #print(s, next_s)
        sprite_spec = file_contents[s:next_s]
        tile_n = sprite_spec[0]
        assert sprite_spec[1] == 0x14
        assert sprite_spec[2] == 0x13
        sprite_cursor = 3
        print()
        sprite_width = 16
        #previous_tile = 0
        for n in range(tile_n):

            this_tile = sprite_spec[sprite_cursor:sprite_cursor+3]
            sprite_cursor += 3

            x_marker = int(this_tile[0])
            y_marker = int(this_tile[1])
            tile_marker = int(this_tile[2])

            #for t in this_tile:
            #    print(hex(t) + ' ', end='')

            if y_marker % 4 == 0:
                tile_constant = 0
            elif y_marker % 4 == 1:
                tile_constant = 256
                y_marker -= 1
            elif y_marker % 4 == 2:
                tile_constant = 512
                y_marker -= 2
            else:
                print("Weird tile Y here:", y_marker)

            tile = get_tile(img, tile_marker + tile_constant)

            #print(tile_marker)

            #tile_xs.append(x_marker)
            #tile_ys.append(y_marker)

            tile_x = (x_marker - 9) * 16
            tile_y = (y_marker - 0x44) * 4

            print(tile_x)

            if sprite_width < tile_x:
                sprite_Width = tile_x

            dest_img.paste(tile, (tile_x + dest_x, tile_y + dest_y))

        print(i, "width", sprite_width)
        print(i, "tile x", tile_x)
        dest_x += tile_x + 64
        #dest_y += 32
        if dest_x > 1000:
            dest_y += 128
            dest_x = 0

    dest_img.show()
    dest_img.save(image_output_filename)


if __name__ == '__main__':
    FILES_TO_ENCODE = ['TMAP_00.png', 'TMAP_00A.png', 'TMAP_01A.png', 'TMAP_01B.png', 'TMAP_03A.png', 'TMAP_06A.png',
                       'TMAP_10B.png', 'TMAP_11A.png', 'TMAP_12B.png', 'TMAP_14A.png', "TMAP_16B.png",
                       'TMAP_27A.png', 'TMAP_29B.png', 'TMAP_32A.png',
                       'ORTITLE.png', 'GENTO.png', 'BENIMARU.png', 'HANZOU.png', 'TAMAMO.png', 'GOEMON.png',
                       'HEILEE.png', 'SHIROU.png', 'MEIRIN.png', 'GENNAI.png', 'OUGI.png',
                       'GENNAIJ.png', 'GOEMONJ.png', 'SHIROUJ.png', 'HANZOJ.png']
    for f in FILES_TO_ENCODE:
        encode(f)
    #encode('TEFF_00A.png')
    #encode('ORTITLE.png')
    #encode('GENTO.png')
    #write_spz('TEFF_00A.png', 6)
    #decode_spz('SFCHR_98.SPZ', 'SFCHR_98.png')
    #decode_spz('TEFF_00A.SPZ', 'TEFF_00A.png')   # Simple and already documented
    #decode_spz('SFCHR_99.SPZ', 'SFCHR_99_background01.png' )    # Much more complex
    #decode_spz('CHAR_32A.SPZ', 'CHAR_32A.png')

    #decode('TMAP_00A.GEM')
