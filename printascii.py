#!/usr/bin/env python
import os

def print_ascii():
    special = (7,8,9,10,13)
    spec_dict = {}.fromkeys(special, ' ')
    spec_dict[7] = '\\a'
    spec_dict[8] = '\\b'
    spec_dict[9] = '\\t'
    spec_dict[10] = r'\n'
    spec_dict[13] = r'\r'
    cols = 6
    max_code = 128
    rows = max_code/cols
    line = ''
    for i in range (cols):
        line += "DEC  HEX CH    "
    print line
    for i in range(rows):
        line = ''
        for j in range(cols+1):
            code = j*rows + i
            if code>max_code-1:
                break
            ch = chr(code)
            if (code in spec_dict):
                ch = spec_dict[code]
            line += "%3d  %2X  %-2s    " % (code, code, ch)
        print line
if __name__ == '__main__':
    print_ascii()
