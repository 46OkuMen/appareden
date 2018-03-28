"""
    Text typesetter for Appareden.
    Truncates ORFIELD text that exceeds limits.
"""
from appareden.rominfo import CONTROL_CODES, B_CONTROL_CODES, WAITS, POSTPROCESSING_CONTROL_CODES, MSGS
from appareden.rominfo import DUMP_XLS_PATH,  portrait_characters, MAX_LENGTH
from appareden.utils import typeset, shadoff_compress, replace_control_codes, sjis_punctuate, properly_space_waits

from romtools.dump import DumpExcel

Dump = DumpExcel(DUMP_XLS_PATH)

filenames = ['ORFIELD.EXE',]
for f in filenames:
    rownum = 0
    worksheet = Dump.workbook.get_sheet_by_name(f)
    first_row = list(worksheet.rows)[0]
    header_values = [t.value for t in first_row]
    en_col = header_values.index('English (Ingame)')
    category_col = header_values.index('Category')

    for row in worksheet.rows:
        if row == first_row:
            continue

        english =row[en_col].value
        category = row[category_col].value

        if category:
            maxlen = MAX_LENGTH[category]
            if len(english) > maxlen:
                print(english, "is too long")
                while len(english) >= maxlen:
                    english = english[:-1]
                english += "."
                print(english)
                row[en_col].value = english
                print()


# More experimental: Typesetting MSG strings

HIGHEST_SCN = 2401

#msg_files = [f for f in os.listdir(os.path.join('original', 'OR')) if f.endswith('MSG') and not f.startswith('ENDING')]
msgs_to_typeset = [f for f in MSGS if int(f.lstrip('SCN').rstrip('.MSG')) <= HIGHEST_SCN]
rownum = 0
worksheet = Dump.workbook.get_sheet_by_name('MSG')
first_row = list(worksheet.rows)[0]
header_values = [t.value for t in first_row]
en_col = header_values.index('English (Ingame)')
jp_col = header_values.index('Japanese')
en_typeset_col = header_values.index('English (Typeset)')
file_col = header_values.index('File')

for m in msgs_to_typeset:
    portrait_window_counter = 0
    for row in worksheet.rows:
        nametag = False
        file = row[file_col].value
        if file == m:
            japanese = row[jp_col].value
            english = row[en_col].value

            #for cc in CONTROL_CODES:
            #    # Skip this one
            #    if cc == b'[ff]':
            #        continue
            #    english = english.replace(cc.decode('shift-jis'), CONTROL_CODES[cc].decode('shift-jis'))

            # If a character with a portrait is given a nametag in this line,
            # the next line needs to be typeset more aggressively due to less screen space.

            if english.count('"') == 0:
                # Nametag
                nametag = True
                #print("-"*57)

            for name in portrait_characters:
                #if name.encode('shift-jis') in t.japanese:
                if name == japanese.replace('[LN]', '').replace('　', ''):
                    portrait_window_counter = 2
                    break


            # For Haley's lines
            # TODO: DIsabling for now
            #english = sjis_punctuate(english)

            if portrait_window_counter > 0:
                english = typeset(english, 37)
            else:
                english = typeset(english, 57)

            english = properly_space_waits(english)

            print(english)
            row[en_typeset_col].value = english
            english_lines = english.split('[LN]')
            line_count = 5
            for e in english_lines:
                if portrait_window_counter > 0:
                    pass
                    #print ("%s%s" % (" "*20, e))
                else:
                    #print(e)
                    pass
                line_count -= 1

            if not nametag:

                while line_count > 0:
                    #print()
                    line_count -= 1

                #print('-'*57)

                if line_count < 0:
                    pass
                    #print("^ This window overflows")

            if portrait_window_counter > 0:
                portrait_window_counter -= 1

Dump.workbook.save(DUMP_XLS_PATH)
