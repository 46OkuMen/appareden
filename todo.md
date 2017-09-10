# Appareden Todo

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.

## Cheat saves
* Some more equipment in the inventory than are valid equipments
* Some more items than are valid items

## ORFIELD
* No pointers for "Whose equipment?" / equipment screen headers
	* Currently points to the " charm" in Monja Bosatsu Charm, pointer value 5720...?
* Shop menus are busted
* Way too many strings showing when displaying which items are equipped
* "Move" as blank entry in menu.
	* Due to an unmarked blank string; added to dump, added to pointers, now fixed.

## ORBTL
* Guts changes to "rm" after first round of the battle?
* Crash after first story battle?
	* Crash after every battle really.
	* It's a crash when the screen fades to black for the first time, but before EXP and level ups happen. So some kind of issue in that. 
		* Issue with a pointer in the first 55 strings.