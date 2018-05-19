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


MAP_PALETTE_RGB =    [(0x00, 0x00, 0x00),
                      (0x33, 0x33, 0x33),
                      (0x88, 0x44, 0x33),
                      (0xff, 0x44, 0x00),
                      (0xdd, 0x99, 0x44),
                      (0xee, 0xbb, 0x44),
                      (0xcc, 0xbb, 0xaa),
                      (0xff, 0xdd, 0x99),
                      (0x00, 0x33, 0x66),
                      (0x77, 0x77, 0x11),
                      (0x00, 0x77, 0xbb),
                      (0x88, 0x77, 0x66),
                      (0xcc, 0xcc, 0x33),
                      (0x66, 0xcc, 0xdd),
                      (0xaa, 0x77, 0x55),
                      (0xff, 0xff, 0xff),]

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


# Plane activation for each color in the palette.
# Which bit is active there
PLANE_COLORS = [(1, 3, 5, 7, 9, 0xb, 0xd, 0xf),
                (2, 3, 6, 7, 0xa, 0xb, 0xe, 0xf),
                (4, 5, 6, 7, 0xc, 0xd, 0xe, 0xf),
                (8, 9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf)]


def encode(filename, dest_disk=DEST_DISK):
    """Encode an image file as GEM and reinsert it."""
    just_filename = filename.split('.')[0]
    gem_filename = just_filename + '.GEM'

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
            print(p)
            f.write(p)

        row_cursor = 0
        starting_row_cursor = 0

        for i, pattern in enumerate(unique_patterns):
            row_cursor = starting_row_cursor
            chain_count = 0
            print("Start pattern %s. row_cursor: %s" % (pattern, row_cursor))
            for loc in pattern_locations[pattern]:
                if pattern == unique_patterns[0] and loc == 0:
                    row_cursor += 1
                    row_cursor %= total_rows
                    continue

                if loc == row_cursor:
                    chain_count += 1
                else:
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
                        print("Ultra skip: %s %s %s, row_cursor after: %s" % (hex(first_byte), hex(second_byte), hex(third_byte), row_cursor))

                    elif loc - row_cursor >= 63:
                        first_byte = 0xc0 + ((loc - row_cursor) + 1) // 256
                        second_byte = ((loc - row_cursor) + 1) % 256
                        f.write(first_byte.to_bytes(1, byteorder='little'))
                        f.write(second_byte.to_bytes(1, byteorder='little'))

                        if loc == pattern_locations[pattern][0]:
                            starting_row_cursor = loc
                        row_cursor = loc
                        print("Far skip: %s %s, row_cursor after: %s" % (hex(first_byte), hex(second_byte), row_cursor))
                        assert row_cursor == loc
                    elif loc - row_cursor < 63:
                        skip_and_write_code = 0x81 + ((loc - row_cursor) % total_rows)
                        if loc == pattern_locations[pattern][0]:
                            starting_row_cursor = loc
                        f.write(skip_and_write_code.to_bytes(1, byteorder='little'))
                        print("Short skip: %s, row_cursor after: %s" % (hex(skip_and_write_code), row_cursor))
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
    pix = img.load()

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

# TMAP00 is used: ??