# Appareden TODOs

## Last TODOs before beta testing
* "Eternal" spell crash when all HP is full
* "Are you sure?" windows have spaceing that is really hard to edit, what's up with that?

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
		* Window a bit too small for my tastes, but basically OK
	* Buy Equipment
		* OK
	* Sell Items
		* OK
	* Sell Equipment
		* OK

* ZP recovery items say they're healing HP.
	* Do the JP strings just say "points restored" generically?

## ORBTL
* Last party member's menu is a little wider than the rest?

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
	* (32A - Ships)
* Further improvements to the SPZ decoder.
	* At this point I mostly just need something to re-encode the SPZ decoder's output.
		* I think the best thing to do would be to output separate sprites into their own image files. That way they can be edited and repacked more easily.
* What are the requirements for each TEFF image?
	* Gento
		* Come on! - individual letters
		* Kiyahh!
		* Do your best! - individual letters
		* Chest!
		* Careful!
		* Raagghh! - monolithic
	* Haley
		* Holy Light - individual letters
		* Deus X Machina
		* Santa Lucia
		* Judgment - monolithic
		* Apocalypse - monolithic
		* Apocalypse (2)
			* (Where does this appear?)
	* Gennai
		* Eleheal
		* Eleshot
		* Elerecover
		* Elespark
		* Elestun
		* Elebuster

* Might be worth some attempt at optimizing the GEM encoder a little more.
	* Control code for alternating chains? 10101 etc

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