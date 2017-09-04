import unittest
from checkmono import *

class TestFontParse(unittest.TestCase):
    def test_font_prase(self):
        bdf = BdfFile(r'test/Bengali_16p.bdf')
        bounding = bdf._font_info.bounding

        self.assertEqual(bounding, BoundingBox(w='5', h='16', xoff='2',
            yoff='-3'))

        self.assertEqual(bdf._font_info.ascent, '13')
        self.assertEqual(bdf._font_info.descent, '3')

        chars = bdf._chars

        self.assertEqual(chars[0].bounding, BoundingBox(w='5', h='16', xoff='2',
            yoff='-3'))
        self.assertEqual(chars[1].bounding, BoundingBox(w='6', h='16', xoff='3',
            yoff='-3'))

        self.assertEqual(chars[0].bitmap_width(), 2)
        self.assertEqual(len(chars[1].bitmap), 16)
        
        self.assertEqual(chars[0].dwidth, '9')

        
    def test_check(self):
        bdf = BdfFile(r'test/Bengali_16p.bdf')
        bdf.checkElms()

if __name__ == '__main__':
    unittest.main()

