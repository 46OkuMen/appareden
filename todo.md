# Appareden Todo

## Crashes
* Visiting the weapon shop in Dragonia before talking to Tiamat soft locks the game??

## Reinserter
* Can't reinsert ō yet, complains about illegal multibyte sequence.
* Better typesetting accounting for control codes.
* [WAIT] control codes sometimes overwrite a few characters ago.
	* What's the pattern? It's only some of them...
		* Not related to the WAIT number. Is it an even/odd positioning thing?
		* "A hot bath,[WAIT2]ya know?"     -> "A hot bathya know?"
		* "A hot bath,[WAIT3]ya know?"     -> "A hot bathya know?"
		* "A hot bath, [WAIT2]ya know?"    -> "A hot bathya know?"
		* "A hot bath,  [WAIT2]ya know?"   -> "A hot bath,ya konw?"
		* "A hot bath,  [WAIT2]Ya know?"   -> "A hot bath,Ya know?"
		* "A hot bath,[WAIT2] ya know?"    -> "A hot bath,ya know?"
		* "A hot bath, [WAIT2] ya know?"   -> "A hot bath,ya know?"
		* "A hot bath,[WAIT2]  ya know?"   -> "A hot bath, ya know?" (correct)
		* "A hot bath,  [WAIT2]ya know?"   -> "A hot bath, ya know?" (correct)
		* "A hot bath,  [WAIT2]  ya know?" -> "A hot bath,   ya know?"
		* "A hot bath, [WAIT2]  ya know?"  -> "A hot bath, ya know?"
		* "A hot bath, [WAIT2][WAIT2]ya know?" -> "A hot bath, ya know?" (correct)
		* "Khh.... [WAIT6]Orochi!! Strike." -> "Khh.... Orochi! Strike."
		* "Khh....[WAIT2]orochi!! Strike."  -> "Khh.... orochi! Strike."
		* "Khh....[WAIT2]  Orochi!! Strike." -> "Khh....   Orochi! Strike."
		* "Khh....  [WAIT2]Orochi!! Strike." -> "Khh....   Orochi! Strike."
		* "Khh.... [WAIT2] Orochi!! Strike." -> "Khh....   Orochi! Strike."
		* "A hot bath can't be beat, [WAIT2] Orochi!! Strike." -> "A hot bath can't be beOrochi!! Strike."
		* "A hot bath can't be beat,[WAIT2]Orochi!! Strike."   -> "A hot bath can't be bOrochi!! Strike."
		* "A hot bath bath can't be beat,[WAIT2]Orochi!! Strike." -> "A hot bath bath can't be Orochi!! Strike."
		* "A beat,[WAIT2]Orochi!! Strike." -> "A beat,Orochi!! Strike."
		* "A[WAIT2]Orochi!! Strike." -> "A Orochi!! Strike."
		* "a[WAIT2]Orochi!! Strike." -> "aOrochi!! Strike."
		* "a[WAIT2]a[WAIT2]a[WAIT2]" -> "aaa"


	* First theory: [WAIT2] should always have two spaces at the end of it, and other spaces should be removed?
		* Non-initial ones don't need any more spaces.
	* Second theory: [WAIT] has an internal counter of 1 space, which decreases by 1 for every (lowercase?) word before it.
		* So, need to count the lowercase-starting words preceding the WAIT and on the same line, then add n-1 spaces before/after the WAIT.
	* Whatever I'm doing now, it has one too many spaces usually?

* Haley in SCN12800 - the control codes "n>k@(haley)n" might be wrong? They don't wait or clear the screen.

## Typesetting


## MSGs
* Need to clear the window when there's a bunch of long text, then short text, in the same window
	* Example: SCN3100.MSG, border crossing after getting Tamamo
* When a message starts with ( instead of ", the ( glows red
	* Is an old SJIS thing being left in there?? Might be an issue that I always split before SJIS quotes...
* Numbers usually lack a space in front. Should I add another one?
	* It's probably due to the Shadoff compression, any alterations I should make to that?
* Rarieties Shopkeeper's goodbye message labels him as Armor Shopmaster in Naniwa
* What's with the "#(" at 0x36553 in SCN06001.MSG? Is it a typo?

## ORFIELD
* State of the menus:
	* Menu
	* Character Status Select
		* Buffer problems
	* Status Screen
	* Equipment Screen
		* OK
	* Item SCreen
		* OK
	* Zen Screen
		* Buffer problem? "out" as the blank space
		* "Can't use the Zen arts" string is broken
	* Settings
		* Auto-Battle ON/OFF is super broken still
			* Now it's really, really broken
			* I should try just leaving it as the SJIS all caps versions, since those are supported now.
				* Well uh, that looks great but it crashes upon going back to the previous screen now.
		* Order screen is having buffer problems
			* (Only upon making a switch)
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

## Update Patch
* See what was updated in the MSGs.
	* Floppy:
		* SCN05000
		* SCN05103
		* SCN06003
		* SCN10502
		* SCN10900
		* ENDING
	* CD:
		* SCN12306
		* And all the ones in the Floppy

## CD Version
* Need to re-map FILE_BLOCKS.
	* Attempting to consolidate/finalize the list of blocks in original ORFIELD first.
	* Also, this could just be set to all the FD blocks plus a certain offset?
* Need to re-map POINTER_TABLES.
	* ORBTL is done.
* Need to see if there are any new strings in ORBTL and ORFIELD.
* Need to re-hack ORFIELD and ORBTL, with the text code as well as control codes.
* Need to find the locations of every string. See find_cd_diffs.py
	* They can probably be stored in a new column, "Offset (CD)".
		* Done for ORFIELD and ORBTL.

## Cheat saves
* Some more equipment in the inventory than are valid equipments
* Some more items than are valid items
	* The items "Heals10-20", "Revive dead", and "Sandals?" have glitched status windows
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