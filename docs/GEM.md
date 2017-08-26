A horribly organized set of notes produced during the reversing of the GEM format.

Current understanding of the format:
TODO update, I understand it now
It's RGB tuples and some extra garbage I don't understand, separated by 00s. 
Then at the location indicated in the pointer, it writes each pattern 

## Header
Header: first 0x12 bytes?
0-2: Constant "Gem"
03-05: 02 04 00
06-07: background color?
08-09: ??
0a-0b: Height, in pixels
0c-0d: Offset where the lookup table ends and the image proper begins
0e-??: Palette information, in BR Gx format

00 03
33 38
40 F4
4D 94
FB AC
B9 FD
80 21
57 D0
66 87
3A CF
8B 80
7F FF
(00)
Probably not RGB tuples...

0x10: B value
0x11: G value

000000: black
FF0000: black
00FF00: bright pink
FFFF00: bright pink
0000FF: bright green
FF00FF: bright green
00FFFF: white
FFFFFF: white

Clearly the first byte is unrelated...?
FF FF = white
F0 FF = cyan
0F FF = yellow
FF 0F = magenta
FF F0 = white

F0 00 = blue
0F 00 = red
00 F0 = green

Ok, so it's BR Gx. (Not sure what the final value does)

That teal color is RGB 007788. In this world it'd be 80 7x. (yep, there's an 80 7f)


## BENIMARU.GEM
Last few bytes are 00 09 00. Let's replace the 09
00: Removes one pixel from the bottom-right of the "ru"
01: Gold line fill
02: Gold line fill
03: Gold line fill
04: Gold line fill
05: Corner pixel shifted down 3 pixels
06: Gold line fill
07: Repeating gold pixel spaced out by 3, for several columns
08: Garbage, scrambles the rest of the image
(09): Normal
0a: Places 7-8 pixels of various colors in that "ru" corner
0b: Places two rows of 8 pixels of various colors in that corner, expanded upward
0c: Garbage
0d: Places (9+32+32+25) 98 (0x62) garbage rows, starting in that corner
0e: same as 0d
0f: same as 0d
10: Gold line fill (128 pixels tall of gold lines, covering width of screen)
11: Writes a gold pixel, spaced down by 3 black pixels
12: Writes two gold pixels, spaced down by 3 black pixels
13: " " 3
14: " " 4
15: " " 5
16: " " 6
17: " " 7
18: Gold line fill
19: Writes 256 (?) gold pixels
1a: Writes 512 (?) gold pixels
1b: Writes 768 (?) gold pixels
1c: Writes 1024 (?) gold pixels
1d: Writes 1280 (?) gold pixels
1e: Writes 1572 (?) gold pixels
1f: Writes some more gold pixels
20: Gold line fill
21: Writes a gold pixel, spaced down by 1 black pixel
22: " " 2 gold pixels
--
2f: " " 15 gold pixels
30: 48 (?) gold pixels, spaced by 1 black pixel
31: 256 (?) gold pixels, spaced down by 1 black pixel
--
3f: " ", but a lot of pixels
40: Gold line fill
41: One gold pixel (looks normal)
42: Extra gold pixel below the normal one
--
4f: 15 gold pixels
50: 16 gold pixels
--
5f: 31 gold pixels
60: Gold line fill
	60 41: Repeats a write 64 times
	60 46: Same thing
61: 256 (?) gold pixels, no spacing
--
6f: Lots of gold pixels, no spacing
70: Gold line fill, or maybe still more gold pixels  (yeah, still does this even with 41 right afterward)
71: " "
75: " "
--
7f: " "
80: Moves cursor down 1,280 pixels AND DOESN'T WRITE
	TODO: Try 80 80 and see what happens.
81: Corner pixel; normal
82: Corner pixel is shifted down one
83: Corner pixel is shifted down two
--
8f: Corner pixel is shifted down 15
90: Corner pixel is shifted down 16
--
9f: Corner pixel is shifted down 31
a0: Corner pixel is shifted down 32
--
af: Corner pixel is shifted down 47
b0: Corner pixel is shifted down 48
--
bf: Corner pixel is shifted down 63
c0: Skip 64 AND DOESN'T WRITE
	c0 00: Does nothing
	c0 01: Writes one row
	c0 02: Skips 1, writes 1
	c0 c0: SKips 191, writes 1
c1: Skip 255 and write
	c1 01: Skips 256, writes 1
c2: Skip 511 and write
c3: Skip 767 and write
(c4: 1,023, c5: 1,279, c6: 1,536, c7: 1,792, c8: 2,047, c9: 2,304, ca: 2,559, cb: 2,815, cc: 3,072, cd: 3,327, ce: 3,583, cf: 3,839)
--
ff: " "

ff - c1 = 3e, or 63. How many different pixels can I access 
c1: (256*1)-1 =     255
ff: (256*64)-1 = 16,383

768 different rows

The previous row seems to be part of the phrase 0c 05 84.
And the row is just gold pixel, yellow pixel, then blanks. 
Replace the 84 and see what happens?
00: Row is gone
80: Row gets spaced out a lot
88: Row is spaced down 4 from original

Replace the 05 and see what happens?
01: Black, black, then three previous rows are all black too
02: Black, black, then two previous rows are all black too
03: Black, black, then previous row is all black too
04: Black, black
05: Gold, yellow
06: Gold, black
07: Gold, yellow, then next row is various different colors
08: Gold, yellow, then 2nd row down is various different colors

Some kind of palette at the beginning?
ff ff ff 00
fe fe fe 00
fc fd fc 01 f0 f3 f0 07 e7 ef e0 0f 8f 9f 80
7f 7f 7f 00
7c 7c 7e 00
30 30 78 00 00
80 80 80 00
e0 e0 e0 00
f1 f1 f1 00 80 9f 80 3f 00 7f 00
7f 7f 7f 00
1f df 1f c0 4f ef 0f f0 a7 f7 07 f8 f9 f9 01 3e 9e bf 80 1f cf df c0 03 f2 f7 f0 01 f9 fb f8 00
fd fc fc 00
e7 e7 e7 00
c3 db c3 00
41 5d 41 00
20 ae 20 82 00 cf 00 44 00 e6 00 60 00 f0 00 20 00 60 00 00 00 00 00 00
87 87 87 00
cf cf cf 80 1f 9f 1f c0 cf ef 0f e0 a7 f7 07 f8 53 fb 03 fc a9 fd 01 78 00 7c 00 00 00 3c 00 00 84 98 80 00
c0 c0 c0 00
e1 e1 e1 00
7e 7e 7e 07 c5 df c0 1f 80 bf 80 0e c0 df c0 00
f0 f0 f0 00
f8 f8 f8 02 c0 c7 c0 1f 00 3f 00 ff 00 ff 00
7e 54 ff 00 10 00 38 00 00 fc fc fc 01 01 03 00
7f 2a ff 00 f8 01 fe 00 00
60 80 00 00 (or maybe 00 60 80 00)
c7 c7 c7 00 03 3b 03 54 01 fd 01 aa 00 fe 00 c0 00 f0 

Those triplets may be some sort of lookup table. Changing the cf cf cf at 0xd2 to aa aa aa, etc. changes an 8-pixel row pattern on the heads of the "ru" and below the "be" kana modifying quote.

So what's with the much longer ones/the "interruptions" of the chart?
	Replacing them with ff ff ff... seems to change some of the colors of the filled in stuff...?

They appear to be RGB triplets. Changing ff ff ff -> ff 00 ff gives a blue background instead of teal.
Now how are these pixel patterns called?
	Something in 09 41 c1 37 9d seems to call the pattern at 0xd2.
	09:
		00: Pattern is replaced by black lines
		0a: Pattern is replaced by black line, then gold-black-black-teal-teal-teal-teal-teal
		0b: Pattern is replaced by two black lines, then yellow-yellow-gold-black-teal-teal-teal-teal
	41: ...number of times the first instance is duplicated??
		21: Moves both instances down 2 pixels, and the other instance is one pixel lower now
		22: Moves both instances down 4 pixels, and the other instance is one pixel lower and duplicated 2 lower as well
		23: That, but 6 and another duplication
		42: Moves both instances down 2 pixels, also the other instance is doubled now
		43: Moves both instances down 3 pixels? Also the other instance is tripled now
		4f: That, but 15
	c1: Offset of both instances, coarse offset
		c0: Moves both instances left 64 pixels
		c2: Moves both instances right 64 pixels
	37: offset of first instance
		38: Moves first (also second) instance of the pattern down one pixel
		00: Moves first (also second) instance sof the pattern "up" 37 pixels
	9d: offset of second instance
		9e: Moves the second instance of the pattern down one pixel
		9f: Same, down 2 pixels
		81: pattern is right below the first instance of the pattern

Replacing the first pattern (ff ff ff) with aa aa aa shows the background drawn on a lot of stuff.
	First move is drawing the pattern 32 + 32 + 11 = 75 times.

	60 = 
		61 4a: draw pattern 331 times (320+11)
		62 4a: draw pattern 587 times (18*32 + 11)
	4a = draw pattern 75 times...?
		4b = draw pattern 76 times  (0x4b = 75)
		3f = draw pattern 64 times  (0x3f = 63)
		03 = draw pattern 04 times

	86 = drop down 5
	47 = draw pattern 6 times

Height is 32 pixels, width 192 pixels

Changing the value 0e (offset x06) in the header seems to make the background teal for some reason?
	That's more convenient, so I'll take it

Changing the value fd (offset 0xc) in the header skews the teal background, but leaves the characters untouched


0a 41: teal, black, gold, yellow - next line
0a 8f: teal, black, gold, yellow - 15th line after
0a 82: teal, black, gold, yellow - 2nd line after
0a 81: " "
0a 80: teal, black, orange, yellow, black - next line
0b 82: black, gold, yellow, yellow - 2nd line after
09 82: teal, black, yellow, gold, brown - 2nd line after
05 82: teal, black, orange, yellow, brown - 2nd and 4th lines after

With 0a, pixels seem to be manipulated in 4's and not 8's...
0b appears to copy(?) an 8-pixel row.

200 is x0f0
640 is x280

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

        # A pattern is mistakenly placed at 5,366 or so when it should be at 5,622...
    # That's a difference of 256...
    # The pattern is: 1111 1011
    #                 1111 1001
    #                 1111 1011
    #                 1111 1000
    # The second-to-last R ff,  G: bb,  B: 44, so  bf 4 is the color (1010)
    # ff dd 99, so 9fd (1110)
    # Or, fb f9 fb f8
        # Start pattern b'\xfb\xf9\xfb\xf8'. row_cursor: 4083
        #Short skip: 0x82
        #Far skip: 0xc5 0x0
        # 41 82 c5 00
        # Write a line at 4084 (80, 84)
        # Skip a line, then write a line at (80, 86). Cursor is now 4086
        # Far skip: c5 00, which is 1,279? 4086 + 1279 = 5365.
            # This should be c6 00. That produces the correct results...


# Looking for an ultra-skip control code:
# Original location: 16,010
    # 80 01: 16,265
    # 80 ff: 81,290? max total_rows = 32,000, so 81,290 % 32,000 = 17,290, which would be in a quarter down the 43rd block (344th column). Which is correct.

    # TODO: Make sure - is it 255 or 256x?

    # And it's actually 80 xx yy, where xx is coarse (255x) and yy is fine (1x). Great, that is perfect control.


List of images that will require translations:

Profile Names:
BENIMARU.GEM
GENNAI.GEM
GENTO.GEM
HANZOU.GEM
HEILEE.GEM
MEIRIN.GEM
OUGI.GEM
SHIROU.GEM
TAMAMO.GEM

Fullscreen Notes:
GENNAIJ.GEM
GOEMONJ.GEM
HANZOJ.GEM
SHIROUJ.GEM

Title Screen:
ORTITLE.GEM

Battle Skills (Dropping in Text):
TEFF_00A.GEM
TEFF_0AA.GEM
TEFF_0BA.GEM
TEFF_01A.GEM
TEFF_1AA.GEM
TEFF_02A.GEM
TEFF_03A.GEM
TEFF_04A.GEM
TEFF_05A.GEM
TEFF_06A.GEM
TEFF_07A.GEM
TEFF_08A.GEM
TEFF_09A.GEM
TEFF_12A.GEM
TEFF_13A.GEM
TEFF_14A.GEM
TEFF_15A.GEM
TEFF_16A.GEM
TEFF_17A.GEM
TEFF_18A.GEM
TEFF_19A.GEM

Battle Enemies:
CHAR_32A.GEM (one sprite has text *slurp*)

Battle Numbers/Phrases (Minigames):
NRCHR_99.GEM
SFCHR_99.GEM
SFFONT.GEM  (intro to fighting minigame, all black and white and just text. easy for checking?)


MAYBE (most of these are probably better left in for flavor, but might need to be translated?):
SFMAP_A.GEM
SFMAP_B.GEM (these have signs in the background. Not super important to change and possibly better left as flavor)
TMAP_01B.GEM (contains sign saying GOEMON'S BAR in ABASHIRI)
TMAP_32A.GEM (TENCHU **** written on floor in circle)
XMAP_19.GEM (battleback, character visible)