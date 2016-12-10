import os
import xlsxwriter

dir = os.curdir

msgs = [os.path.join(dir, 'OR', m) for m in os.listdir(os.path.join(dir, 'OR')) if m.endswith('.MSG')]

assert len(msgs) == 248

workbook = xlsxwriter.Workbook('appareden_dump.xlsx')
header = workbook.add_format({'bold': True, 'align': 'center', 'bottom': True, 'bg_color': 'gray'})

for m in msgs:
    with open(m, 'rb') as f:
        contents = f.read()
        cursor = 0
        sjis_buffer = ""
        sjis_buffer_start = 0
        sjis_strings = []
        while cursor < len(contents):
            if 0x80 <= ord(contents[cursor]) & 0Xf0 <= 0x9f:
                sjis_buffer += contents[cursor]
                cursor += 1
                sjis_buffer += contents[cursor]
            elif ord(contents[cursor]) == 0x77:
                cursor += 1
                if ord(contents[cursor]) == 0x30:
                    cursor += 1
                    assert ord(contents[cursor]) & 0xf0 == 0x30
                    sjis_buffer += '[WAIT' + str(ord(contents[cursor]) & 0xf) + ']'
            elif ord(contents[cursor]) == 0x3e:
                # [FACExxxxx] control code, or something else starting with 3e
                cursor += 1
                if ord(contents[cursor]) == 0x66:
                    # it's a face control code
                    sjis_buffer += '[FACE'
                    cursor += 1
                    counter = 5
                    while counter:
                        sjis_buffer += contents[cursor]
                        cursor += 1
                        counter -= 1
                    sjis_buffer += ']'
                else:
                    sjis_buffer += contents[cursor-1]
                    sjis_buffer += contents[cursor]
            elif 0x20 <= ord(contents[cursor]) <= 0x7e and ord(contents[cursor]) != 0x6e:
                # ASCII characters, but not 'n' or '#'
                sjis_buffer += contents[cursor]
            else:
                if sjis_buffer:
                    sjis_strings.append((sjis_buffer_start, sjis_buffer))
                sjis_buffer = ""
                sjis_buffer_start = cursor+1
            cursor += 1

        if len(sjis_strings) == 0:
            continue

        worksheet = workbook.add_worksheet(m.split('\\')[-1])
        worksheet.set_column('B:B', 100)
        worksheet.write(0, 0, 'Offset', header)
        worksheet.write(0, 1, 'Japanese', header)
        row = 1
        for s in sjis_strings:
            loc = '0x' + hex(s[0]).lstrip('0x').zfill(4)
            jp = s[1].decode('shift-jis')
            worksheet.write(row, 0, loc)
            worksheet.write(row, 1, jp)
            row += 1

workbook.close()
