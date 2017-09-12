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
		* Also crashes when scrollilng down to that item
* Shop menus are busted
* Way too many strings showing when displaying which items are equipped
* The "Good" string that's used everywhere is accidentally lowercase, so the pointer is probably off by one.

## ORBTL

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.
	* Or just do those problem files manually.
* Need to progress in the game far enough to get to the minigames and test their graphics.
* Still haven't given them over to SkyeWelse.

## Cheat saves
* Some more equipment in the inventory than are valid equipments
* Some more items than are valid items