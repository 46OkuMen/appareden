# Appareden Todo

## Reinserter
* Better typesetting accounting for control codes.
* [WAIT] control codes sometimes overwrite a few characters ago.
	* What's the pattern? It's only some of them...
		* Not related to the WAIT number. Is it an even/odd positioning thing?
	* You can workaround it by adding spaces after it, but that's annnoying...

## MSGs
* Vagrant "Come on(overline) The place is empty."
	* Replaced the ~ with --, maybe that'll work?
	* Also, the overline should come from an actual overlined character, not ~...
* Need to clear the window when there's a bunch of long text, then short text, in the same window
	* Example: SCN3100.MSG, border crossing after getting Tamamo
* When a message starts with ( instead of ", the ( glows red
* Numbers usually lack a space in front. Should I add another one?
	* It's probably due to the Shadoff compression, any alterations I should make to that?
* Rarieties Shopkeeper's goodbye message labels him as Armor Shopmaster in Naniwa
* Thunder Dragon displays Gen'nai's face
	* It uses control code >f04100
		* And indeed, FACE4100.GEM is Thunder Dragon...
		* Code >f04100, 4200, 4700, etc. all show Gen'nai's face. Where is it going wrong?
		* GEM in current use is at memory 0x4503. 0000 for Gento, 0100 for Benimaru. 0400 is Gen'nai, shows up when 
	* First few control codes in scene: 01000, 00091, 01050, 00111
		* Face image files are only 4 digits long
		* 0100 = benimaru neutral
		* 0410 = invalid filename, but starts with 4 so it's Gen'nai
		* 4100 should be Thunder Dragon

## ORFIELD

* State of the menus:
	* Item Shop
		* Max name length: ?
		* Max description length: 33
			* Window expands in both directions when you lengthen the header. There must be some value of a center location, it'd be nice to adjust that
	* Equipment Shop
		* Max name length: 17
		* Max description length: 36?
		* Window is at maximum width
	* Sell Items
		* Weird spacing, and that ` thing too
	* Sell Equipment

* Equipment names need to be padded out to the max with spaces, or they'll leave garbage when you equip a shorter thing afterwards
	* Item names too; alignment of the shop menus depends on it
	* Won't be a terrible loss of space, since this can be done with the underscore control code and not the ~
	* This needs to account for ^s too

* ZP recovery items say they're healing HP.
	* Do the JP strings just say "points restored" generically?

* Where do the town names appear ingame? No sign of them so far
	* Also, that's probably not all the locations in the game. Which points to them not being used

* "Can't use that zen art" text is bugged, reads "tectionH"

## ORBTL

* Zen art types are too long, use shorter ones from ORFIELD
	* Might still be too long

## Graphics
* Need to figure out how larger SPZ files point to tiles beyond the 255th one.
	* Or just do those problem files manually.
* Need to progress in the game far enough to get to the minigames and test their graphics.
* That one cat tank monster near Koro-pok-guru village has an animation we should translate too.
	* Wheelcat - CHAR_43A.GEM
* Still haven't given them over to SkyeWelse.
* How should we handle the shop signs?
	* All identified.
* CD version intro graphics need to be translated too.
	* All identified.

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
* JP strings in MSGs not being found
	* There's some difference between the string in the dump and the string in the msg.
	* Look for double-ascii-spaces, improperly dumped kanji, etc. Compare byte by byte.
* MSG dialogue includes >f00013 and the next window too
	* Put an [LN] at the end of the line, if there's one at the end of the JP line
* Game freezes, and resetting it makes it freeze at the sound select screen
	* See if the joystick is stuck in Joy2Key