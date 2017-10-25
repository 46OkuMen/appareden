# Appareden Todo

## Reinserter
* Add functionality to move overflowing strings between spare space.
* Better typesetting accounting for control codes.
* Need to typeset files with portraits and files without portraits differently.
* Fix the two problem files in the last batch.
* [WAIT] control codes don't seem to be inserting properly...

## MSGs
* Vagrant "Come on(overline) The place is empty."
* Issues with the ">f01040 tags when meeting GOemon/Master
* Move all MSGs to one sheet in the sys dump.

## ORFIELD
* Shop menus are busted
	* Appears to be the overflow issue from the equipment slots. Need to add more space strings to the dump
* "No zen points" popup is glitched
* Need to expand the equipment name buffers on the status screen. Currently capped at 15 or 16, as on the equipment screen
	* Now capped at 19, which is almost enough. Looking for ways to get more space now

* Equipment names need to be padded out to the max with spaces, or they'll leave garbage when you equip a shorter thing afterwards
	* Item names too; alignment of the shop menus depends on it
	* Won't be a terrible loss of space, since this can be done with the underscore control code and not the ~

* Using a HealOne type Zen art brings up a very misaligned screen.
	* The HP, ZP, and Status column colud use a bit more alignment...

* Item description room in shops is very short, so try to hack in a string-truncation display thing.
	* See docs/item_description_truncation.txt

* I'm not sure how to deal with the window bleeding.
	* Does it have to do with the compressed chars taking up different amounts of room onscreen and ondisk?
		* No; changing all the options to all-lowercase leaves the same issue
	* Ah. Looks like all the headers need to be even-numbered lengths...?
		* And you generally want ~~ at the end of a section header to avoid text overflow.

* ZP recovery items say they're healing HP.
	* Do the JP strings just say "points restored" generically?

* Where do the town names appear ingame? No sign of them so far

* "Ded"
	* Might have been "Dea". "Poi" is showing up for poison, and in memory it's "^Poi"
	* Need more than 4 chars of space for that slot
		* Slot is after "Settings" at 0x28085
		* Whoops, now it is broken more. Just 3 chars now... why?
		* It has 6 chars of space for that slot. &c^Dea
			* Something happens in memory that loads a 00 into that location plus 6...
			* See docs/Dea_glitch_fix.txt

* " Whose?" (equipment) screen is really skinny

## ORBTL
* Benmiaru "Transform" overflows from the action window

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