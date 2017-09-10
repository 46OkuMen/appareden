# Appareden Todo

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.

## Cheat saves
* Some more equipment in the inventory than are valid equipments
* Some more items than are valid items

## ORFIELD
* No pointers for "Whose equipment?" / equipment screen headers
	* Currently points to the " charm" in Monja Bosatsu Charm, pointer value 5720...?
		* Also crashes when scrollilng down to that item
* Shop menus are busted
* Way too many strings showing when displaying which items are equipped
* "Move" as blank entry in menu.
	* Due to an unmarked blank string; added to dump, added to pointers, now fixed.
* The "Good" string that's used everywhere is accidentally lowercase, so the pointer is probably off by one.

## ORBTL
* Guts changes to "rm" after first round of the battle?
	* Not a standard wrong pointer. Becomes "rm" regardless of "Guts"'s length
	* Part of that block is used as memory during gameplay, so it needs to be identified and marked as volatile...
		* Fixed, it was a blank string.
* Crash after first story battle?
	* Crash after every battle really.
	* It's a crash when the screen fades to black for the first time, but before EXP and level ups happen. So some kind of issue in that. 
		* Issue with a pointer between strings 20-21.
			* Workaround for now with an equal length setting.