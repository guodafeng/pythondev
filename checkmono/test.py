import unittest
from checkmono import *

class TestFontParse(unittest.TestCase):
    def test_font_prase(self):
        bdf = BdfFile(r'test/Bengali_16p.bdf')
        bounding = bdf._font_info.bounding

        self.assertEqual(bounding, BoundingBox(w='5', h='16', xoff='2',
            yoff='-3'))

        chars = bdf._chars

        self.assertEqual(chars[0].bounding, BoundingBox(w='5', h='16', xoff='2',
            yoff='-3'))
        self.assertEqual(chars[0].bounding, BoundingBox(w='6', h='16', xoff='3',
            yoff='-3'))
if __name__ == '__main__':
    unittest.main()

