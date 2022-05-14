# Appareden TODOs

## Emulation
* Did a recent version of np21 FMGEN stop running the game? Need to determine this, and if needed, specify which emulator versions people should use.
	* Recent FMGENs started crashing when the too-big GEM tilesets are included. Let's either recommend np21/W only, or don't reinsert those files at all.

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
* Is the user going to use np2 FMGEN? If not sure, choose YES.
	* If YES, insert SCN12307.COD. (Averts final boss crash)
	* (We no longer recommend this emulator, so should we just remove this option and make sure to insert the file?)
* Is the user going use NP21/W for emulation? If not sure, choose NO.
	* If YES, insert TMAP_00A.GEM. (Image edits in Sapporo, which is too big for standard np2 FMGEN builds)
	* If YES, insert TMAP_10B.GEM. (Image edits in that one city I can't find the name of)
	* If YES, insert TMAP_12B.GEM. (Image edits in the hidden village)

## Final release stuff
* Write a README
	* Determine which emulators to recommend
* Write a Pachy98 config
* Translation for manual?