# Appareden TODOs

## Emulation
X Did a recent version of np21 FMGEN stop running the game?
	* Cause found: the too-big TMAP_00A (72,863 bytes) overran the EMS page frame into D000, where resident
	  code lives. Which emulators froze depended on what was mapped there. The new TMAP_00A is 63,969 bytes.

## ASM
* Clean up and split FD/CD ORBTL ASM. (Not necessary, just nice)

## Typesetting
* Indentations after 'clears throat' with asterisks are wrong. Only two, so easy to fix manually?

## Graphics
* Further improvements could be made to the SPZ decoder to avoid some manual work.
	* At this point I mostly just need something to re-encode the SPZ decoder's output.
		* I think the best thing to do would be to output separate sprites into their own image files. That way they can be edited and repacked more easily.

## Voice Scenes
* Let's do subs on YouTube, and link them in the readme

## Pachy98 settings
X No emulator questions needed any more:
	* SCN12307.COD is always inserted.
	* TMAP_00A/10B/12B.GEM are always inserted: the new encoder (gem_codec.py) keeps them under the
	  64KB EMS page frame ORFIELD loads tilesets into (the old 72KB TMAP_00A overran it and froze
	  the game on Start). Added to both release configs, along with NRCHR_99.GEM/SPZ (Neko Run
	  English text) and FD's missing SFCHR_99.SPZ.

## Final release stuff
* Write a README
	* Determine which emulators to recommend
* Write a Pachy98 config
* Translation for manual?


## v0.99 Bugs
X Graphics/tileset issues
	* This is just due to missing .spz files - make sure those are included
X Typesetting/text overwriting issues
	* Refreshes fine:
	"Goodness... Lord Shiro is so beautiful and yet so
	 manly. He's truly an angel sent here by God."

	"Dear God, let me be a gleaming trumpet upon his lips."
	Separated by "/>p@"


	"I wonder when Uncle Haley'll come back" [...]

	"Sometimes the peak of Mt. Aso" [...]
	Separated by "/>p@"

	* Overwriting issue:
	"... Oh. Looks like you aren't agents of the Shogunate.
	 This is Nagasaki. It's the headquarters of Christianity 
	 in our country."
                                          xxxxxxxxxxxxxxxx
	"We Christians are being oppressed by the Shogunate, you
	 see. We're barely surviving thanks to the efforts of
	 Lord Shiro for hte moment, but..."

	"Who knows how long that'll last... I've heard there's
	 some resistance out towards Imari of some sort,
	 though..."

	 These lines end with "/>k@ 
	 * Replaced all >k with >p - the lines display fine now
	 	* Can we replace all >k with >p in every .MSG file? What side effects would that have?
* Minor typesetting issues
	* For non-portrait characters, it seems like the second window has a space added to the nametag? ex. "Christian" for the first window, then " Christian" for the next few ones
		* Once you see it, you can't un-see it
		* Added Christian, Kenta etc to the NAMES array, we'll see if that fixes the typesetting?
		* These seem to occur on lines where the nametag is in the same string.
X Soft lock with "Pill" in the text displayed?
	* Is this a "Repel's effect wore off" type message from Benimaru's zen?
		"Keystone" - "Party blessed with holy protection"
		0x27ee0	0x28526	法術の効果が切れた	The effect wore off
	* Fixed - incorrect rominfo block for that text
X Dragon Bone description too long? "Dragon powers enhance strength"
X Stat up messages "Max HP raised by409 points!" may need to support 3-digit numbers
* Blank message when trying to use an item while dead (Prime Appare Sake)
	* This a full HP/ZP recovery item - wonder which message this is supposed to be
X "Unable to recover any HP" (while dead?) has too small of a window
X Too small of a window when healing everyone with Ultimate Eternal - "fully recovered their HP" goes past the window
X Last fight with Ultimate Benkei - nametag is too long, so the first line starts on the second line
* SHiro talks to himself - "You've learned to save others just fine on your own..." -> "Haley, may you walk with the Lord"
* "Dragon Majin Okitsugu" might be too long
X Softlock in cut scene before final boss
	* Probably the missing .COD file
* Ultimate Eternal softlock??
	* Seems fixed now? Something with the party messages
	* Not a softlock anymore, but seems to lead to a text corruption bug
		* Use Keystone before, it works fine - "Party blessed with holy protection"
		* Use Ultimate Eternal, get a message with only 4 things (what happens to Tamamo??) and 3 are "can't heal further"
		* Use Keystone again - "rther"
		* Other spells have glitched messages too