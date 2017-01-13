"""
Appareden internally uses 'n' (0x6e) as a newline control code. That's obviously
not very convenient for an English translation, so we'd like to change that.
"""

with open('original_ORFIELD.EXE', 'rb') as f:
    file_contents = f.read()
    ns = [i for i in xrange(len(file_contents)) if file_contents.find('n', i) == i]
    # 286 n's.

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

ns_to_replace = ns[100:101]
print [hex(n) for n in ns_to_replace]

for n in ns_to_replace:
    file_contents = file_contents[:n] + "o" + file_contents[n+1:]

with open('ORFIELD.EXE', 'wb') as f:
    f.write(file_contents)
