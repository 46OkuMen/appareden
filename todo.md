# Appareden Todo

## CD Version
* Check to see if any of these changes will work for patching the CD version.

## Reinserter
* Add functionality to move overflowing strings between spare space.
* Better typesetting accounting for control codes.
* Fix the two problem files in the last batch.

## ORFIELD
* No pointers for "Whose equipment?" / equipment screen headers
	* Currently points to the " charm" in Monja Bosatsu Charm, pointer value 5720...?
		* Also crashes when scrollilng down to the following item, Dainichi charm
			* Workaround: Just put a [00] at the end of its description string

* Shop menus are busted
	* Appears to be the overflow issue from the equipment slots. Need to add more space strings to the dump
* The "Good" string that's used everywhere is accidentally lowercase, so the pointer is probably off by one.
	* Workaround, changed to "OK"
* Save menu is super wide
* "No zen points" popup is glitched
* Extra "ld" after Gold value in status screen
	* Pointer issue, fixed now.
* Need to expand the equipment name buffers on the status screen. Currently capped at 15 or 16, as on the equipment screen
	* Now capped at 19, which is almost enough. Looking for ways to get more space now

* Equipment names need to be padded out to the max with spaces, or they'll leave garbage when you equip a shorter thing afterwards
	* Won't be a terrible loss of space, since this can be done with the underscore control code and not the ~

* Ship item displays "Ocean Dragon Pill" as its error message when you're in a town
* Airship crashes the game with its error message, like that charm's error
	* Workaround, added an [00] at the end
* "This Zen art is for use in battle" has an overflowing window
	* Workaround, added an [00] at the end

* Using a HealOne type Zen art brings up a very misaligned screen.
	* Take a look at the spaces and stuff around 0x2ea85 and later.
		* Actually not spaces - it just has to do with the varying character name lengths.
			* Fixed.
	* The HP, ZP, and Status column colud use a bit more alignment...

* Life1-2 crashes the game

* Item description room in shops is very short, so try to hack in a string-truncation display thing.
	* See docs/item_description_truncation.txt

## ORBTL

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.
	* Or just do those problem files manually.
* Need to progress in the game far enough to get to the minigames and test their graphics.
* Still haven't given them over to SkyeWelse.

## Cheat saves
* Some more equipment in the inventory than are valid equipments
* Some more items than are valid items
	*The items "Heals10-20", "Revive dead", and "Sandals?" have glitched status windows