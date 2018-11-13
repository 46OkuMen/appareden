"""
    Utilities for encoding images as .GEM files, as used in Appareden.
    Possibly useful for other TGL/GIGA games, but would need less hard-coding in the palettes.
"""

from romtools.disk import Disk
from rominfo import DEST_DISK, DEST_CD_DISK
from PIL import Image, ImageDraw
from bitstring import BitArray
from shutil import copyfile

FILES_TO_ENCODE = ['TMAP_00.png', 'TMAP_00A.png', 'TMAP_01A.png', 'TMAP_01B.png', 'TMAP_03A.png', 'TMAP_06A.png',
                   'TMAP_10B.png', 'TMAP_11A.png', 'TMAP_12B.png', 'TMAP_14A.png', "TMAP_16B.png",
                   'TMAP_27A.png', 'TMAP_29B.png', 'TMAP_32A.png',
                   'ORTITLE.png', 'GENTO.png', 'BENIMARU.png', 'HANZOU.png', 'TAMAMO.png', 'GOEMON.png',
                   'HEILEE.png', 'SHIROU.png', 'MEIRIN.png', 'GENNAI.png', 'OUGI.png',
                   'GENNAIJ.png', 'GOEMONJ.png', 'SHIROUJ.png', 'HANZOJ.png',
                   'TEFF_00A.png', 'TEFF_01A.png', 'TEFF_02A.png', 'TEFF_03A.png', 'TEFF_04A.png', 'TEFF_05A.png',
                   'TEFF_06A.png', 'TEFF_07A.png', 'TEFF_08A.png', 'TEFF_09A.png', 'TEFF_0AA.png', 'TEFF_0BA.png',
                   'OP_02B.png', 'TEFF_12A.png', 'TEFF_13A.png', 'TEFF_15A.png', 'TEFF_16A.png', 'TEFF_17A.png',
                   'CHAR_32A.png', 'CHAR_43A.png', 'OP_02C.png', 'OP_04B.png', 'OP_07B.png',
                   'SFCHR_99.png'
                   ]
TILED_TEFFS = ['TEFF_00A.png', 'TEFF_02A.png', 'TEFF_04A.png', 'TEFF_06A.png', 'TEFF_07A.png', 'TEFF_08A.png',
               'TEFF_0AA.png', 'TEFF_12A.png']
SINGLE_SPRITE_TEFFS = ['TEFF_01A.png', 'TEFF_03A.png', 'TEFF_05A.png', 'TEFF_09A.png', 'TEFF_0BA.png',
                       'TEFF_13A.png', 'TEFF_15A.png', 'TEFF_16A.png', 'TEFF_17a.png']

MANUAL_SPZS = ["SFCHR_99.SPZ"]

class Palette:
    def __init__(self, palette_string):
        self.string = palette_string
        self.colors = self._string_to_rgb(palette_string)

    def _string_to_rgb(self, palette_string):
        result = []
        palette_hex = palette_string.hex()
        for _ in range(16):
            r = int(palette_hex[1], 16) * 0x11
            g = int(palette_hex[2], 16) * 0x11
            b = int(palette_hex[0], 16) * 0x11
            result.append((r, g, b))
            palette_hex = palette_hex[3:]
        return result

# Some are longer than others - has something to do with spritesheets.
NAMETAG_PALETTE = b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xfb\xac\xb9\xfd\x80\x21\x57\xd0\x66\x87\x3a\xcf\x8b\xff\xff\xff\x00'
MAP_PALETTE =     b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xeb\xac\xb9\xfd\x60\x31\x77\xb0\x76\x87\x3c\xcd\x6c\x6a\x7f\xff\x00'
SHIP_PALETTE =    b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xfb\xac\xb9\xfd\x60\x31\x77\xb0\x76\x87\x3c\xcd\x6c\xda\xcf\xff\x00'
OP_PALETTE =      b'\x00\x04\x22\x63\x40\xd0\x38\x32\x95\x76\x6c\x55\x4b\x79\x88\x6d\x97\xfc\xec\xdb\xfd\xee\xef\xff\x00'
TITLE_PALETTE =   b'\x00\x01\x11\x38\x40\xD4\x5C\x94\xFC\xAC\xB9\xEC\x80\x21\x57\xE1\x76\x87\x29\xBC\x7C\xFF\xFF\xFF\x00'
TEFF_PALETTE =    b'\x00\x03\x33\x38\x40\xf4\x4d\x94\xfb\xac\xb9\xfd\x80\x21\x57\xd0\x66\x87\x3a\xcf\x8b\xa6\xaf\xff\x32\x33\x00'
OP_TEXT_PALETTE = b'\x00\x02\x32\x26\x32\xc6\x8e\xa9\xfb\xbf\xda\xcb\x79\x84\x54\x19\x11\xd1\xf2\x8b\x55\xf0\xdf\xff\x00'
SFCHR_PALETTE =   b'\x00\x03\x33\x49\x52\xF5\x3C\x93\xEB\xAC\xB9\xFD\x80\x21\x77\xD0\x66\x87\x3C\xCF\x8B\xFB\xEF\xFF\x35\x36\x33\x00'

def edit(string, loc, replacement):
    return string[:loc] + replacement + string[loc+1:]

def get_closest_color_index(palette, rgb):
    hammings = [255]*16
    for i, color in enumerate(palette):
        hamming = 0
        for val in range(3):
            hamming += abs(color[val] - rgb[val])
        hammings[i] = hamming
    return hammings.index(min(hammings))


NAMETAG_PALETTE_IMAGES = ['BENIMARU', 'GENNAI', 'GENTO', 'HANZOU', 'HEILEE',
                          'MEIRIN', 'OUGI', 'TAMAMO', 'GOEMON', 'SHIROU',
                          'CHAR_32A', 'CHAR_43A']
MAP_PALETTE_IMAGES = ['TMAP_00', 'TMAP_00A', 'TMAP_01A', 'TMAP_01B',
                      'TMAP_03A', 'TMAP_06A', 'TMAP_10B', 'TMAP_11A',
                      'TMAP_12B', 'TMAP_14A', 'TMAP_16B', 'TMAP_27A',
                      'TMAP_29B']
SHIP_PALETTE_IMAGES = ['TMAP_32A']
TITLE_PALETTE_IMAGES = ['ORTITLE', 'GENNAIJ', 'GOEMONJ', 'HANZOJ', 'SHIROUJ']

OP_PALETTE_IMAGES = ['OP_02B', 'OP_02C']
OP_TEXT_PALETTE_IMAGES = ['OP_04B', 'OP_07B']

TEFF_PALETTE_IMAGES = ['TEFF_00A', 'TEFF_0AA', 'TEFF_0BA', 'TEFF_01A', 'TEFF_02A', 'TEFF_03A', 'TEFF_04A', 'TEFF_05A',
                       'TEFF_06A', 'TEFF_07A', 'TEFF_08A', 'TEFF_09A', 'TEFF_12A', 'TEFF_13A', 'TEFF_15A',
                       'TEFF_16A', 'TEFF_17A',]

SFCHR_PALETTE_IMAGES = ['SFCHR_99',]

# Plane activation for each color in the palette.
# Which bit is active there
PLANE_COLORS = [(1, 3, 5, 7, 9, 0xb, 0xd, 0xf),
                (2, 3, 6, 7, 0xa, 0xb, 0xe, 0xf),
                (4, 5, 6, 7, 0xc, 0xd, 0xe, 0xf),
                (8, 9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf)]


def encode(filename):
    """Encode an image file as GEM and reinsert it."""
    just_filename = filename.split('.')[0]
    gem_filename = just_filename.replace('img_edited', 'patched') + '.GEM'

    unpathed_filename = just_filename.split('/')[-1]

    # "Polymorphism"
    if unpathed_filename in NAMETAG_PALETTE_IMAGES:
        print("Using nametag palette")
        palette = Palette(NAMETAG_PALETTE)
    elif unpathed_filename in MAP_PALETTE_IMAGES:
        print("Using map palette")
        palette = Palette(MAP_PALETTE)
    elif unpathed_filename in SHIP_PALETTE_IMAGES:
        print("Using ship palette")
        palette = Palette(SHIP_PALETTE)
    elif unpathed_filename in TITLE_PALETTE_IMAGES:
        print("Using title palette")
        palette = Palette(TITLE_PALETTE)
    elif unpathed_filename in TEFF_PALETTE_IMAGES:
        print("Using text effect palette")
        palette = Palette(TEFF_PALETTE)
    elif unpathed_filename in OP_PALETTE_IMAGES:
        print("Using OP palette")
        palette = Palette(OP_PALETTE)
    elif unpathed_filename in OP_TEXT_PALETTE_IMAGES:
        print("Using OP text palette")
        palette = Palette(OP_TEXT_PALETTE)
    elif unpathed_filename in SFCHR_PALETTE_IMAGES:
        print("Using SFCHR palette")
        palette = Palette(SFCHR_PALETTE)
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
                        palette_index = palette.colors.index(p)
                    except ValueError:
                        palette_index = get_closest_color_index(palette.colors, p)
                    pattern.append(palette_index in PLANE_COLORS[plane])

            pattern = BitArray(pattern).bytes

            if pattern in unique_patterns:
                pattern_locations[pattern].append(row_cursor)
            else:
                unique_patterns.append(pattern)
                pattern_locations[pattern] = [row_cursor,]

            row_cursor += 1

    IMAGE_DATA_LOCATION = 0x10 + len(palette.string) + (len(unique_patterns)*4)

    with open(gem_filename, 'wb') as f:
        f.write(b'Gem')
        f.write(b'\x02\x04\x00\x0e\x00')
        f.write(b'\x30\x00') # not sure what these bytes do. 18 for nametag, 30 for teff, doesn't seem to matter
        f.write(height.to_bytes(2, byteorder='little'))
        f.write(IMAGE_DATA_LOCATION.to_bytes(2, byteorder='little'))
        f.write(b'\x00\x00') # not sure about these either
        f.write(palette.string)
        for p in unique_patterns:
            #print(p)
            f.write(p)

        row_cursor = 0
        starting_row_cursor = 0

        for i, pattern in enumerate(unique_patterns):
            row_cursor = starting_row_cursor
            chain_count = 0
            #print("Start pattern %s. row_cursor: %s" % (pattern, row_cursor))
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

            f.write(b'\x00')
            starting_row_cursor += 1
            starting_row_cursor %= total_rows

        f.write(b'\x00'*80)  # for good measure. TODO: Still necessary?

    copyfile(gem_filename, gem_filename.replace('patched', 'patched_CD'))

    # Reinsert into both disks
    try:
        d = Disk(DEST_DISK)
        d.insert(gem_filename, path_in_disk='TGL/OR')
    except:
        print("That file isn't on this disk")

    cd = Disk(DEST_CD_DISK)
    cd.insert(gem_filename, path_in_disk='TGL/OR')


def write_spz(filename, single_sprite=False):
    """Write a SPZ sprite-sheet-spec for an image, with n sprites."""
    just_filename = filename.split('.')[0]
    spz_filename = just_filename.replace('img_edited', 'patched') + '.SPZ'
    png_filename = just_filename + '.PNG'
    print(just_filename, spz_filename, png_filename)

    img = Image.open(png_filename)
    width, _ = img.size
    # Number of sprites: width / 64
    n = width // 64
    print(filename, width, "n = ", n)

    # There's a limit of 7 sprites for the drop-in spell displays, and 24 tiles total.
    # Squish multiple letters into a 32x32 sprite if necessary.

    with open(spz_filename, 'wb') as f:
        f.write(b'FSPR')
        if single_sprite:
            tiles_per_sprite = n*4
            f.write(b'\x01\x00')
        else:
            tiles_per_sprite = 4
            f.write(n.to_bytes(2, byteorder='little'))

        just_filename = just_filename.split('/')[-1]
        f.write(bytes(just_filename, encoding='ascii'))
        f.write(b'\x00'*0x12)

        top_cursor = 0
        bottom_cursor = n*2
        pointer_start = 0x20 + (n*2)

        for sprite in range(n):
            f.write(pointer_start.to_bytes(2, byteorder='little'))
            pointer_start += 0xf

        if single_sprite:
            tiles_per_sprite = n * 4
            f.write(tiles_per_sprite.to_bytes(1, byteorder='little'))
            f.write(b'\x14\x13')

            col = 0x13
            row = 0x44

            for _ in range(tiles_per_sprite // 2):
                f.write(col.to_bytes(1, 'little'))
                f.write(row.to_bytes(1, 'little'))
                f.write(top_cursor.to_bytes(1, 'little'))
                top_cursor += 1
                col += 1

            col = 0x13
            row = 0x48
            for _ in range(tiles_per_sprite // 2):
                f.write(col.to_bytes(1, 'little'))
                f.write(row.to_bytes(1, 'little'))
                f.write(bottom_cursor.to_bytes(1, 'little'))
                bottom_cursor += 1
                col += 1

        else:
            for sprite in range(n):
                # Don't pull this out of the loop! It needs to be written for every /sprite/.
                f.write(tiles_per_sprite.to_bytes(1, byteorder='little'))     # number of 16x16 tiles in sprite

                # TODO:  Write \x13\x44, etc. with a loop based on tiles_per_sprite.
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
                bottom_cursor += 1

    copyfile(spz_filename, spz_filename.replace('patched', 'patched_CD'))

    try:
        d = Disk(DEST_DISK)
        d.insert(spz_filename, path_in_disk='TGL/OR')
    except:
        print("That file isn't on this disk")

    cd = Disk(DEST_CD_DISK)
    cd.insert(spz_filename, path_in_disk='TGL/OR')

def get_tile(img, n):
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
    dest_img_draw = ImageDraw.Draw(dest_img)

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
            #print(tile)

            print("Tile: " + str(tile_marker))

            #tile_xs.append(x_marker)
            #tile_ys.append(y_marker)

            tile_x = (x_marker - 9) * 16
            tile_y = (y_marker - 0x44) * 4

            #print(tile_x)

            if sprite_width < tile_x:
                sprite_width = tile_x

            dest_img.paste(tile, (tile_x + dest_x, tile_y + dest_y))

            if tile_constant == 0:
                tile_color = (255, 0, 0, 0)
            elif tile_constant == 256:
                tile_color = (0, 255, 0, 0)
            elif tile_constant == 512:
                tile_color = (0, 0, 255, 0)
            tile_name = hex(tile_marker)[2:]
            #tile_name = "%s %s" % (tile_x, tile_y)
            dest_img_draw.text((tile_x+dest_x, tile_y+dest_y), tile_name, fill=tile_color)


        dest_img_draw.text((tile_x + dest_x - 32, tile_y + dest_y + 32), "Sprite %s" % (hex(i)[2:]), fill=(255, 0, 0, 0))
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

    #for f in FILES_TO_ENCODE:
    #    f = 'img_edited/' + f
    #    encode(f)

    #for teff in TILED_TEFFS:
    #    teff = 'img_edited/' + teff
    #    write_spz(teff)

    #for teff in SINGLE_SPRITE_TEFFS:
    #    teff = 'img_edited/' + teff
    #    write_spz(teff, single_sprite=True)

    for spz in MANUAL_SPZS:
        with open('original/OR/%s' % spz, 'rb') as f:
            contents = f.read()

        # Do edits

        # 1 Round -> Round 1
        contents = edit(contents, 0x932, b'\x19')
        contents = edit(contents, 0x935, b'\x1a')
        contents = edit(contents, 0x938, b'\x1b')
        contents = edit(contents, 0x93b, b'\x1c')
        contents = edit(contents, 0x93e, b'\x1d')
        contents = edit(contents, 0x941, b'\x1e')

        contents = edit(contents, 0x95c, b'\x19')
        contents = edit(contents, 0x95f, b'\x1a')
        contents = edit(contents, 0x962, b'\x1b')
        contents = edit(contents, 0x965, b'\x1c')
        contents = edit(contents, 0x968, b'\x1d')
        contents = edit(contents, 0x96b, b'\x1e')




        # Gen______to -> Gento
        contents = edit(contents, 0xc1d, b'\x13')
        contents = edit(contents, 0xc20, b'\x14')
        contents = edit(contents, 0xc29, b'\x13')
        contents = edit(contents, 0xc2c, b'\x14')
        contents = edit(contents, 0xc35, b'\x13')
        contents = edit(contents, 0xc38, b'\x14')



        with open('patched/%s' % spz, 'wb') as f:
            f.write(contents)

        copyfile('patched/%s' % spz, 'patched_CD/%s' % spz)

        # Reinsert into both disks
        try:
            d = Disk(DEST_DISK)
            d.insert('patched/%s' % spz, path_in_disk='TGL/OR')
        except:
            print("That file isn't on this disk")

        cd = Disk(DEST_CD_DISK)
        cd.insert('patched_CD/%s' % spz, path_in_disk='TGL/OR')



    # decode_spz('SFCHR_98.SPZ', 'SFCHR_98.png')
    # decode_spz('TEFF_00A.SPZ', 'TEFF_00A.png')   # Simple and already documented
    #decode_spz('original/OR/NRCHR_99.SPZ', 'img_original/NRCHR_99_background1.png' )    # Much more complex
    # decode_spz('CHAR_32A.SPZ', 'CHAR_32A.png')
