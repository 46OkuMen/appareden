# Appareden Todo

## Reinserter
* Better typesetting accounting for control codes.
* Need to typeset files with portraits and files without portraits differently.
* Fix the two problem files in the last batch.
* [WAIT] control codes don't seem to be inserting properly...
	* They insert as expected, they just aren't interpreted correctly by the game. Why is this?

## MSGs
* Vagrant "Come on(overline) The place is empty."
* Issues with the ">f01040 tags when meeting GOemon/Master
* Move all MSGs to one sheet in the sys dump.

## ORFIELD

* State of the menus:
	* Item Shop
		* Max description length: 33
			* Window expands in both directions when you lengthen the header. There must be some value of a center location, it'd be nice to adjust that
		* Glitched text when something is purchased
	* Weapon Shop
		* Pretty bad overflow from too-long weapon names.
		* Window is not at its maximum width yet
		* Glitch on "purchased"
	* Armor Shop
		* (Uses same strings as weapon shop)
	* Sell Items
		* Glitched header, glitched contents
	* Sell Equipment

* Equipment names need to be padded out to the max with spaces, or they'll leave garbage when you equip a shorter thing afterwards
	* Item names too; alignment of the shop menus depends on it
	* Won't be a terrible loss of space, since this can be done with the underscore control code and not the ~

* Using a HealOne type Zen art brings up a very misaligned screen.
	* The HP, ZP, and Status column colud use a bit more alignment...
		* Not sure what's happening here

* ZP recovery items say they're healing HP.
	* Do the JP strings just say "points restored" generically?

* Where do the town names appear ingame? No sign of them so far

* True Spirit crashes the game again

* "Can't use that zen art" text is bugged, reads "tectionH"

## ORBTL
* Zen art "spirit" shows up as "Snow text"

* Zen art types are too long, use shorter ones from ORFIELD
	* Might still be too long

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.
	* Or just do those problem files manually.
* Need to progress in the game far enough to get to the minigames and test their graphics.
* That one cat tank monster near Koro-pok-guru village has an animation we should translate too.
* Still haven't given them over to SkyeWelse.
* How should we handle the shop signs?

## CD Version
* So, none of the executables will be the same. Uh oh.
	* ORFIELD.EXE has text that is offset by some amount, but appears the same?
		* It's not a constant amount, so there's probably some new block in the middle. Haven't looked for it specifically yet
			* See docs/CD_differences.txt

* In light of that, need to generate a new column for CD offsets. And probably re-do pointer stuff, ugh

## Cheat saves
* Some more equipment in the inventory than are valid equipments
* Some more items than are valid items
	*The items "Heals10-20", "Revive dead", and "Sandals?" have glitched status windows
* Can't finish a battle, Harry just levels up forever
	* Whoops, it's not forever, just a lot of times (up to lv72)
	* Lv72 Harry file now in Journal Go

## Determined to be non-issues
* Ship item displays "Ocean Dragon Pill" as its error message when you're in a town
	* It does so in the Japanese version too
* The "Good" string that's used everywhere is accidentally lowercase, so the pointer is probably off by one.
	* Workaround, changed to "OK"

## How to fix things
* Window bleeding
	* Pad it with one ~ at the end.
* Window too narrow
	* Pad it with lots of ~ at the end.
* Window too large
	* Put [00] at the end.
* Stuff not found while reinserting MSGs
	* Some characters got garbled by the dumper. Compare the dump's characters to those in the original file byte by byte.