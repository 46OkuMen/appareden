"""
    Utilities for encoding images as .GEM files, as used in Appareden.
    Possibly useful for other TGL/GIGA games, but would need less hard-coding in the palettes.
"""

import os
from romtools.disk import Disk
from rominfo import SRC_DISK, DEST_DISK, DEST_CD_DISK
from PIL import Image, ImageDraw
from shutil import copyfile
import gem_codec
import nrchr_text

SRC_CD_DISK = os.path.join('original_CD', 'Appareden (CD-UPDATED).hdi')
PRISTINE_CACHE = os.path.join('original', 'pristine')

FILES_TO_ENCODE = ['TMAP_00.png',
                   # These used to be left out: the old encoder made them bigger than the
                   # 64KB EMS page frame ORFIELD loads tilesets into. gem_codec gets them
                   # under their original sizes.
                   'TMAP_00A.png', 'TMAP_10B.png', 'TMAP_12B.png',
                   'TMAP_01A.png',
                   'TMAP_01B.png', 'TMAP_03A.png', 'TMAP_06A.png',
                   'TMAP_11A.png', 'TMAP_14A.png', "TMAP_16B.png",
                   'TMAP_27A.png', 'TMAP_29B.png',
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

MANUAL_SPZS = ['SFCHR_99.SPZ']

# Images redrawn against a different palette than their original file's.
# Everything else uses its original GEM's palette.
TITLE_PALETTE =   b'\x00\x01\x11\x38\x40\xD4\x5C\x94\xFC\xAC\xB9\xEC\x80\x21\x57\xE1\x76\x87\x29\xBC\x7C\xFF\xFF\xFF'
OP_TEXT_PALETTE = b'\x00\x02\x32\x26\x32\xc6\x8e\xa9\xfb\xbf\xda\xcb\x79\x84\x54\x19\x11\xd1\xf2\x8b\x55\xf0\xdf\xff'
PALETTE_OVERRIDES = {
    'GENNAIJ': TITLE_PALETTE, 'GOEMONJ': TITLE_PALETTE,
    'HANZOJ': TITLE_PALETTE, 'SHIROUJ': TITLE_PALETTE,
    'OP_07B': OP_TEXT_PALETTE,
}

def edit(string, loc, replacement):
    return string[:loc] + replacement + string[loc+1:]


def pristine(filename, src_disk):
    """A file as it is on the untouched source disk image (cached under
    original/pristine/). The loose copies in original/OR and original/CD
    can't be trusted: some were overwritten during 2018 experiments
    (CHAR_43A.GEM and OP_04B.GEM had their transparent color edited,
    NRCHR_99.GEM was re-encoded, SCN12307.COD was blanked)."""
    tag = 'FD' if src_disk == SRC_DISK else 'CD'
    d = os.path.join(PRISTINE_CACHE, tag)
    path = os.path.join(d, filename.upper())
    if not os.path.exists(path):
        os.makedirs(d, exist_ok=True)
        try:
            Disk(src_disk).extract(filename.upper(), path_in_disk='TGL/OR', dest_path=d)
        except Exception:
            return None
    with open(path, 'rb') as f:
        return f.read()


TARGETS = [(SRC_DISK, 'patched', DEST_DISK),
           (SRC_CD_DISK, 'patched_CD', DEST_CD_DISK)]


def encode(filename):
    """Encode an edited image as GEM and reinsert it into both disks.

    Each disk's version is encoded against that disk's original GEM, taken
    from the untouched source disk image: the original supplies the palette
    (unless overridden) and transparent color, and unedited pixels keep their
    original palette indices exactly. See gem_codec.py for the format."""
    name = os.path.splitext(os.path.basename(filename))[0].upper()
    img = Image.open(filename)

    for src_disk, out_dir, disk in TARGETS:
        original = pristine(name + '.GEM', src_disk)
        if original is None:
            print("%s: not on %s" % (name, disk))
            continue
        data, stats = gem_codec.encode_edit(original, img, PALETTE_OVERRIDES.get(name))
        if len(data) > gem_codec.MAX_TMAP_SIZE and name.startswith('TMAP'):
            raise Exception("%s is %d bytes; ORFIELD loads tilesets into a 64KB EMS "
                            "page frame" % (name, len(data)))
        gem_filename = os.path.join(out_dir, name + '.GEM')
        with open(gem_filename, 'wb') as f:
            f.write(data)
        print("%s: %d bytes (original %d), %d pixels quantized" % (gem_filename, len(data),
                                                                   len(original), stats['quantized']))
        Disk(disk).insert(gem_filename, path_in_disk='TGL/OR')


def encode_nekorun_text():
    """Neko Run's three Japanese text sprites in NRCHR_99 -> English
    (nrchr_text.py renders the art and repacks the sheet and its SPZ)."""
    for src_disk, out_dir, disk in TARGETS:
        gem, spz_bytes, report = nrchr_text.build(pristine('NRCHR_99.GEM', src_disk),
                                                  pristine('NRCHR_99.SPZ', src_disk))
        for ext, data in (('GEM', gem), ('SPZ', spz_bytes)):
            path = os.path.join(out_dir, 'NRCHR_99.' + ext)
            with open(path, 'wb') as f:
                f.write(data)
            Disk(disk).insert(path, path_in_disk='TGL/OR')
        print("%s: NRCHR_99 %s" % (out_dir, report))


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
                # Red
                tile_color = (255, 0, 0, 0)
            elif tile_constant == 256:
                # Green
                tile_color = (0, 255, 0, 0)
            elif tile_constant == 512:
                # Blue
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

    for f in FILES_TO_ENCODE:
        f = 'img_edited/' + f
        encode(f)

    encode_nekorun_text()

    for teff in TILED_TEFFS:
        teff = 'img_edited/' + teff
        write_spz(teff)

    for teff in SINGLE_SPRITE_TEFFS:
        teff = 'img_edited/' + teff
        write_spz(teff, single_sprite=True)

    for spz in MANUAL_SPZS:
        contents = pristine(spz, SRC_DISK)
         # Do edits
         # 1 Round -> Round 1
        """
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
        """

        # 2 Round starts: 0x995?
        # 87 88 89
        # aa a9 aa

        #contents = edit(contents, 0x996, )

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
     #decode_spz('TEFF_00A.SPZ', 'TEFF_00A.png')   # Simple and already documented
    #decode_spz('original/OR/SFCHR_99.SPZ', 'img_original/SFCHR_99_background01.png' )    # Much more complex
    # decode_spz('CHAR_32A.SPZ', 'CHAR_32A.png')