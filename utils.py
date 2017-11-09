def effective_length(s):
    """The length of a string, ignoring the control codes."""

    # TODO: Not working properly yet.
    length = 0
    chars = s.split()
    while chars:
        if chars[0] != b'[':
            length += 1
            chars.pop(0)
        else:
            while chars[0] != b']':
                chars.pop(0)
            chars.pop(0)

    return length

def typeset(s, width=37):
    if len(s) <= width:
        return s

    words = s.split(b' ')
    lines = []

    while words:
        line = b''
        while len(line) <= width and words:
            if len(line + words[0] + b' ') > width:
                break
            line += words.pop(0) + b' '

        line = line.rstrip()
        lines.append(line)
    #for l in lines:
    #    print(l)

    return b'/'.join(lines)

def shadoff_compress(s):
    # Definitely don't compress filenames!
    if b'.GEM' in s:
        return s
    # If it's all spaces, keep it the same
    if s.count(b' ') == len(s):
        return s

    s = s.decode('shift-jis')
    compressed = ''

    chars = list(s)

    continuous_spaces = 0
    #print(chars)
    while chars:
        c = chars.pop(0)
        if c == ' ':
            continuous_spaces += 1
            if not chars:
                compressed += c
        elif c.isupper():
            if continuous_spaces > 2:
                compressed += '_' + chr(continuous_spaces)
            elif continuous_spaces > 0:
                compressed += ' '*(continuous_spaces)
            continuous_spaces = 0
            compressed += '^'
            compressed += c
        else:
            if continuous_spaces > 2:
                compressed += '_' + chr(continuous_spaces)
                c = c.upper()
            elif continuous_spaces > 0:
                compressed += ' '*(continuous_spaces-1)
                c = c.upper()
            continuous_spaces = 0
            compressed += c
        #print(bytes(compressed, encoding='shift-jis'))

    #print(bytes(compressed, encoding='shift-jis'))

    return bytes(compressed, encoding='shift-jis')

def replace_control_codes(s):
    s = s.decode('shift-jis')
    cursor = 0
    while cursor < len(s):
        c = s[cursor]
        if c == 'n':
            if s[cursor-1] != '>':
                s = s[:cursor] + '/' + s[cursor+1:]
        if c == 'w':
            s = s[:cursor] + '}' + s[cursor+1:]
        if c == 'c':
            if s[cursor-1] != '>':
                s = s[:cursor] + '$' + s[cursor+1:]
        cursor += 1
    s = s.encode('shift-jis')
    return s