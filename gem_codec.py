"""
    Exact decoder and size-optimizing encoder for TGL's .GEM image format.

    The format was taken from the game's own decoder (ORTITLE.EXE, the routine
    at 1AD0:0237 when running under np2core) rather than from experiments, so
    every opcode below is what the game actually does. Nothing here is
    Appareden-specific; the palettes etc. live in gem.py.

    Layout
        00  "Gem"
        03  version (2)
        04  number of planes (4)
        05  0 (nonzero makes the decoder reuse one pattern forever; unused)
        06  word: transparent color index, or 0xFFFF for none. A transparent
            pixel leaves VRAM untouched (the GRCG writes in RMW mode with a
            per-pixel mask).
        08  word: width in bytes (width / 8). The decoder itself ignores it.
        0A  word: height in pixels
        0C  dword: file offset of the command stream
        10  palette: 16 colors in 24 bytes (two colors per 3 bytes, see below)
        28  a zero-terminated run of junk bytes (usually just the 00)
        ..  pattern table: 4 bytes (one per plane) per 8-pixel row
        ..  command stream, up to the offset at 0C

    Drawing
        The image is a column-major sequence of 8-pixel rows: position
        pos = col * height + row, col = x // 8. A cursor walks forward
        through the positions (it can never move back).

        Pattern 0 is written at position 0 before any command runs. Every
        other pattern starts with the cursor at the position of the *first
        write of the previous pattern*. So the pattern table must be ordered
        by first occurrence.

        Opcodes dispatch on the highest set bit T of the byte b. The count n
        comes from the low bits L = b & (T-1):
            L == 0             -> n = next two bytes, big-endian
            L & (T >> 1)       -> n = ((L ^ (T >> 1)) << 8) | next byte
            otherwise          -> n = L
        (For T=1, L is always 0.)

            00        end of pattern: load the next pattern and move the
                      cursor back to its start. 00 00 ends the image.
            80-FF     move n rows, write once                (skip)
            40-7F     n times: move 1 row, write              (repeat)
            20-3F     n times: move 2 rows, write             (repeat, step 2)
            10-1F,
            01-07     n times: move 4 rows, write             (repeat, step 4)
            08-0F     move 1, write the current pattern; then n-1 times:
                      load the next pattern, move 1, write. The pattern then
                      ends as if a 00 followed.                (literal run)

        n = 0 means 65536 in the repeat loops; the encoder never emits it.
"""

from collections import Counter

TRANSPARENT_NONE = 0xFFFF


# --------------------------------------------------------------------------
# Palette packing: 3 bytes per two colors, nibbles B1 R1 | G1 B2 | R2 G2
# (i.e. color 0 = (R, G, B) from nibbles (b0 low, b0 high, b1 high)).
# --------------------------------------------------------------------------

def unpack_palette(pal24):
    colors = []
    for i in range(8):
        a, b, c = pal24[i * 3:i * 3 + 3]
        # Two 12-bit colors, stored as nibbles B R G, B R G.
        n = [a >> 4, a & 15, b >> 4, b & 15, c >> 4, c & 15]
        for bb, rr, gg in (n[0:3], n[3:6]):
            colors.append((rr * 17, gg * 17, bb * 17))
    return colors


def pack_palette(colors):
    """colors: 16 (r, g, b) tuples with 0-255 components (rounded to 4 bits)."""
    n = []
    for r, g, b in colors:
        n += [round(b / 17), round(r / 17), round(g / 17)]
    return bytes((n[i] << 4) | n[i + 1] for i in range(0, 48, 2))


# --------------------------------------------------------------------------
# Decoder
# --------------------------------------------------------------------------

class GemHeader:
    def __init__(self, data):
        if data[:3] != b'Gem' or data[3] != 2:
            raise ValueError("not a GEM v2 file")
        self.planes = data[4]
        self.flag5 = data[5]
        self.transparent = int.from_bytes(data[6:8], 'little')
        self.width_bytes = int.from_bytes(data[8:10], 'little')
        self.height = int.from_bytes(data[0xA:0xC], 'little')
        self.cmd_offset = int.from_bytes(data[0xC:0x10], 'little')
        self.palette_bytes = data[0x10:0x28]
        p = 0x28
        while data[p] != 0:
            p += 1
        self.junk = data[0x28:p]
        self.pattern_offset = p + 1
        self.n_patterns = (self.cmd_offset - self.pattern_offset) // self.planes


def _count(data, i, b, top):
    """Decode the count of opcode byte b (highest bit top); i points after b."""
    low = b & (top - 1)
    if low == 0:
        return (data[i] << 8) | data[i + 1], i + 2
    half = top >> 1
    if low & half:
        return ((low ^ half) << 8) | data[i], i + 1
    return low, i


def decode_commands(data, hdr=None):
    """Run the command stream. Returns (writes, end_offset, stats) where writes
    is a list of (position, pattern_index) in the order the game draws them."""
    if hdr is None:
        hdr = GemHeader(data)
    writes = [(0, 0)]
    pat = 0
    pos = 0
    saved = 0
    flag = True          # [133F]: "start position of this pattern already saved"
    i = hdr.cmd_offset
    stats = Counter()

    def move(n):
        nonlocal pos, saved, flag
        pos += n
        if not flag:
            saved = pos
            flag = True

    while True:
        b = data[i]
        i += 1
        if b == 0:
            stats['end'] += 1
            if data[i] == 0:
                return writes, i + 1, stats
            pat += 1
            pos = saved
            flag = False
            continue
        top = 0x80
        while not (b & top):
            top >>= 1
        n, i = _count(data, i, b, top)
        if top == 0x80:
            stats['skip'] += 1
            move(n)
            writes.append((pos, pat))
        elif top == 0x08:
            stats['run'] += 1
            for k in range(n or 0x10000):
                if k:
                    pat += 1
                move(1)
                writes.append((pos, pat))
                flag = False
            # falls into the 00 handler without consuming a byte
            if data[i] == 0:
                return writes, i + 1, stats
            pat += 1
            pos = saved
            flag = False
        else:
            step = {0x40: 1, 0x20: 2}.get(top, 4)
            stats['rep%d' % step] += 1
            for _ in range(n or 0x10000):
                move(step)
                writes.append((pos, pat))


def decode(data):
    """Decode a GEM to (width, height, palette_rgb, pixels, transparent) where
    pixels is a list of rows of palette indices, or None for pixels never
    written / written transparent."""
    hdr = GemHeader(data)
    writes, end, _ = decode_commands(data, hdr)
    h = hdr.height
    npos = max(p for p, _ in writes) + 1
    cols = max(-(-npos // h), hdr.width_bytes)
    width = cols * 8
    pix = [[None] * width for _ in range(h)]
    po = hdr.pattern_offset
    for pos, pat in writes:
        col, row = divmod(pos, h)
        planes = data[po + pat * hdr.planes: po + (pat + 1) * hdr.planes]
        for x in range(8):
            bit = 0x80 >> x
            c = 0
            for pl in range(hdr.planes):
                if planes[pl] & bit:
                    c |= 1 << pl
            if c == hdr.transparent:
                continue
            pix[row][col * 8 + x] = c
    return width, h, unpack_palette(hdr.palette_bytes), pix, hdr.transparent


def to_image(data, background=(0x00, 0x77, 0x88)):
    from PIL import Image
    w, h, pal, pix, _ = decode(data)
    img = Image.new('RGB', (w, h), background)
    px = img.load()
    for y in range(h):
        for x in range(w):
            c = pix[y][x]
            if c is not None:
                px[x, y] = pal[c]
    return img


# --------------------------------------------------------------------------
# Encoder
# --------------------------------------------------------------------------

def _count_bytes(opbase, top, n):
    """Encode opcode family (opbase = top bit value, e.g. 0x40) with count n.
    Returns bytes, choosing the shortest form."""
    half = top >> 1
    if top > 1 and 1 <= n < half and not (n & half) and (top > 2 or n == 1):
        # short form: L = n, must be nonzero and not have the half bit
        return bytes([opbase | n])
    if top > 1 and n < (half << 8) and half:
        hi = n >> 8
        return bytes([opbase | half | hi, n & 0xFF])
    return bytes([opbase, n >> 8, n & 0xFF])


def op_skip(n):
    assert 1 <= n <= 0xFFFF
    return _count_bytes(0x80, 0x80, n)


def op_rep(step, n):
    assert 1 <= n <= 0xFFFF
    if step == 1:
        return _count_bytes(0x40, 0x40, n)
    if step == 2:
        return _count_bytes(0x20, 0x20, n)
    # step 4: 0x10 family (1..7, 2-byte up to 0x7FF) or 0x05 (1).
    return _count_bytes(0x10, 0x10, n)


def op_run(n):
    assert 1 <= n <= 0xFFFF
    return _count_bytes(0x08, 0x08, n)


SKIP_COST = [0] + [1] * 63 + [2] * (0x4000 - 64)      # index n < 0x4000
def skip_cost(n):
    return SKIP_COST[n] if n < 0x4000 else 3

REP_LIMITS = {1: (31, 0x1FFF), 2: (15, 0xFFF), 4: (7, 0x7FF)}
def rep_cost(step, n):
    a, b = REP_LIMITS[step]
    return 1 if n <= a else 2 if n <= b else 3

def run_cost(n):
    return 1 if n <= 3 else 2 if n <= 0x3FF else 3


def _row_patterns(width, height, idx, planes=4):
    """Column-major list of 4-byte plane patterns for every 8-pixel row."""
    pats = []
    for col in range(width // 8):
        x0 = col * 8
        for y in range(height):
            row = idx[y]
            p = [0] * planes
            for x in range(8):
                c = row[x0 + x]
                bit = 0x80 >> x
                for pl in range(planes):
                    if c >> pl & 1:
                        p[pl] |= bit
            pats.append(bytes(p))
    return pats


def _pattern_plan(start, req):
    """Cheapest command sequence that writes every position in req (sorted,
    all > start) moving forward from cursor `start`.

    Returns (dp, back): dp[t] = cost to have written req[:t] with the cursor on
    req[t-1] (t=0: cursor on start); back[t] = (prev t, op, n)."""
    m = len(req)
    pos = [start] + req
    INF = 1 << 30
    dp = [INF] * (m + 1)
    back = [None] * (m + 1)
    dp[0] = 0
    # chain[st][t]: how many consecutive steps of exactly st start at node t
    chains = {}
    for st in (1, 2, 4):
        ch = [0] * (m + 1)
        for t in range(m - 1, -1, -1):
            if pos[t + 1] - pos[t] == st:
                ch[t] = 1 + ch[t + 1]
        chains[st] = ch
    for t in range(m):
        base = dp[t]
        if base >= INF:
            continue
        c = base + skip_cost(pos[t + 1] - pos[t])
        if c < dp[t + 1]:
            dp[t + 1] = c
            back[t + 1] = (t, 'skip', pos[t + 1] - pos[t])
        for st in (1, 2, 4):
            L = chains[st][t]
            if not L:
                continue
            a, b = REP_LIMITS[st]
            cands = set(range(1, min(L, 40) + 1))
            cands.update(min(L, v) for v in (a, b, 0xFFFF))
            for n in cands:
                c = base + rep_cost(st, n)
                if c < dp[t + n]:
                    dp[t + n] = c
                    back[t + n] = (t, 'rep%d' % st, n)
    return dp, back


def _emit(back, t_end):
    ops = []
    t = t_end
    while t:
        pt, op, n = back[t]
        ops.append((op, n))
        t = pt
    ops.reverse()
    out = bytearray()
    for op, n in ops:
        if op == 'skip':
            out += op_skip(n)
        else:
            out += op_rep(int(op[3:]), n)
    return out


def encode(width, height, idx, palette_bytes, transparent=0x0E, junk=b'', planes=4):
    """Encode an image given as rows of palette indices (0-15).

    transparent: palette index the game treats as see-through, or
    TRANSPARENT_NONE.

    Every row is written, including rows made entirely of the transparent
    color, as in all of TGL's own files. Skipping them looks like a free
    saving (the normal draw masks those pixels out anyway), but sprite-sheet
    loaders switch transparency off first (1AD0:0433 sets header word 6 to
    FFFF) and decode the whole sheet opaque, then build tile masks from the
    key color: an unwritten row stays whatever was in VRAM (black)."""
    assert width % 8 == 0
    assert len(palette_bytes) == 24
    assert 0 not in junk
    pats = _row_patterns(width, height, idx, planes)
    N = len(pats)

    # Pattern table in order of first occurrence; position 0 is always drawn.
    order = {}
    table = []
    occ = []
    for p, pat in enumerate(pats):
        k = order.get(pat)
        if k is None:
            k = order[pat] = len(table)
            table.append(pat)
            occ.append([])
        occ[k].append(p)
    U = len(table)
    first = [o[0] for o in occ]

    INF = 1 << 30
    A = [INF] * U       # cost of pattern k ending in 00
    B = [INF] * U       # cost of pattern k up to a literal run on its last position
    plans = []
    for k in range(U):
        if k == 0:
            start, req = 0, occ[0][1:]
        else:
            start, req = first[k - 1], occ[k]
        dp, back = _pattern_plan(start, req)
        m = len(req)
        A[k] = dp[m] + 1
        if m >= 1 and req[m - 1] - ([start] + req)[m - 1] == 1:
            B[k] = dp[m - 1]
        plans.append(back)

    # C[k]: longest literal run that can start on pattern k's last position.
    C = [1] * U
    for k in range(U - 2, -1, -1):
        j = k + 1
        if len(occ[j]) == 1 and occ[j][0] == occ[k][-1] + 1:
            C[k] = 1 + (C[j] if len(occ[j]) == 1 else 0)
    # C[j] was computed from j's last (= only) position, so chaining is right.

    G = [INF] * (U + 1)
    Gb = [None] * (U + 1)
    G[0] = 0
    for k in range(U):
        g = G[k]
        if g >= INF:
            continue
        if g + A[k] < G[k + 1]:
            G[k + 1] = g + A[k]
            Gb[k + 1] = (k, 0)
        if B[k] < INF:
            for c in range(1, C[k] + 1):
                v = g + B[k] + run_cost(c)
                if v < G[k + c]:
                    G[k + c] = v
                    Gb[k + c] = (k, c)

    segs = []
    k = U
    while k:
        pk, c = Gb[k]
        segs.append((pk, c))
        k = pk
    segs.reverse()
    cmds = bytearray()
    for k, c in segs:
        m = len(occ[k]) - (1 if k == 0 else 0)
        if c == 0:
            cmds += _emit(plans[k], m)
            cmds.append(0)
        else:
            cmds += _emit(plans[k], m - 1)
            cmds += op_run(c)
    cmds.append(0)

    pattern_offset = 0x10 + 24 + len(junk) + 1
    cmd_offset = pattern_offset + planes * U
    out = bytearray(b'Gem')
    out += bytes([2, planes, 0])
    out += transparent.to_bytes(2, 'little')
    out += (width // 8).to_bytes(2, 'little')
    out += height.to_bytes(2, 'little')
    out += cmd_offset.to_bytes(4, 'little')
    out += palette_bytes + junk + b'\x00'
    for t in table:
        out += t
    out += cmds
    return bytes(out)


def indices_from_decoded(pix, transparent):
    """decode()'s pixel grid back to indices (None -> transparent)."""
    t = 0 if transparent == TRANSPARENT_NONE else transparent
    return [[t if c is None else c for c in row] for row in pix]


def reencode(data):
    """Decode a GEM and encode it again (for benchmarking the encoder)."""
    hdr = GemHeader(data)
    w, h, _, pix, tr = decode(data)
    return encode(w, h, indices_from_decoded(pix, tr), hdr.palette_bytes, tr)


def nearest_index(palette, rgb):
    """Closest palette entry by summed absolute difference (as gem.py did)."""
    best, bi = None, 0
    for i, c in enumerate(palette):
        d = abs(c[0] - rgb[0]) + abs(c[1] - rgb[1]) + abs(c[2] - rgb[2])
        if best is None or d < best:
            best, bi = d, i
    return bi


def encode_edit(original_gem, edited_img, palette_override=None, tolerance=24):
    """Re-encode an edited version of an existing GEM.

    Transparency and header junk come from the original file, and so does
    the palette unless palette_override (24 packed bytes) is given. If the
    image has the original's size and palette, pixels within `tolerance`
    (|dR|+|dG|+|dB|) of the original keep the original palette index
    exactly, so unedited areas stay bit-identical to the original art.
    Everything else is quantized to the nearest palette color.
    Returns (gem_bytes, stats)."""
    hdr = GemHeader(original_gem)
    ow, oh, opal, opix, tr = decode(original_gem)
    img = edited_img.convert('RGB')
    w, h = img.size
    px = img.load()
    palette_bytes = palette_override or hdr.palette_bytes
    pal = unpack_palette(palette_bytes)
    keep_original = (w, h) == (ow, oh) and palette_bytes == hdr.palette_bytes
    if keep_original:
        idx = indices_from_decoded(opix, tr)
    else:
        idx = [[0] * w for _ in range(h)]
    cache = {}
    kept = quantized = 0
    for y in range(h):
        row = idx[y]
        for x in range(w):
            e = px[x, y]
            if keep_original:
                o = pal[row[x]]
                if abs(o[0] - e[0]) + abs(o[1] - e[1]) + abs(o[2] - e[2]) <= tolerance:
                    kept += 1
                    continue
            c = cache.get(e)
            if c is None:
                c = cache[e] = nearest_index(pal, e)
            quantized += 1
            row[x] = c
    data = encode(w, h, idx, palette_bytes, tr, hdr.junk)
    return data, {'kept': kept, 'quantized': quantized}


# ORFIELD reads a whole TMAP tileset into the EMS page frame (C000:0000, four
# 16KB pages); anything past 64KB lands on whatever is mapped above it.
MAX_TMAP_SIZE = 0x10000
