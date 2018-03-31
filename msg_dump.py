"""
    Use python2 to run this
"""

import os
import xlsxwriter

from rominfo import PORTRAITS

dir = os.curdir

msgs = [os.path.join(dir, 'original', 'OR', m) for m in os.listdir(os.path.join(dir, 'original', 'OR')) if m.endswith('.MSG')]

print len(msgs)

#assert len(msgs) == 248

workbook = xlsxwriter.Workbook('appareden_msg_dump.xlsx')
header = workbook.add_format({'bold': True, 'align': 'center', 'bottom': True, 'bg_color': 'gray'})


worksheet = workbook.add_worksheet('MSGS')
worksheet.set_column('B:B', 60)
worksheet.set_column('C:C', 60)
worksheet.write(0, 0, 'File', header)
worksheet.write(0, 1, 'Offset', header)
worksheet.write(0, 2, 'Japanese', header)
worksheet.write(0, 3, 'English', header)

row = 1

for m in msgs:
    portrait = None
    flush_portrait = False
    with open(m, 'rb') as f:
        contents = f.read()
        cursor = 0
        broken = False
        sjis_buffer = ""
        sjis_buffer_start = 0
        sjis_strings = []
        while cursor < len(contents):
            if 0x80 <= ord(contents[cursor]) <= 0x9f or 0xe0 <= ord(contents[cursor]) <= 0xef:
                first = contents[cursor]
                sjis_buffer += first
                cursor += 1
                second = contents[cursor]
                sjis_buffer += second

                #if ord(first) == 0x81 and ord(second) == 0x75:  # Break before SJIS start quote
                #    broken = True

                if ord(first) == 0x81 and ord(second) == 0x76:  # Break after SJIS end quote
                    broken = True
            elif ord(contents[cursor]) == 0x77:
                cursor += 1
                if ord(contents[cursor]) == 0x30:
                    cursor += 1
                    assert ord(contents[cursor]) & 0xf0 == 0x30
                    sjis_buffer += '[WAIT' + str(ord(contents[cursor]) & 0xf) + ']'
            elif ord(contents[cursor]) == 0x3e:
                # [FACExxxxx] control code, or something else starting with ">""
                cursor += 1
                if ord(contents[cursor]) == 0x66:
                    # it's a face control code
                    #sjis_buffer += '[FACE'
                    portrait = ''
                    cursor += 1
                    counter = 5
                    while counter:
                        #sjis_buffer += contents[cursor]
                        portrait += contents[cursor]
                        cursor += 1
                        counter -= 1
                    #sjis_buffer += ']'
                #else:
                #    sjis_buffer += contents[cursor-1]
                #    sjis_buffer += contents[cursor]
                elif ord(contents[cursor]) != 0x6b:
                    # If we run into a >w or >c, that's the end of this portrait...?
                    # Anything except >k ends the portrait streak.
                    # (>k clears the window but keeps the same portrait)
                    # Need to flush it after it's added to the list of sjis strings.
                    flush_portrait = True
                broken = True

            elif ord(contents[cursor]) == 0x23:
                # Don't include "#"
                broken = True

            #elif ord(contents[cursor]) == 0x40:
            #    # "@", symbols a nametag until the  "n", 6e
            #    cursor += 1
            #    while ord(contents[cursor]) != 0x6e:
            #        sjis_buffer += contents[cursor]
            #        cursor += 1
            #    sjis_buffer += '[LN]'
            #    broken = True

            elif 0x20 <= ord(contents[cursor]) <= 0x7e and ord(contents[cursor]) != 0x6e and ord(contents[cursor]) != 0x40:
                # ASCII characters, but not 'n' or "@"
                sjis_buffer += contents[cursor]
            elif ord(contents[cursor]) == 0x6e:
                sjis_buffer += '[LN]'
            else:
                if sjis_buffer and sjis_buffer != '[LN]':
                    if portrait:
                        sjis_strings.append((sjis_buffer_start, sjis_buffer, portrait))
                    else:
                        sjis_strings.append((sjis_buffer_start, sjis_buffer, ''))
                sjis_buffer = ""
                sjis_buffer_start = cursor+1

            try:
                lookahead_first, lookahead_second = ord(contents[cursor+1]), ord(contents[cursor+2])
                if lookahead_first == 0x81 and lookahead_second == 0x75:
                    # Look ahead and break before SJIS start quote
                    broken = True
            except IndexError:
                pass


            if broken:
                if sjis_buffer and sjis_buffer != '[LN]':
                    sjis_strings.append((sjis_buffer_start, sjis_buffer, portrait))
                sjis_buffer = ""
                sjis_buffer_start = cursor+1
                broken = False

            if flush_portrait:
                portrait = None
                flush_portrait = False

            cursor += 1

        if len(sjis_strings) == 0:
            continue

        for s in sjis_strings:
            loc = '0x' + hex(s[0]).lstrip('0x').zfill(4)
            jp = s[1].decode('shift-jis')
            portrait = s[2]
            filename = m.split('\\')[-1]
            worksheet.write(row, 0, filename)
            worksheet.write(row, 1, loc)
            worksheet.write(row, 2, jp)
            worksheet.write(row, 3, portrait)
            row += 1

workbook.close()
