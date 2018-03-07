.GEM is Appareden's image format, used for sprites, backgrounds, tilesets, and the "animated" CD opening. It (or some version of it) is common to many of the games TGL developed, and appears in Edge and the entire Farland Story series. Since GIGA is the adult version of TGL, .GEM also appears in games like Briganty. There's also a format called .HEM used in Steam Hearts, whose name suggests it's some sort of variant.

The main unit that makes up a .GEM is a pattern, a horizontal row of eight pixels of particular colors. A section of the file is dedicated to defining all of the unique patterns that occur in an image. Then, the remaining part of the file is a series of instructions on where to paint these patterns on the screen.

## Header

47 65 6d 02 04 00 0e 00 18 00 20 00 2f 03 00 00

The header is still a bit of a mystery, but it doesn't present much of a problem. Many of the values don't appear to have an effect on the image. Of what we do know, these are of interest:

* 0-2: The string "Gem".
* 6: Which color of the palette will show up as transparent. Most images in the game were encoded with a teal background, evidently.
* a-b: Image height.
* c-d: Location of pattern-writing instructions. At this point, the program stops defining patterns and begins to write them to the screen.

## Palette

The PC-98 can display 16 colors at once, chosen from 4096 (4026 according to Touhou wiki?). These 16 colors are specified right after the header, packed into 24 bytes. They are given as RGB tuples, (...)

## Pattern Definitions
To display 16 colors, you need 4 bits to specify which color something needs to be - four planes ^^ two possibilities. The PC-98 uses 4 bitplanes in its VRAM, which is enough to define the color of every pixel.

Let's say the first color in the palette is black, and the sixteenth color is white. If the first bit in each plane is 0, the final displayed color would be the 0000th color in the palette, black. If the first bit in every plane is 1, the pixel would be the 1111th color, white.

(More accurately, they're in reverse order. First plane is the ones place, second plane is the twos place, third plane is the fours place, and fourth plane is the eights place.)

And to determine which of the eight pixels in a pattern are filled in, you need one byte - eight positions ^^ two possibilities. So, with four bytes, you can define what will show up for eight pixels.

Let's say the first pattern is a0 a0 a0 00. a0 represented in binary is 1010 0000, so this would be the first and third pixels of the pattern would be filled in, with color 0111, or seven. 

## Pattern Writing
At the location given at offset c-d in the header, the program switches from defining patterns to writing them.

## .SPZ Format
Most of the .GEMs we were interested in editing were single sprites - the title screen, status screen nametags, etc. But when most characters use a special skill in battle, a short animation displays the name of their skill, dropping in letter by letter. To define how a .GEM is sliced (...)

## Other notes

In a rare bit of almost-luck, we did find a program that could at least interpret and display GEMs, a PC-98 utility called MLD. (link) Unfortunately, it doesn't display many images we were interested in, so we fell back on our tried-and-true approach: replacing the game's title screen with the image in question and reloading it from a save state. And as is the case with most 90s Japanese programs, it's closed-source, and we were unable to contact the developer to ask for details.

## Further mysteries

* How much cross-compatibilitiy is there between different versions of GEM?
	* Works: FS7
	* Yet to check: FS1-6, Edge, Briganty, Steam Hearts
	* Still haven't looked for GEMS in: Sword Dancer series, more GIGA stuff

* What is a HEM, anyway?