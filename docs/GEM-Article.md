.GEM is Appareden's image format, used for sprites, backgrounds, tilesets, and the "animated" CD opening. It (or some version of it) is common to many of the games TGL developed, and appears in Edge and the entire Farland Story series. Since GIGA is the adult version of TGL, .GEM also appears in games like Briganty and Variable Geo.

The main unit that makes up a .GEM is a pattern, a horizontal row of eight pixels of particular colors. A section of the file is dedicated to defining all of the unique patterns that occur in an image. Then, the remaining part of the file is a series of instructions on where to paint these patterns on the screen.

## Header

47 65 6d 02 04 00 0e 00 18 00 20 00 2f 03 00 00

The header is still a bit of a mystery, but it doesn't present much of a problem. Many of the values don't appear to have an effect on the image. Of what we do know, these are of interest:

* 0-2: The string "Gem".
* 6: Which color of the palette will show up as transparent. Most images in the game were encoded with a teal background, evidently.
* a-b: Image height.
* c-d: Location of pattern-writing instructions. At this point, the program stops defining patterns and begins to write them to the screen.

## Palette

The PC-98 can display 16 colors at once, chosen from 4096 (4026 according to Touhou wiki?). These 16 colors are specified right after the header, packed into 24 bytes. They are given as RGB tuples, in the order BRG. Two colors are specified in three bytes like so: BR Gb rg.

## Pattern Definitions
To display 16 colors, you need 4 bits to specify which color something needs to be - four planes ^^ two possibilities. The PC-98 uses 4 bitplanes in its VRAM, which is enough to define the color of every pixel.

Let's say the first color in the palette is black, and the sixteenth color is white. If the first bit in each plane is 0, the final displayed color would be the 0000th color in the palette, black. If the first bit in every plane is 1, the pixel would be the 1111th color, white.

(More accurately, they're in reverse order. First plane is the ones place, second plane is the twos place, third plane is the fours place, and fourth plane is the eights place.)

And to determine which of the eight pixels in a pattern are filled in, you need one byte - eight positions ^^ two possibilities. So, with four bytes, you can define what will show up for eight pixels.

Let's say the first pattern is a0 a0 a0 00. a0 represented in binary is 1010 0000, so this would be the first and third pixels of the pattern would be filled in, with color 0111, or seven. 

The patterns repeat with no separation until the file reaches the pattern-writing offset specified in the header.

## Pattern Writing
The program has a cursor it moves from top to bottom, left to right, over the entirety of the image. For each pattern, it starts down one row from its original location.

"Repeat": The simplest instruction is a byte in the 40s and 50s range - the game subtracts 0x40 and writes the pattern that many times. The maximum repeat, with byte 5f, is 31 (0x1f) times.

"Short skip": Between 81 and bf, the program subtracts 80, skips that number of rows, and writes the pattern once. The maximum skip, with byte bf, is 63 (0x3f) empty rows.

"Long skip": Bytes c0 through ff are used to skip a bit further than that. The program reads the next byte too. For example, let's say the skip is c1 23. The program subtracts c000 to get the number 0x123, then skips that number of rows, then writes the pattern once. The maximum long skip, with bytes ff ff, is (something in the 16,000s?) empty rows.

But that still isn't enough. The title screen, being 640x400, is 32,000 rows long (640/8 = 80, 80 * 400 = 32,000). In the worst case, if there were a pattern at the top left and bottom right corners only, we'd need to skip 31,999 rows to write it there. Which brings us to...

"Ultra skip": The byte 80 grants the most control. The program reads two more bytes, one for coarse control, one for fine control. The coarse control byte is multiplied by 255, then added to the fine control byte, to get the number of rows to skip. Then it writes once. The maximum ultra skip, with bytes 80 ff ff, is 65,281 (0xff01) empty rows.

And finally, a 00 marks the end of a pattern. The cursor is reset to where it started, but down one for each completed pattern.

## .SPZ Format
Most of the .GEMs we were interested in editing were single sprites - the title screen, status screen nametags, etc. But when most characters use a special skill in battle, a short animation displays the name of their skill, dropping in letter by letter. To define how a .GEM is sliced into invidividual sprites, the game uses a .SPZ file.

Header:
* 0-3: The string "FSPR".
* 4-5: The number of sprites.
* 6-d: The source filename, minus ".GEM".
* e-1f: All 00 bytes.

Then, a list of where the sprites are located.

A sprite is made up of a number of 8x8? tiles.  (...)




## Other notes

In a rare bit of almost-luck, we did find a program that could at least interpret and display GEMs, a PC-98 utility called MLD. (link) Unfortunately, it doesn't display many images we were interested in, so we fell back on our tried-and-true approach: replacing the game's title screen with the image in question and reloading it from a save state. And as is the case with most 90s Japanese programs, it's closed-source, and we were unable to contact the developer to ask for details.

## Further mysteries

* Farland Story:
	* Farland Story: Tooi Kuni no Monogatari (1)
	* Farland Story Denki: Arc O no Ensei (2)
	* Farland Story: Tenshi no Namida (3)
	* Farland Story: Shirogane no Tsubasa / Hagukin no Tsubasa (4)  (different pronunciations)
	* Farland Story: Daichi no Kizuna (5)
	* Farland Story: Kamigami no Isen (6)
	* Farland Story: Juuou no Akashi (7)

	* Farland Story 2 (gaiden game, Windows)
	* Farland Story: Yottsu no Fuuin (SNES, remake of FS1+2)
	* Farland Story: Kyou Shin no Miyako (8, Win95)

* How much cross-compatibilitiy is there between different versions of GEM?
	* Works: FS1-7, Edge, Kisou Shiden Gen-Kaiser, Sword Dancer 2, Variable Geo 1
	* Works, but need to rename it as "GRP": Harlem Blade
	* Can't find the title image, probably HEM: Briganty, Steam Hearts
	* Uses HEM and TOY: Variable Geo 2
	* Can't run: Sword Dancer

* TGL also uses an image format called HEM in releases including Steam Hearts, Briganty, and Variable Geo 2. It sounds like some sort of variant, but doesn't appear to have any of the same structure. More research is needed.
* And what is TOY?