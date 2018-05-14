import os
import re
import utility
from collections import namedtuple



g_logger = None
g_err = []
def mylogger(path = ''):
    global g_logger
    if g_logger is None:
        g_logger = utility.get_logger(path)

    return g_logger
 
BoundingBox = namedtuple('BoundingBox', ['w', 'h', 'xoff', 'yoff'])

CheckItem = namedtuple('CheckItem', ['file_to_check', 'base_file'])

# class CheckErr(Exception):
    # def __init__(self, message):
        # self.message = message


# class BreakRule(CheckErr):
    # pass


class CharElm(object):
    def __init__(self, content):
        # internal parse functions
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
            raise_error('No matched bounding info for glyph char')

        def parse_unicode(content):
            pattern = re.compile(r'STARTCHAR ([0-9A-F]{4})',
                    re.MULTILINE)
            match = pattern.search(content)
            if match:
                return match.groups()[0]
            raise_error('No matched unicode for glyph char')

        def parse_bitmap(content):
            pattern = (
            re.compile(r'BITMAP[\r\n]([0-9a-fA-F\r\n]+)ENDCHAR',
                    re.MULTILINE) )
            match = pattern.search(content)
            if match:
                return match.groups()[0].split()
            raise_error('No matched bitmap buffer for glyph char')

        def parse_dwidth(content):
            # only parse dwdith x now
            pattern = re.compile(r'DWIDTH (\d+)', re.MULTILINE)
            match = pattern.search(content)
            if match:
                return match.groups()[0]
            raise_error('No matched dwidth for glyph char')
        # internal parse functions end

        self.bounding = parse_bounding(content)
        self.unicode = parse_unicode(content)
        self.bitmap = parse_bitmap(content)
        self.dwidth = parse_dwidth(content)

    def bitmap_width(self):
        if len(self.bitmap) <= 0:
            raise_error('bitmap should not be None')
        w = len(self.bitmap[0])
        for r in self.bitmap:
            if w != len(r):
                raise_error('each line in bitmap should be equal')
        return w

    def consistent_to(self, font_info):
        def check(val, err):
            if not val:
                raise_error('glyph ' + self.unicode + ' '+ err) 


        check(int(self.bounding.w) > 0 and int(self.bounding.h) > 0,
                'Height, Width should not be zero')
        check(self.bounding.h == font_info.bounding.h, 
        'BBh should be equal to font height')
        check(self.bounding.xoff == '0', 'BBxoff is recomended to be 0')
        check(self.bounding.yoff == font_info.bounding.yoff,
                'BByoff should be equal to font yoff')
        check(len(self.bitmap) == int(font_info.bounding.h),
                'Height of bitmap should be equal to the font height')
        check(self.bitmap_width()*8 >= int(self.bounding.w),
                'Bitmap length multiple of 8 should be greater or equal'
                'than glyph width')
        # check(self.dwidth == self.bounding.w,
                # 'Dwidth is not equal to BBX width. It is suggest that '
                # 'Dwidth should contain the width of that dependent char,'
                # 'Other kerning (position adjustment) will be done by MTK'
                # )


class FontInfo(object):
    def __init__(self, content):
        # internal parse functions
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
            raise_error('No font bounding box defined')

        def parse_ascent(content):
            pattern = re.compile(r'FONT_ASCENT (\d+)[\r\n]+'
            'FONT_DESCENT (\d+)', re.MULTILINE)
            match = pattern.search(content)
            if match:
                asc = match.groups()[0]
                desc = match.groups()[1]
                return (asc, desc)
            raise_error('No ascent and descent value defined')
        # internal parse functions end
        
        self.bounding = parse_bounding(content)
        self.ascent, self.descent = parse_ascent(content)



class BdfFile(object):
    def __init__(self, fname):
        # internal parse functions
        def parse_char_elms(content):
            pattern = re.compile(r'STARTCHAR[\s\S]+?ENDCHAR', re.MULTILINE)
            it = re.finditer(pattern, content)
            chars = []
            for match in it:
                chars.append(CharElm(match.group(0)))

            return chars
        # internal parse functions end
 
        self._fname = fname
        content = utility.read_all(self._fname)
        self._font_info = FontInfo(content)
        self._chars = parse_char_elms(content)

    def checkElms(self):
        for elm in self._chars:
            elm.consistent_to(self._font_info)
            
            

def _compare_fontinfo(info1, info2):
    if info1.ascent != info2.ascent:
        raise_error('FONT_ASCENT is not equal in the two files')
    if info1.descent != info2.descent:
        raise_error('FONT_DESCENT is not equal in the two files')


def check_bdf(fn1, fn2=''):
    global g_err
    g_err = []

    b1 = BdfFile(fn1)
    b1.checkElms()

    if fn2 != '':
        b2 = BdfFile(fn2)
        _compare_fontinfo(b1._font_info, b2._font_info)

    return g_err


def raise_error(message):
    global g_err
    g_err.append(message + '\n')




