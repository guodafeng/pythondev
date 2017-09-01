import os
import re
import utility
from collections import namedtuple



g_logger = None
def mylogger(path = ''):
    global g_logger
    if g_logger is None:
        g_logger = utility.get_logger(path)

    return g_logger
 
class CharElm(object):
    def __init__(self, content):
        def parse_bounding(content):
            pattern = re.compile(r'BBX (\d+) (\d+) '
            r'([0-9\-]+) ([0-9\-]+)', re.MULTILINE)
            match = pattern.search(content)
            if match:
                w = match.groups()[0]
                h = match.groups()[1]
                xoff = match.groups()[2]
                yoff = match.groups()[3]
                return BoundingBox(w, h, xoff, yoff)

            return None


        self.bounding = parse_bounding(content)

BoundingBox = namedtuple('BoundingBox', ['w', 'h', 'xoff', 'yoff'])

class FontInfo(object):
    def __init__(self, content):
        def parse_bounding(content):
            pattern = re.compile(r'FONTBOUNDINGBOX (\d+) (\d+) '
            r'([0-9\-]+) ([0-9\-]+)', re.MULTILINE)
            match = pattern.search(content)
            if match:
                w = match.groups()[0]
                h = match.groups()[1]
                xoff = match.groups()[2]
                yoff = match.groups()[3]

                return BoundingBox(w, h, xoff, yoff)
            return None

        
        self.bounding = parse_bounding(content)



class BdfFile(object):
    def __init__(self, fname):
        def parse_char_elms(content):
            pattern = re.compile(r'STARTCHAR[\s\S]+?ENDCHAR', re.MULTILINE)
            it = re.finditer(pattern, content)
            chars = []
            for match in it:
                chars.append(CharElm(match.group(0)))

            print("chars length:", len(chars))

            return chars


        self._fname = fname
        content = utility.read_all(self._fname)
        self._font_info = FontInfo(content)
        self._chars = parse_char_elms(content)



