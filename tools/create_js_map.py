import os
import re


def create_js_map(file_name):
    # create a structure map, field name using the first line, value
    # using the second line
    fh = open(file_name, 'r', encoding='utf8')
    lines = fh.readlines()
    fh.close()

    if len(lines) < 2:
        print("wrong data in file_name")
        return

    fields = lines[0].split(',')
    print("fields len:" + str(len(fields)));
    values = lines[1].split(',')
    print("values len:" + str(len(values)));

    fvs = zip(fields,values)
    out = ''
    for (field,value) in fvs:
        value = value.strip('"')
        if field and value:
            out += "'{0}': '{1}',\n".format(field, value)

    print(out)
        


def parse_values(line):
    pattern = re.compile("(.*),")
    return re.findall(pattern, line)

create_js_map("data/mnc_language.txt")
