# Appareden TODOs
* It is really unclear which of these still need attention.

## ASM
* Clean up and split FD/CD ORBTL ASM.

## Typesetting
* Indentations after 'clears throat' with asterisks are wrong. Only two, so easy to fix manually?

## Graphics
* Further improvements to the SPZ decoder.
	* At this point I mostly just need something to re-encode the SPZ decoder's output.
		* I think the best thing to do would be to output separate sprites into their own image files. That way they can be edited and repacked more easily.

## Voice Scenes
* Let's do subs on YouTube, and link them in the readme

## Pachy98 settings
* Is the user going to use np2 FMGEN? If not sure, choose YES.
	* If YES, insert SCN12307.COD. (Averts final boss crash)
* Is the user going to have 16.6MB+? If not sure, choose NO.
	* If YES, insert TMAP_00A.GEM. (Image edits in Sapporo, which is too big for standard np2 FMGEN builds)
	* If YES, insert TMAP_10B.GEM. (Image edits in that one city I can't find the name of)
	* If YES, insert TMAP_12B.GEM. (Image edits in the hidden village)