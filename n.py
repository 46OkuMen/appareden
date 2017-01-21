"""
Appareden internally uses 'n' (0x6e) as a newline control code. That's obviously
not very convenient for an English translation, so we'd like to change that.
"""

from romtools.disk import Disk

# So, there are 286 n's. When replaced

# 0 to 2: fine
# 0 to 10: fine
# 0 to 100: fine
# 0 to 150: music but scene never loads
# 100 to 150: music but scene never loads
# 100 to 125: music but scene never loads
# 100 to 112: music but scene never loads
# 100 to 106: music but scene never loads
# 100 to 103: fine
# 103: music but scene never loads

# 104: Skips the first line of text in every box, then graphics displaying errors
    # m: Treats the first m as a newline maybe?? But the two n's are still newlines. (& graphics crash)
    # o: Skips the first line, and the only line begins with "Pp" as if o were the newline...
        # then the graphics crash really hard
# 105: no printing, lots of graphical errors
    # m: same
    # o: doesn't print anything, prints a lot of transparent blue window material
    # p:
# 106: display until end of line, then horrible text-displaying errors
    # o: Catastrophic crash, but there's text in the middle of the screen beginning with "p"
    # q: Catastrophic crash
# 107: more weird text-displaying errors
    # m: displays lm, then weird text gets displayed everywhere
    # o: displays lm, then weird text gets displayed everywhere
# 108: image printing error, prints lots of control codes (but still newlines with n)
    # o: same.
# 109: text stops printing after the nametag (and before the m!!)
    # o: displays up to m, then text gets weird and it crashes
    # p: displays up to o, then text gets weird and it crashes
# 110: text gets weird (is that an n in there??)
    # m: displays up to m, then text gets weird and it crashes
    # o: displays up to m, then text gets weird and it crashes

# So, possible suspects: 104, 106, 109
# 107, 108, 110 are probably not related


# 125 to 150: fine
# 150 to 200: fine
# 200 to 225: error message
# 225 to 250: fine
# 250 to 275: fine
# 275 to 286: fine
# 0 to 286: error message

# Messing with IDA now. The n's at 0x15b1d and 0x15b5f (109 and 110) changed to m's are promising:
    # This seems to create a thing where it looks for "m*n" and uses that as a newline.
    # But it blanks out anything between the m and the n, of course.
    # So, why don't I set that first character to something never used (<) and use <n as the code?

    # n displays now, but it still has the newlnie afterwards.

# 109 and 110 replaced with <: displays n but still does a linebreak afterwards
# 108, 109, 110: displays window, but can't display faces
# 105, 109, 110: same as just 109 and 110?
# 105, 106, 109, 110: Graphical glitches/crash. BUT it does display an n without a newline afterwards
# 106, 109, 110: Worse graphical glitch than above, but still n without newline
# 105, 106, 107, 109, 110: Milder graphical glitch than those two, but still n without newline
# 105, 107, 109, 110: Doesn't display n's anymore, they're newlines again
# 106, 107, 109, 110: Same as 105, 106, 109, 110
# 104, 106, 109, 110: Like 105 106 109 110, but with more graphical glitches and crashes
# 106, 109, 110, 111: Same, but more graphical glitches
# 106, 109, 110, 112: Same
# 106, 109, 110, 113: Same
#                114: Same
# 104, 106: Freaks out during the first line break, tons of graphical glitches


# 104 15519 = cmp byte ptr es:[bx], 6e
# 105 15528 = mov byte ptr [bx], 6e
# 106 155d6 = cmp byte ptr es:[bx], 6e
# 107 155ee = mov byte ptr [bx], 6e
# 108 15624 = jmp loc_21D94 (yeah, so don't mess with this)
# 109 15b1d = cmp byte ptr [bx+di], 6e     -- part of printLine
# 110 15b5f = cmp byte ptr [bx+di], 6e     -- part of printLine

# The solution: 104, 105, 106, 107, 109, and 110 need to be changed.

# 6 to 69 (inclusive): that big table of n's. Seems to have no effect when changed

with open('original_ORFIELD.EXE', 'rb') as f:
    file_contents = f.read()
    ns = [i for i in xrange(len(file_contents)) if file_contents.find('n', i) == i] # 286
    cs = [i for i in xrange(len(file_contents)) if file_contents.find('c', i) == i] # 95
    ws = [i for i in xrange(len(file_contents)) if file_contents.find('w', i) == i] # 200

ns_to_replace = [ns[104], ns[105], ns[106], ns[107], ns[109], ns[110],]
print [hex(n) for n in ns_to_replace]

for n in ns_to_replace:
    file_contents = file_contents[:n] + "/" + file_contents[n+1:]

#for i, c in enumerate(cs):
#    print i, hex(c)

# 95 cs.

# 26 11f80
# 27 129f6
# 28 12ab3
# 31 15241
# 32 15b16 = cmp byte ptr [bx+di], 63
# 33 15b6c = cmp byte ptr [bx+di], 63
# 39 2551b = cmp ax, 63

cs_to_replace = [cs[32], cs[33], cs[39],]
for c in cs_to_replace:
    file_contents = file_contents[:c] + "$" + file_contents[c+1:]

#for i, w in enumerate(ws):
#    print i, hex(w)

# 63 151b7 = cmp byte ptr [bp+var_6+1], 77
# 67 15b0f = cmp byte ptr [bx+di], 77
# 68 15b99 = cmp byte ptr [bx+di], 77

ws_to_replace = [ws[63], ws[67], ws[68]]
for w in ws_to_replace:
    file_contents = file_contents[:w] + "}" + file_contents[w+1:]

with open('ORFIELD.EXE', 'wb') as f:
    f.write(file_contents)

AppareDisk = Disk('appareden-patched.hdi')

AppareDisk.insert('ORFIELD.EXE', 'TGL/OR')
AppareDisk.insert('SCN02400.MSG', 'TGL/OR')
