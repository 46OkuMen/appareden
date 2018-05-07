# Appareden TODOs

## ASM
* Clean up and split FD/CD ORBTL ASM.

## Typesetting
* Indent non-first lines after quotes?
	* Mostly working, fix the stragglers now.
* Extra-long names like Sacrosanct Dragon might need additional (4) spaces in front of each line.
* Need to split windows that overflow using [SPLIT].

## MSGs
* Need to clear the window when there's a bunch of long text, then short text, in the same window
	* Example: SCN3100.MSG, border crossing after getting Tamamo
	* (Is this still a problem?)
* Rarieties Shopkeeper's goodbye message labels him as Armor Shopmaster in Naniwa
* Haley in SCN12800 - the control codes "n>k@(haley)n" might be wrong? They don't wait or clear the screen.

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

## Graphics
* Get some placeholder graphics for the highest priority ones - nametags and Ougi?
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.
	* Or just do those problem files manually.