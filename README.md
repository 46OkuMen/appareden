# appareden
![Appareden Title](img/Appareden_title.png)

Romhacking utilities and notes developed as part of [46 OkuMen](http://46okumen.com/)'s English translation patch for *Appareden - Fukuryuu no Shou* (あっぱれ伝 ー伏龍の章ー) (PC-98), a traditional and colorful JRPG based on Japanese history and myth.

### Draft Reinsertion Progress


| Segment      | %      |  Strings            |
| -------------|-------:|:-------------------:|
| ORTITLE.EXE  | 100%   | (18 / 18)           |
| ORFIELD.EXE  | 100%   | (1326 / 1326)       |
| ORBTL.EXE    | 100%   | (792 / 792)         |
| Dialogue     | 100%   | (5601 / 5592)       |
| Images       | 89%    | (49 / 55)           |
| **Total**    |**100%**|  **(7786 / 7783)**  |

### Project notes
* This game's script is longer than our three released projects's scripts combined.
* The game is available on both floppy and CD versions, and our patch targets both.
* A few hacks unique to this project:
	* Dictionary compression - the patch implements compression of the most-common words, and adds ASM to decompress these words at display time.
	* .GEM encoder - this project re-encodes a fairly complex file format used for all iamges in the game.
* Because the game is long and testing is time-consuming, we spent some time on stuff to make it a little easiser:
	* Deciphering save-file format
	* Developing a few cheats
	* Generating a world map from lots of game screenshots
* File types:
	* .MSG - game script file
	* .EXE - system text
	* .GEM - custom image format
	* .SPZ - sprite sheet format
	* .COD - dialogue event routine file format
	* Some of these formats may exist in other TGL games, such as the Farland Story games.
* This is a fullscreen 16-color RPG, so it is an absolute memory hog. It was fairly prone to memory issues upon release, and is still fairly unstable even after the developer's patch.

## Development

### Requirements
* A working hard-disk dump of *Appareden*
* [romtools](https://github.com/46OkuMen/romtools)
* xlsxwriter
* openpyxl
* Bitstring
* nosetests
* ndcpy

### Running Tests
`nosetests test.py` - a few sanity checks

### Building
This requires an existing HDI of Appareden, such as the one from the Neo Kobe pack. The utilities should work on the (developer-) patched or unpatched versions.
Place your dump of `Appareden.hdi` in the subfolder `original`. Then run these scripts to dump the system text, dialogue, and pointers:

```
python sys_dump.py
python msg_dump.py
python find_pointers.py
```

Translate the script, which is dumped into `appareden_sys_dump.xlsx` and `appareden_msg_dump.xlsx`.

Now create a subfolder `patched`, where another copy of `Appareden.hdi` should go. Now run these to reinsert text and images:

```
python typeset_script.py
python reinsert.py
python gem.py
```

Now, `patched/Appareden.hdi` should be playable in English as far as you've translated.

### Main scripts
* sys_dump.py - dumps text from system files (ORTITLE.EXE, ORFIELD.EXE, ORBTL.EXE) into appareden_sys_dump.xlsx.
* msg_dump.py - dumps text from dialogue files (a few hundred .MSG files) into appareden_msg_dump.xlsx.
* find_pointers.py - dumps pointers into appareden_pointer_dump.xlsx.
* typeset_script.py - adds line breaks where necessary into the translated column of the .MSG files.
* reinsert.py - Replaces the JP strings with the translated ones in the dump excel, adjusts pointers, and reinserts the translated files into the HDI.

### Other scripts (used by the above)
* rominfo.py - maps out many properties of the game files, including text blocks, pointer blocks, control codes, etc.
* asm.py - holds the ASM strings used for various text/game modification hacks. Some will be in the final patch (text compression routines, bugfixes), others are just for testing ("turn off random battles" cheat, etc).
* pointer_info.py - list of pointers to reassign. There are lots of duplicate strings - we can save space by re-pointing duplicates to the same text location.
* portraits.py - list of portraits and their character/emotion.
* utils.py - helper functions.

### One-time utility scripts
* dictionary.py - counts the words in ORFIELD/ORBTL and generates a compression dictionary for each. The dictionary is then inserted into the first string in each file.
* replace_title.py - for easily viewing a GEM image. Give it the filename of a GEM image in patched/, and it will replace the title screen with it.
* portraitcrop.py - crop the fullscreen portraits.
* tools/find_cd_diffs.py - determine the text-block location differences between the FD and CD versions.
* n.py - explorative script for trying different control-code values for a line break.

### License
This project is licensed under the Creative Commons A-NC License - see the [LICENSE.md](LICENSE.md) file for details.