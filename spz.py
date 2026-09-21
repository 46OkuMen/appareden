"""
    Reader/writer for TGL's .SPZ sprite tables (the sprites cut out of a .GEM
    tile sheet), taken from NEKORUN.EXE's sprite drawer (1C09:3F9D under
    np2core) rather than from experiments.

    Layout
        00  "FSPR"
        04  word: number of sprites N
        06  name of the .GEM, zero-padded to 0x20
        20  N words: file offset of each sprite record
        ..  sprite records

    Sprite record
        00  tile count
        01  hotspot X, in 16-pixel units
        02  hotspot Y, in 16-pixel units
        03  3 bytes per tile:
              x   column, 16-pixel units (sprite X = x - hotspot X)
              yb  row = yb >> 2 (16-pixel units), bank = yb & 3
              t   tile index low byte; tile = bank * 256 + t

    Tiles are 16x16 cells of the .GEM sheet, numbered row by row
    (40 per row on a 640-pixel sheet). The game cuts them out with a mask
    plane built from the GEM's transparent color.
"""

from dataclasses import dataclass, field

TILE = 16


@dataclass
class Sprite:
    hx: int
    hy: int
    tiles: list = field(default_factory=list)     # [(x, y, tile)] x/y in tile units

    def bounds(self):
        xs = [x for x, _, _ in self.tiles]
        ys = [y for _, y, _ in self.tiles]
        return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def parse(data):
    assert data[:4] == b"FSPR", data[:4]
    n = int.from_bytes(data[4:6], "little")
    name = data[6:0x20].split(bytes(1))[0].decode("ascii")
    offsets = [int.from_bytes(data[0x20 + 2 * i:0x22 + 2 * i], "little") for i in range(n)]
    sprites = []
    for o in offsets:
        count, hx, hy = data[o], data[o + 1], data[o + 2]
        tiles = []
        for k in range(count):
            x, yb, t = data[o + 3 + 3 * k:o + 6 + 3 * k]
            tiles.append((x, yb >> 2, ((yb & 3) << 8) | t))
        sprites.append(Sprite(hx, hy, tiles))
    return name, offsets, sprites


def build(name, sprites, share=True):
    """Serialize sprites. Identical records are stored once (the originals
    do the same, e.g. a glyph used twice)."""
    n = len(sprites)
    head = b"FSPR" + n.to_bytes(2, "little") + name.encode("ascii")
    head = head.ljust(0x20, b"\0")
    body = bytearray()
    offsets = []
    seen = {}
    base = 0x20 + 2 * n
    for s in sprites:
        rec = bytes([len(s.tiles), s.hx, s.hy])
        for x, y, tile in s.tiles:
            assert 0 <= tile < 1024 and 0 <= y < 64 and 0 <= x < 256
            rec += bytes([x, (y << 2) | (tile >> 8), tile & 0xFF])
        if share and rec in seen:
            offsets.append(seen[rec])
            continue
        seen[rec] = base + len(body)
        offsets.append(base + len(body))
        body += rec
    return head + b"".join(o.to_bytes(2, "little") for o in offsets) + bytes(body)


def tile_box(tile, sheet_width=640):
    per_row = sheet_width // TILE
    return ((tile % per_row) * TILE, (tile // per_row) * TILE)


def render(sprite, sheet, background=(255, 0, 255)):
    """Draw a sprite from an RGBA/RGB sheet image (transparent pixels = alpha 0
    or the background color). Returns (image, (ox, oy)) where (ox, oy) is the
    hotspot's position inside the image."""
    from PIL import Image
    x0, y0, x1, y1 = sprite.bounds()
    img = Image.new("RGBA", ((x1 - x0) * TILE, (y1 - y0) * TILE), background + (255,))
    for x, y, tile in sprite.tiles:
        sx, sy = tile_box(tile, sheet.width)
        cell = sheet.crop((sx, sy, sx + TILE, sy + TILE)).convert("RGBA")
        img.alpha_composite(cell, ((x - x0) * TILE, (y - y0) * TILE))
    return img, ((sprite.hx - x0) * TILE, (sprite.hy - y0) * TILE)
