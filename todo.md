# Appareden Todo

## CD Version
* So, none of the executables will be the same. Uh oh.
	* ORFIELD.EXE has text that is offset by some amount, but appears the same?
		* It's not a constant amount, so there's probably some new block in the middle. Haven't looked for it specifically yet
			* See docs/CD_differences.txt

* In light of that, need to generate a new column for CD offsets. And probably re-do pointer stuff, ugh

## Reinserter
* Add functionality to move overflowing strings between spare space.
* Better typesetting accounting for control codes.
* Need to typeset files with portraits and files without portraits differently.
* Fix the two problem files in the last batch.
* [WAIT] control codes don't seem to be inserting properly...

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
* Need to expand the equipment name buffers on the status screen. Currently capped at 15 or 16, as on the equipment screen
	* Now capped at 19, which is almost enough. Looking for ways to get more space now

* Equipment names need to be padded out to the max with spaces, or they'll leave garbage when you equip a shorter thing afterwards
	* Won't be a terrible loss of space, since this can be done with the underscore control code and not the ~

* Ship item displays "Ocean Dragon Pill" as its error message when you're in a town
	* It does so in the Japanese version too

* Using a HealOne type Zen art brings up a very misaligned screen.
	* The HP, ZP, and Status column colud use a bit more alignment...

* Item description room in shops is very short, so try to hack in a string-truncation display thing.
	* See docs/item_description_truncation.txt

* ZP recovery items say they're healing HP.

* "Not enough ZPBenimuaru not enough ZPdoesn't know any Zen arts"

* Where do the town names appear ingame? No sign of them so far

## ORBTL
* Benmiaru "Transform" overflows from the action window

* "Enemy snuck up on you" text is blanked

* "Defenseraised by 16points!" for every stat, also "Harrygained a level!"

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.
	* Or just do those problem files manually.
* Need to progress in the game far enough to get to the minigames and test their graphics.
* Still haven't given them over to SkyeWelse.

## Cheat saves
* Some more equipment in the inventory than are valid equipments
* Some more items than are valid items
	*The items "Heals10-20", "Revive dead", and "Sandals?" have glitched status windows
* Can't finish a battle, Harry just levels up forever