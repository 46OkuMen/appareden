# Appareden TODOs

## Reinserter
* Haley in SCN12800 - the control codes "n>k@(haley)n" might be wrong? They don't wait or clear the screen.

## ASM
* Clean up and split FD/CD ORBTL ASM.

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
			* OK (Permanently)
		* Exit
			* OK
	* Buy Items
		* Window a bit too small for my tastes
	* Buy Equipment
		* OK
	* Sell Items
		* OK
	* Sell Equipment
		* Alignment is a bit messed up with the "Gale" and "Moonlight" items. Try not compressing them? Or adding a space after them?
			* Yeah, let's try not compressing them.

* ZP recovery items say they're healing HP.
	* Do the JP strings just say "points restored" generically?

* Need to figure out what's in every shop so I can give some item descriptions more room.
	* See docs/shops.md.

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