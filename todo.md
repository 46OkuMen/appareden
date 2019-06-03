# Appareden TODOs

## Last TODOs before beta testing
* "Eternal" spell crash when all HP is full
* "Are you sure?" windows have spacing that is really hard to edit, what's up with that?

## ASM
* Clean up and split FD/CD ORBTL ASM.

## Typesetting
* Extra-long names like Sacrosanct Dragon might need additional (4) spaces in front of each line.
* Indentations after 'clears throat' with asterisks are wrong. Only two, so easy to fix manually?

## MSGs
* Need to clear the window when there's a bunch of long text, then short text, in the same window
	* Example: SCN3100.MSG, border crossing after getting Tamamo
	* (Is this still a problem?)
* Rarieties Shopkeeper's goodbye message labels him as Armor Shopmaster in Naniwa
* Haley in SCN12800 - the control codes "n>k@(haley)n" might be wrong? They don't wait or clear the screen.

## ORFIELD
* Recovery spells do a rainbow flash on the target select screen...?
	* This only happened in the cheat save file with Haley at a too-high level. Hasn't happened outside there
* State of the menus:
	* Menu
		* OK
	* Character Status Select
		* OK
	* Status Screen
		* OK
	* Equipment Screen
		* OK
	* Item Screen
		* OK
	* Zen Screen
		* OK
	* Zen Target Screen
		* OK
	* Settings
		* Auto-Battle
			* OK
		* Order Change
			* OK
		* Exit
			* OK
	* Buy Items
		* Window a bit too small for my tastes, but basically OK
	* Buy Equipment
		* OK
	* Sell Items
		* OK
	* Sell Equipment
		* OK

* ZP recovery items say they're healing HP.
	* Do the JP strings just say "points restored" generically?

## Graphics
* Which MAP tileset goes to which place?
	* 00 - not sure where
		* Test map?
	* 00A - Sapporo, has palette issues
		* Not palette, the palette is the same.
		* The image renders properly when it's the title screen, is it interacting weirdly with some other image?
		* Is it too large KB-wise? It's 89 KB, the rest are around 49-ish
			* That looks like it.
			* It loads properly in NP21/W with memory set to 16.6MB+. This can be a Pachy option.
	* 01A/01B - Ashabari
	* 03A - Hakodate
	* 06A - Hirosaki
	* 10B - The unnamed city, memory issues (67kb)
	* 11A - Mito?
	* 12B - Hidden village and Dragonian Village, memory issues (70kb)
	* 14A - Naniwa and Kobe?
	* 16B - Nikkou and Izumo Grand Shrine
	* 27A - ?
	* 29B - Edo

* Further improvements to the SPZ decoder.
	* At this point I mostly just need something to re-encode the SPZ decoder's output.
		* I think the best thing to do would be to output separate sprites into their own image files. That way they can be edited and repacked more easily.
* What are the requirements for each TEFF image?
	* Gento
		* Come on! - individual letters
		* Kiyahh!
		* Do your best! - individual letters
		* Chestoh!
		* Careful!
		* Raagghh! - monolithic
	* Haley
		* Holy Light - individual letters
		* Hallelujah - individual
		* Deus X Machina - individual
		* Santa Lucia - individual
		* Judgment - monolithic
		* Apocalypse - monolithic
	* Gennai
		* Eleheal - individual
		* Eleshot - 
		* Elerecover - unused
		* Elespark
		* Elestun
		* Elebuster

* "Slurp" CHAR images
	* 32A:
		* Segment 1 in bottom-left corner: 64x16 top-right of Slurp
		* Segment 2 at bottom-center: 80x16 middle of Slurp
		* Segment 3 at bottom-right: 80x16 bottom of slurp
	* 43A:
		* Segment 1 on the left: 34(!)x16 middle-right of Slurp
		* Segment 2 in the middle: 80x16 bottom of Slurp
		* Segment 3 up-and-right of that: 64x16 top-right of Slurp (partially duplicates S1)
		* Segment 4 on the right: 48x16 middle-left of Slurp (partially duplicates S1)
		* (I think this might be a slightly different graphic than 32A. But it's probably fine)

* SFCHR_99.GEM
	* SF is located in Kobe (use state 3)
	* Currently it's totally broken - were those extra parts of the palette (32, 33, etc) important??
	* Need to edit the .SPZ manually.
		* Gen   to sprite needs its parts to be placed adjacent
		* "1 Round" / "2 Round" etc need to be rearranged.

## Voice Scenes
* What to do??
	* Don't dub them, please
	* Put all the script text on the images?
		* Which images?
	* Also sub them for Youtube and link them in the readme??

## Pachy98 settings
* Is the user going to use np2 FMGEN? If not sure, choose YES.
	* If YES, insert SCN12307.COD. (Averts final boss crash)
* Is the user going to have 16.6MB+? If not sure, choose NO.
	* If YES, insert TMAP_00A.GEM. (Image edits in Sapporo, which is too big for standard np2 FMGEN builds)
	* If YES, insert TMAP_10B.GEM. (Image edits in that one city I can't find the name of)
	* If YES, insert TMAP_12B.GEM. (Image edits in the hidden village)