# Appareden TODOs

## Reinserter
* Can't reinsert ō yet, complains about illegal multibyte sequence.
	* Workaround for now is replacing them with [o], [O], [u], and [U]...

* Haley in SCN12800 - the control codes "n>k@(haley)n" might be wrong? They don't wait or clear the screen.

* "Don't Compress" category still compresses.

## ASM
* Any way to get the outlines/shadows back for fullwidth text? I wondeer what important thing I got rid of.
* Clean up and split up the CD code, and write everything into an ASM file for easy reference.

## Typesetting
* Indent non-first lines after quotes
* Extra-long names like Sacrosanct Dragon might need additional (4) spaces in front of each line.
* Need a control code to split windows into two.

## MSGs
* Need to clear the window when there's a bunch of long text, then short text, in the same window
	* Example: SCN3100.MSG, border crossing after getting Tamamo
	* (Is this still a problem?)
* Rarieties Shopkeeper's goodbye message labels him as Armor Shopmaster in Naniwa

## ORFIELD
* State of the menus:
	* Menu
		* OK
	* Character Status Select
		* OK
	* Status Screen
		* OK
	* Equipment Screen
		* OK
	* Item SCreen
		* OK
	* Zen Screen
		* OK
	* Zen Target Screen
		* Status is a little too close to the ZP. Might need to adjust the 232 spaces...
		* Any buffer issues?
	* Settings
		* Auto-Battle
			* OK
		* Order Change
			* Buffer problems again
		* Exit
			* OK
	* Item Shop
		* Max name length: 20
		* Max description length: 33
			* Window expands in both directions when you lengthen the header. There must be some value of a center location, it'd be nice to adjust that
	* Equipment Shop
		* Max name length: 17
		* Max description length: 36?
	* Sell Items
		* ?
	* Sell Equipment
		* Alignment is a bit messed up with the "Gale" and "Moonlight" items. Try not compressing them? Or adding a space after them?
			* Yeah, let's try not compressing them.

* ZP recovery items say they're healing HP.
	* Do the JP strings just say "points restored" generically?

* Need to figure out what's in every shop so I can give some item descriptions more room.
	* See docs/shops.md.

* Item shop menu is acting differently in FD and CD versions.
	* String in FD: 0x4c long
	* String in CD: 0x4d long
	* FD: 620 pixels wide
	* CD: 573 pixels wide
	* FD with empty header: 239 pixels wide
	* CD with empty header: 254 pixels wide
	* Compare the code around FD-ORFIELD "900b" and CD-ORFIELD "b60b", which are referneces to the item shop header pointer.
		* Any mentions of values around 239-254?

## ORBTL
* Zen art types are too long, use shorter ones from ORFIELD
	* Actually they need to be even shorter

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.
	* Or just do those problem files manually.

## CD Version
* Bottom-left house in Mito with tree in front of it crashes when you enter it.
	* Does this in the original too.
	* Exclusive to the CD version, it is fine in the FD one.

## How to fix things
* Window bleeding
	* Pad it with one ~ at the end.
* Window too narrow
	* Pad it with lots of ~ at the end.
* Window too large
	* Put [00] at the end.
* JP strings in MSGs not being found
	* There's some difference between the string in the dump and the string in the msg.
	* Look for double-ascii-spaces, improperly dumped kanji, etc. Compare byte by byte.
* MSG dialogue includes >f00013 and the next window too
	* Put an [LN] at the end of the line, if there's one at the end of the JP line
* Game freezes, and resetting it makes it freeze at the sound select screen
	* See if the joystick is stuck in Joy2Key