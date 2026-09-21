"""
    Overlines (macrons) in the credits: "Jado~" -> Jadō, "O~NO" -> ŌNO.

    ENDING.EXE draws the credits into text VRAM (routine at image offset
    1223, called once from 3FA1), so the hardware draws each glyph and the
    main game's trick of overlaying character 7E on the previous letter
    doesn't work. Instead:

    * four user-defined characters (gaiji) in CG RAM, JIS 7621-7624 =
      Ō ō Ū ū, each in the left half of its 16x16 cell: a text cell showing
      a gaiji on its own displays the left half.
    * when the credits routine meets "~", it steps back to the previous
      cell, swaps that vowel for the matching gaiji, and builds that
      glyph: the vowel's rows read from the font ROM (half-width characters
      are JIS 29xx in the CG window, as ENDING's own glyph reader does),
      plus a bar above it. So the result matches the player's font ROM.

    The new code lives in the graphics draw_text at image 1088-1222, which
    ENDING never calls (no far calls to it; its helpers are only called
    from inside it). Image offsets; IP = image offset - 0x40 in this segment.
"""

IMAGE_TO_IP = -0x40
HOOK = 0x1265           # half-width path of the credits routine: xor ah,ah / mov es:[di+2000h],dl
LOOP_HEAD = 0x124A      # "mov [0xee],di" at the top of its character loop
CAVE = 0x1088
CAVE_END = 0x1223       # the credits routine itself starts here
HOOK_ORIGINAL = bytes.fromhex("32e4 2688950020".replace(" ", ""))

# (previous char, text VRAM cell code, unused, CG half-select bit)
# The bar row isn't fixed: it's put two rows above the glyph's top row, read
# from the font ROM at run time (fonts differ in where the glyphs start).
# One gaiji per glyph, always its left half: a lone gaiji cell shows the left
# half on real hardware (half bit clear) and in np21w, which ignores the half
# bit for gaiji and alternates halves across consecutive gaiji cells instead.
VOWELS = [
    (b"O", 0x2156, 1, 0x20),    # JIS 7621
    (b"o", 0x2256, 4, 0x20),    # JIS 7622
    (b"U", 0x2356, 1, 0x20),    # JIS 7623
    (b"u", 0x2456, 4, 0x20),    # JIS 7624
]
BAR = 0x7E


def build():
    """Return [(image offset, bytes)] edits for ENDING.EXE."""
    ip = lambda image_off: image_off + IMAGE_TO_IP  # noqa: E731
    items = [
        ("label", "entry"),
        b"\x3c\x7e",                    # cmp al, 7Eh
        ("jcc", 0x74, "macron"),        # je macron
        b"\x32\xe4",                    # xor ah, ah                 (the two instructions
        b"\x26\x88\x95\x00\x20",        # mov es:[di+2000h], dl       the hook replaced)
        b"\xc3",                        # ret -> stosw, jmp loop head
        ("label", "macron"),
        b"\x53\x51\x52",                # push bx / cx / dx
        b"\x26\x8b\x45\xfe",            # mov ax, es:[di-2]         previous cell's code
    ]
    for ch, code, row, half in VOWELS:
        items += [
            b"\xbb" + code.to_bytes(2, "little"),           # mov bx, cell code
            b"\xb9" + bytes([half, row]),                   # mov cx, row:half
            b"\x3c" + ch,                                   # cmp al, vowel
            ("jcc", 0x74, "found"),
        ]
    items += [
        ("jcc", 0xEB, "done"),          # jmp short done: not a vowel, drop the "~"
        ("label", "found"),
        b"\x26\x89\x5d\xfe",            # mov es:[di-2], bx         show the gaiji half
        ("call", "glyph"),
        ("label", "done"),
        b"\x5a\x59\x5b",                # pop dx / cx / bx
        b"\x83\xc4\x02",                # add sp, 2                 skip the stosw
        ("jmp16", "loophead"),          # the "~" takes no cell
        # make_glyph: al = vowel, bh & 7F = gaiji code low byte, cl = half
        ("label", "glyph"),
        b"\x88\xc4",                    # mov ah, al
        b"\xb0\x0b\xe6\x68",            # mov al, 0Bh / out 68h, al  CG dot access
        b"\x31\xd2",                    # xor dx, dx
        ("label", "scan"),              # find the glyph's top row in the font ROM
        b"\x88\xe0\xe6\xa1",            # mov al, ah / out 0A1h, al
        b"\xb0\x09\xe6\xa3",            # mov al, 09h / out 0A3h, al
        b"\x88\xd0\x0c\x20\xe6\xa5",    # mov al, dl / or al, 20h / out 0A5h, al
        b"\xe4\xa9",                    # in al, 0A9h
        b"\x84\xc0",                    # test al, al
        ("jcc", 0x75, "top"),           # jnz top
        b"\xfe\xc2",                    # inc dl
        b"\x80\xfa\x10",                # cmp dl, 10h
        ("jcc", 0x72, "scan"),
        ("label", "top"),
        b"\x88\xd5",                    # mov ch, dl
        b"\x80\xed\x02",                # sub ch, 2                  bar two rows above it
        ("jcc", 0x73, "barok"),         # jnc barok
        b"\x32\xed",                    # xor ch, ch
        ("label", "barok"),
        b"\x31\xd2",                    # xor dx, dx                 dl = line
        ("label", "line"),
        b"\x88\xe0\xe6\xa1",            # mov al, ah / out 0A1h, al  font ROM: JIS 29xx
        b"\xb0\x09\xe6\xa3",            # mov al, 09h / out 0A3h, al
        b"\x88\xd0\x0c\x20\xe6\xa5",    # mov al, dl / or al, 20h / out 0A5h, al
        b"\xe4\xa9",                    # in al, 0A9h
        b"\x38\xea",                    # cmp dl, ch
        ("jcc", 0x75, "keep"),
        b"\x0c" + bytes([BAR]),         # or al, bar
        ("label", "keep"),
        b"\x88\xc6",                    # mov dh, al
        b"\x88\xf8\x24\x7f\xe6\xa1",    # mov al, bh / and al, 7Fh / out 0A1h, al
        b"\xb0\x56\xe6\xa3",            # mov al, 56h / out 0A3h, al  gaiji row 76
        b"\x88\xd0\x08\xc8\xe6\xa5",    # mov al, dl / or al, cl / out 0A5h, al
        b"\x88\xf0\xe6\xa9",            # mov al, dh / out 0A9h, al
        b"\xfe\xc2",                    # inc dl
        b"\x80\xfa\x10",                # cmp dl, 10h
        ("jcc", 0x72, "line"),
        b"\xb0\x0a\xe6\x68",            # mov al, 0Ah / out 68h, al  back to code access
        b"\xc3",                        # ret
    ]
    code, _ = _assemble(items, ip(CAVE), {"loophead": ip(LOOP_HEAD)})
    assert CAVE + len(code) <= CAVE_END, hex(len(code))
    hook, _ = _assemble([("call", "cave"), b"\x90" * 4], ip(HOOK), {"cave": ip(CAVE)})
    assert len(hook) == len(HOOK_ORIGINAL)
    return [(HOOK, hook), (CAVE, code)]


def _assemble(items, origin, external=None):
    """items: bytes, ("label", name), ("jcc", opcode, name), ("call", name) or
    ("jmp16", name). external: addresses of labels outside `items`."""
    sizes = {"jcc": 2, "call": 3, "jmp16": 3}
    labels = dict(external or {})
    for _ in range(2):
        pos = origin
        for it in items:
            if isinstance(it, bytes):
                pos += len(it)
            elif it[0] == "label":
                labels[it[1]] = pos
            else:
                pos += sizes[it[0]]
    out = bytearray()
    pos = origin
    for it in items:
        if isinstance(it, bytes):
            out += it
            pos += len(it)
            continue
        kind = it[0]
        if kind == "label":
            continue
        if kind == "jcc":
            rel = labels[it[2]] - (pos + 2)
            assert -128 <= rel < 128, it
            out += bytes([it[1], rel & 0xFF])
        else:
            op = 0xE8 if kind == "call" else 0xE9
            rel = labels[it[1]] - (pos + 3)
            out += bytes([op]) + (rel & 0xFFFF).to_bytes(2, "little")
        pos += sizes[kind]
    return bytes(out), labels


# The credits routine from its prologue up to the hook, identical on FD and CD
# (the CD build has it 0xA bytes later).
CREDITS_SIG = bytes.fromhex(
    "558bec56571efc8b760ab800a08ec08b3eee00837e06ff740eb8a000f76608"
    "034606034606 8bf8893eee00b2e1ac22c07431".replace(" ", ""))
CREDITS = 0x1223


def file_edits(exe):
    """[(file offset, bytes)] for this ENDING.EXE (FD or CD), found by signature."""
    i = exe.find(CREDITS_SIG)
    assert i >= 0 and exe.find(CREDITS_SIG, i + 1) < 0, "credits routine not found exactly once"
    shift = i - CREDITS              # file offset of image offset 0
    h = shift + HOOK
    assert exe[h:h + len(HOOK_ORIGINAL)] == HOOK_ORIGINAL, "unexpected bytes at the hook"
    return [(shift + off, data) for off, data in build()]


def patch(exe):
    exe = bytearray(exe)
    for off, data in file_edits(bytes(exe)):
        exe[off:off + len(data)] = data
    return bytes(exe)
