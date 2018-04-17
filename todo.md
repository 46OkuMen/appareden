# Appareden Todo

## Crashes
* Visiting the weapon shop in Dragonia before talking to Tiamat soft locks the game??

## Reinserter
* Can't reinsert ō yet, complains about illegal multibyte sequence.

* Haley in SCN12800 - the control codes "n>k@(haley)n" might be wrong? They don't wait or clear the screen.

## Typesetting
* Indent non-first lines after quotes
* Extra-long names like Sacrosanct Dragon might need additional (4) spaces in front of each line.

## MSGs
* Need to clear the window when there's a bunch of long text, then short text, in the same window
	* Example: SCN3100.MSG, border crossing after getting Tamamo
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
		* Status is " Acc Good"
	* Settings
		* Auto-Battle
			* OK (Needed a few extra strings)
		* Order Change
			* OK (Finally...)
		* Exit
	* Item Shop
		* Max name length: 20
		* Max description length: 33
			* Window expands in both directions when you lengthen the header. There must be some value of a center location, it'd be nice to adjust that
	* Equipment Shop
		* Max name length: 17
		* Max description length: 36?
	* Sell Items
		* 
	* Sell Equipment
		* Alignment is a bit messed up with the "Gale" and "Moonlight" items. Try not compressing them? Or adding a space after them?
			* Yeah, let's try not compressing them.

* Attack/Recovery/etc need to have the same length in the item shop, but should be different lengths in the Zen menu.
	* Decouple the 

* ZP recovery items say they're healing HP.
	* Do the JP strings just say "points restored" generically?

## ORBTL

* Zen art types are too long, use shorter ones from ORFIELD
	* Might still be too long

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.
	* Or just do those problem files manually.

## CD Version
* ORFIELD missing pointers for "Buy Items/Sell Items".


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