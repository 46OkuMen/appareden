"""
    Text typesetter for Appareden.
    Truncates ORFIELD text that exceeds limits.
"""
from appareden.rominfo import CONTROL_CODES, B_CONTROL_CODES, WAITS, POSTPROCESSING_CONTROL_CODES
from appareden.rominfo import DUMP_XLS_PATH,  portrait_characters, MAX_LENGTH
from appareden.utils import typeset, shadoff_compress, replace_control_codes, sjis_punctuate

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

# TODO: Uh, gotta save the workbook too I guess