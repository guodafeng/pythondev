#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  
#  Used FreeType-py to convert vector font file to bitmap font file--
#  FreeType high-level python API - Copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
Show how to access glyph outline description.
'''
import freetype
from freetype import *
import re
import logging
import os
import os.path
import getopt
import sys
import codecs

#generate the visualble content in bdf for debug
VISUAL_MODE=False


PADDING_MAP = {}

def init_padding():
    global PADDING_MAP
    hindi_leftpadding18 = []
    hindi_leftpadding22 = []
    hindi_leftpadding26 = []
    PADDING_MAP = {'hindi18':hindi_leftpadding18,
                   'hindi22':hindi_leftpadding22,
                   'hindi26':hindi_leftpadding26}
    for k in PADDING_MAP:
        for i in range(15):
            PADDING_MAP[k].append([])

    # The data are from the HindiFontSpec_Ver26_N.xlsx Remark columns
    hindi_leftpadding18[0] = [0x0940,0x094A,0x094B,0x094C,0xE95B,0xE95C,0xE95D,0xE95E,0xE95F,0xE987,0xE988,0xE989,0xE991,0xE992,0xE993,0xE994,0xE995,0xE9AD]
    hindi_leftpadding18[1] = [0x904,0x905,0x906,0x907,0x908,0x909,0x90A,0x090B,0x090C,0x090D,0x090E,0x090F,0x910,0x911,0x912,0x913,0x914,0x915,0x916,0x917,0x918,0x919,0x091A,0x091B,0x091C,0x091D,0x091E,0x091F,0x920,0x921,0x922,0x923,0x924,0x925,0x926,0x927,0x928,0x929,0x092A,0x092B,0x092C,0x092D,0x092E,0x092F,0x930,0x931,0x932,0x933,0x934,0x935,0x936,0x937,0x938,0x939,0x093D,0x093E,0x093F,0x949,0x950,0x951,0x952,0x953,0x954,0x958,0x959,0x095A,0x095B,0x095C,0x095D,0x095E,0x095F,0x960,0x961,0x962,0x963,0x970,0xE900,0xE901,0xE902,0xE903,0xE904,0xE905,0xE906,0xE907,0xE908,0xE909,0xE90A,0xE90B,0xE90C,0xE90D,0xE90E,0xE90F,0xE915,0xE916,0xE917,0xE918,0xE919,0xE91A,0xE91B,0xE91C,0xE91D,0xE91E,0xE91F,0xE920,0xE921,0xE922,0xE923,0xE924,0xE925,0xE926,0xE927,0xE928,0xE929,0xE92A,0xE92B,0xE92C,0xE92D,0xE92E,0xE92F,0xE930,0xE931,0xE932,0xE933,0xE934,0xE935,0xE936,0xE937,0xE938,0xE939,0xE940,0xE941,0xE942,0xE943,0xE944,0xE945,0xE946,0xE947,0xE948,0xE949,0xE94A,0xE94B,0xE94C,0xE94D,0xE94E,0xE94F,0xE950,0xE951,0xE952,0xE953,0xE954,0xE955,0xE956,0xE957,0xE958,0xE959,0xE970,0xE971,0xE972,0xE973,0xE974,0xE975,0xE976,0xE97C,0xE97D,0xE97E,0xE97F,0xE980,0xE981,0xE982,0xE983,0xE984,0xE985,0xE986,0xE996,0xE997,0xE998,0xE999,0xE99B,0xE99C,0xE99D,0xE99E,0xE99F,0xE9A0,0xE9A1,0xE9A2,0xE9A3,0xE9A4,0xE9A7,0xE9A9,0xE9AA,0xE9AB,0xE9AC,0xE9AE,0xE9AF,0xE9B0,0xE9B1,0xE9B2,0xE9B3,0xE9B4,0xE9B5,0xE9B6,0xE9B7,0xE9B8,0xE9B9,0xE9BC,0xE9BD,0xE9BE,0xE9BF,0xE9C0,0xE9C1,0xE9c2,0xE9C3,0xE9c4]
    hindi_leftpadding18[2] = [0x093C,0x964,0x965,0x966,0x967,0x968,0x969,0x096A,0x096B,0x096C,0x096D,0x096E,0x096F]
    hindi_leftpadding18[3] = [0x903,0x941,0x946,0x948,0xE98E,0xE98F,0xE990]
    hindi_leftpadding18[4] = []
    hindi_leftpadding18[5] = [0x901,0x943,0x944,0x947,0xE97B,0xE98A,0xE98B,0xE98C,0xE98D]
    hindi_leftpadding18[6] = [0x942,0x945,0x094D]
    hindi_leftpadding18[9] = [0x902]
    
    hindi_leftpadding22[0] = [0x940,0x094A,0x094B,0x094C,0xE95B,0xE95C,0xE95D,0xE95E,0xE95F,0xE987,0xE988,0xE989,0xE991,0xE992,0xE993,0xE994,0xE995,0xE9AD]
    hindi_leftpadding22[1] = [0x904,0x905,0x906,0x907,0x908,0x909,0x90A,0x090B,0x090C,0x090D,0x090E,0x090F,0x910,0x911,0x912,0x913,0x914,0x915,0x916,0x917,0x918,0x919,0x091A,0x091B,0x091C,0x091D,0x091E,0x091F,0x920,0x921,0x922,0x923,0x924,0x925,0x926,0x927,0x928,0x929,0x092A,0x092B,0x092C,0x092D,0x092E,0x092F,0x930,0x931,0x932,0x933,0x934,0x935,0x936,0x937,0x938,0x939,0x093D,0x093E,0x093F,0x949,0x950,0x951,0x952,0x953,0x954,0x958,0x959,0x095A,0x095B,0x095C,0x095D,0x095E,0x095F,0x960,0x961,0x962,0x963,0x970,0xE900,0xE901,0xE902,0xE903,0xE904,0xE905,0xE906,0xE907,0xE908,0xE909,0xE90A,0xE90B,0xE90C,0xE90D,0xE90E,0xE90F,0xE915,0xE916,0xE917,0xE918,0xE919,0xE91A,0xE91B,0xE91C,0xE91D,0xE91E,0xE91F,0xE920,0xE921,0xE922,0xE923,0xE924,0xE925,0xE926,0xE927,0xE928,0xE929,0xE92A,0xE92B,0xE92C,0xE92D,0xE92E,0xE92F,0xE930,0xE931,0xE932,0xE933,0xE934,0xE935,0xE936,0xE937,0xE938,0xE939,0xE940,0xE941,0xE942,0xE943,0xE944,0xE945,0xE946,0xE947,0xE948,0xE949,0xE94A,0xE94B,0xE94C,0xE94D,0xE94E,0xE94F,0xE950,0xE951,0xE952,0xE953,0xE954,0xE955,0xE956,0xE957,0xE958,0xE959,0xE970,0xE971,0xE972,0xE973,0xE974,0xE975,0xE976,0xE97C,0xE97D,0xE97E,0xE97F,0xE980,0xE981,0xE982,0xE983,0xE984,0xE985,0xE986,0xE996,0xE997,0xE998,0xE999,0xE99B,0xE99C,0xE99D,0xE99E,0xE99F,0xE9A0,0xE9A1,0xE9A2,0xE9A3,0xE9A4,0xE9A7,0xE9A9,0xE9AA,0xE9AB,0xE9AC,0xE9AE,0xE9AF,0xE9B0,0xE9B1,0xE9B2,0xE9B3,0xE9B4,0xE9B5,0xE9B6,0xE9B7,0xE9B8,0xE9B9,0xE9BC,0xE9BD,0xE9BE,0xE9BF,0xE9C0,0xE9C1,0xE9c2,0xE9C3,0xE9c4]
    hindi_leftpadding22[2] = [0x964,0x965,0x966,0x967,0x968,0x969,0x096A,0x096B,0x096C,0x096D,0x096E,0x096F]
    hindi_leftpadding22[3] = [0x093c]
    hindi_leftpadding22[5] = [0x903,0x941,0x946,0x948,0xE98E,0xE98F,0xE990]
    hindi_leftpadding22[6] = [0x901,0x943,0x944,0x947,0xE97B,0xE98A,0xE98B,0xE98C,0xE98D]
    hindi_leftpadding22[8] = [0x942,0x945,0x094D]
    hindi_leftpadding22[11] = [0x902]

    hindi_leftpadding26[0] = [0x940,0x094A,0x094B,0x094C,0xE95B,0xE95C,0xE95D,0xE95E,0xE95F,0xE987,0xE988,0xE989,0xE991,0xE992,0xE993,0xE994,0xE995,0xE9AD]
    hindi_leftpadding26[1] = [0x904,0x905,0x906,0x907,0x908,0x909,0x90A,0x090B,0x090C,0x090D,0x090E,0x090F,0x910,0x911,0x912,0x913,0x914,0x915,0x916,0x917,0x918,0x919,0x091A,0x091B,0x091C,0x091D,0x091E,0x091F,0x920,0x921,0x922,0x923,0x924,0x925,0x926,0x927,0x928,0x929,0x092A,0x092B,0x092C,0x092D,0x092E,0x092F,0x930,0x931,0x932,0x933,0x934,0x935,0x936,0x937,0x938,0x939,0x093D,0x093E,0x093F,0x949,0x950,0x951,0x952,0x953,0x954,0x958,0x959,0x095A,0x095B,0x095C,0x095D,0x095E,0x095F,0x960,0x961,0x962,0x963,0x970,0xE900,0xE901,0xE902,0xE903,0xE904,0xE905,0xE906,0xE907,0xE908,0xE909,0xE90A,0xE90B,0xE90C,0xE90D,0xE90E,0xE90F,0xE915,0xE916,0xE917,0xE918,0xE919,0xE91A,0xE91B,0xE91C,0xE91D,0xE91E,0xE91F,0xE920,0xE921,0xE922,0xE923,0xE924,0xE925,0xE926,0xE927,0xE928,0xE929,0xE92A,0xE92B,0xE92C,0xE92D,0xE92E,0xE92F,0xE930,0xE931,0xE932,0xE933,0xE934,0xE935,0xE936,0xE937,0xE938,0xE939,0xE940,0xE941,0xE942,0xE943,0xE944,0xE945,0xE946,0xE947,0xE948,0xE949,0xE94A,0xE94B,0xE94C,0xE94D,0xE94E,0xE94F,0xE950,0xE951,0xE952,0xE953,0xE954,0xE955,0xE956,0xE957,0xE958,0xE959,0xE970,0xE971,0xE972,0xE973,0xE974,0xE975,0xE976,0xE97C,0xE97D,0xE97E,0xE97F,0xE980,0xE981,0xE982,0xE983,0xE984,0xE985,0xE986,0xE996,0xE997,0xE998,0xE999,0xE99B,0xE99C,0xE99D,0xE99E,0xE99F,0xE9A0,0xE9A1,0xE9A2,0xE9A3,0xE9A4,0xE9A7,0xE9A9,0xE9AA,0xE9AB,0xE9AC,0xE9AE,0xE9AF,0xE9B0,0xE9B1,0xE9B2,0xE9B3,0xE9B4,0xE9B5,0xE9B6,0xE9B7,0xE9B8,0xE9B9,0xE9BC,0xE9BD,0xE9BE,0xE9BF,0xE9C0,0xE9C1,0xE9c2,0xE9C3,0xE9c4]
    hindi_leftpadding26[2] = [0x964,0x965,0x966,0x967,0x968,0x969,0x096A,0x096B,0x096C,0x096D,0x096E,0x096F]
    hindi_leftpadding26[3] = [0x093c]
    hindi_leftpadding26[5] = [0x903,0x941,0x946,0x948,0xE98E,0xE98F,0xE990]
    hindi_leftpadding26[7] = [0xE97B]
    hindi_leftpadding26[8] = [0x901,0x943,0x944,0x947,0xE98A,0xE98B,0xE98C,0xE98D]
    hindi_leftpadding26[10] = [0x942,0x945,0x094D]
    hindi_leftpadding26[13] = [0x902]


def get_padding_val(font, charcode):
    padval = 0
    paddings = PADDING_MAP[font]
    for i in range(len(paddings)):
        if (charcode in paddings[i]):
            padval = i
            break
    return padval

 


class otf2bdf(object):
    __ttfname = ''
    __bdfname = ''
    __resolution = 72
    __font_name = "" 
    __char_width = 18
    __char_height = 18
    __char_size = 18
    __curchar = None
    #font board box
    __fbbx = 0
    __fbby = 0
    __fxoff = 0
    __fyoff = 0
    #default file dir
    __outdir = 'out\\'
    __bdfdir = 'bdf\\'
    __ttfdir = 'ttf\\'
    __ymax = 0
    __ymin = 0
    #default freetype loading flag
    __my_loadflags = FT_LOAD_RENDER | FT_LOAD_TARGET_MONO


    def __init__(self, ttfname, bdfname):
        self.__ttfname = ttfname
        self.__bdfname = bdfname

    def __save_list(self, filename, codelist, param = 'w'):
        filename = self.__outdir + filename
        fh = open(filename, param)
        
        fh.writelines(codelist)

        fh.close()

    def __save_str(self, filename, str, param = 'w'):
        filename = self.__outdir + filename
        fh = open(filename, param)

        fh.write(str)

        fh.close()
    def __save_unicode_str(self, filename, str, param = 'w'):
        filename = self.__outdir + filename
        with codecs.open(filename, param, encoding='utf-16') as f:
            f.write(str)

    def __get_out_name(self, filename, charsize):
        outname = filename
        for size in [17,18]:
            if (charsize == 18):
                break
            if outname.find(str(size))>=0:
                outname = outname.replace(str(size), str(charsize))
        return outname
                        
    def __get_font_name(self, filename):
        inputfile = open(self.__bdfdir+filename,'r')
        all_the_text = inputfile.read()
        inputfile.close()

        #find all matched unicode strings
        pattern = re.compile(r'(?<=\nFONT )(.*)')
        res = pattern.search(all_the_text)
        if res:
            fontname = res.groups()[0]

        fontname = fontname[:-4] + str(self.__char_width) + str(self.__char_height)
        print fontname
        return fontname

    def __bdf_headerinfo(self, face, charcount):
        header = []

        header.append("STARTFONT 2.1\n")
        header.append("FONT %s\n" % (self.__font_name))

        header.append("SIZE %d 72 72\n" % (self.__char_size))
        if self.__is_chinese():
            header.append("FONTBOUNDINGBOX %hd %hd %hd %hd\n" % (self.__char_width, self.__fbby, self.__fxoff, self.__fyoff))
        else:
            header.append("FONTBOUNDINGBOX %hd %hd %hd %hd\n" % (self.__fbbx,self.__fbby, self.__fxoff, self.__fyoff))


        header.append("STARTPROPERTIES 2\n")
        header.append("FONT_ASCENT %hd\nFONT_DESCENT %hd\n" %
                (self.__font_ascent, self.__font_dscent))
        #imetrics = face.size;
        #header.append("FONT_ASCENT %hd\nFONT_DESCENT %hd\n" %
        #        ((face.ascender * imetrics.y_ppem) / face.units_per_EM,
        #        -((face.descender * imetrics.y_ppem) / face.units_per_EM)));
        header.append("ENDPROPERTIES\n")

        header.append("CHARS %d\n" % (charcount))

        return header


    def __get_bdfcharinfo(self, slot, charcode):
        #Calculate the scale factor for the SWIDTH field.
        swscale = self.__resolution * self.__char_size

        bitmap = slot.bitmap

        logging.info("bitmap width = %d, height = %d, pitch = %d" % (bitmap.width, bitmap.rows, bitmap.pitch))
        logging.info("bitmap left = %d, bitmap top = %d" % (slot.bitmap_left, slot.bitmap_top))
        logging.debug(bitmap.buffer)

        ##Determine the DWIDTH (device width, or advance width in TT terms) and the SWIDTH (scalable width) values.
        dwidth = slot.advance.x >> 6
        swidth = dwidth * 72000.0/swscale

        charinfo = []
        charinfo.append("STARTCHAR %04lX\n" % (charcode))
        charinfo.append("ENCODING %ld\n" % (charcode))


        bbx_w, bbx_h, bbx_xoff, bbx_yoff = self.__get_bounding(bitmap, slot.bitmap_left, slot.bitmap_top)
        
        #MTK addiontal requqiremnet: To keep the same format with the origian chinese MTK bdf files
        if bbx_w<=0:
            bbx_w = dwidth

        #MTK require the same char height, bbx_yoff for all chars, so use self.__fbby and self.__fyoff here, and adjust the buffer later
        #And bbx_xoff should not less than __fxoff
        if bbx_xoff < self.__fxoff:
            bbx_xoff = self.__fxoff
        if self.__is_chinese() and (bbx_w+bbx_xoff)>dwidth:
            dwidth = bbx_w + bbx_xoff
            swidth = dwidth * 72000.0/swscale

        if self.__is_devanagari():
            #padding_val = get_padding_val('hindi'+str(self.__char_size), self.__curchar)
            padding_val = self.__get_bbxoff_in_ref(self.__curchar)
            if (bbx_xoff != padding_val):
                if (dwidth == 0):
                    dwidth = bbx_w + padding_val
                else:
                    dwidth += (padding_val - bbx_xoff) 
                bbx_xoff = padding_val
                swidth = dwidth * 72000.0/swscale


        if self.__is_thai() and dwidth == 0:
            print "warning: dwidth = 0"
            if bbx_w + bbx_xoff <= 0:
                return self.__get_missedinfo_inref(charcode)
            dwidth = bbx_w + bbx_xoff
            swidth = dwidth * 72000.0/swscale
                    

        charinfo.append("SWIDTH %d\n" % ( swidth ))
        charinfo.append("DWIDTH %d\n" % (dwidth))

        x_shift = 0
        if (self.__is_chinese()):
            bbx_w = self.__char_width
            x_shift = bbx_xoff
            bbx_xoff = 0

        charinfo.append("BBX %ld %ld %hd %hd\n" % (bbx_w, self.__fbby, bbx_xoff, self.__fyoff))

        charinfo.append("BITMAP\n")
        dest_byte_per_row = self.__get_dest_byte_per_row(bbx_w)
        height = self.__get_dest_height()

        #rend bitmap buffer to match mtk requirement
        bf = bitmap.buffer
        bf = self.__align_buffer_height(bf, bitmap.rows, bitmap.pitch, (bbx_yoff - self.__fyoff))
        bf = self.__align_buffer_with_ref(bf, bitmap.pitch)
        bf = self.__align_buffer_width(dest_byte_per_row, bitmap.pitch, bf)
        bf = self.__shift_buffer(bf, dest_byte_per_row, x_shift)
        
        for j in range(height):
            for i in range(dest_byte_per_row):
                charinfo.append("%02lx" % bf[j*dest_byte_per_row + i])
            charinfo.append("\n")

        charinfo.append("ENDCHAR\n")

        charinfo.append(  self.__get_visible_content(bf,dest_byte_per_row,height) )
        return charinfo

    def __is_chinese(self):
        return self.__ttfname == 'SimSun.ttf'
    def __is_acsent_from_ref(self):
        return self.__ttfname.lower() == 'NokiaPureS40THAI_Rg_Leelawui.ttf'.lower() \
            or self.__bdfname.lower() == 'DevanagariMT18.bdf'.lower()
    def __is_thai(self):
        return self.__bdfname.lower() == 'ThaiMT18.bdf'.lower()
    def __is_gujarati(self):
        return self.__ttfname.lower() == 'Lohit-Gujarati_Shruti_Win7.ttf'.lower()
    def __is_devanagari(self):
        return self.__bdfname.lower() == 'DevanagariMT18.bdf'.lower()


    def __get_dest_byte_per_row(self, bbx_w):
        bytes = (bbx_w +7)/8
        if (bytes == 0):
            bytes = 1
        return bytes

    def __get_dest_height(self):
        return self.__char_height

    def __align_buffer_with_ref(self, bf, bytes_per_row):
        if (not self.__is_acsent_from_ref):
            return bf
        if (self.__curchar == 0x0937):
            abc = 1
        top_in_ref, bottom_in_ref = self.__get_top_in_ref()
        top = self.__get_top(bf, bytes_per_row)
        if (top - top_in_ref):
            print "align wih ref"
            bottom = self.__get_bottom(bf, bytes_per_row)
            if (bottom - top) != (bottom_in_ref - top_in_ref):
                print (str(self.__curchar) + " height not mattched!")
        
        bf = self.__align_buffer_height(bf, self.__char_height, bytes_per_row, top - top_in_ref)
        return bf;

    def __get_top(self, bf, bytes_per_row):
        for i in range(self.__char_height):
            for j in range(bytes_per_row):
                if bf[i*bytes_per_row +j]:
                    return i
        return 0
    def __get_bottom(self, bf, bytes_per_row):
        for i in range(self.__char_height,0,-1):
            for j in range(bytes_per_row):
                if bf[(i-1)*bytes_per_row +j]:
                    return i-1
        return 0
 
    def __get_top_in_ref(self):
        char_content = self.__get_code_content_in_ref(self.__curchar)
        bf, bytes_per_row = self.__get_bytes_buffer(char_content)
        
        return self.__get_top(bf, bytes_per_row), self.__get_bottom(bf, bytes_per_row);

    def __align_buffer_height(self, bf, rows, byte_per_row_inbuffer, bottom_indent):
        if (self.__ymax + bottom_indent) > self.__char_height:
            bottom_indent = max(self.__char_height - self.__ymax, 0)
        if (self.__ymin + bottom_indent) < 0:
            bottom_indent = -self.__ymin

        top_indent = (self.__char_height - rows - bottom_indent)
        newbf = bf
        #align the buffer height to the font size
        if (top_indent < 0):
            newbf = bf[-top_indent*byte_per_row_inbuffer:]
        else:
            for i in range(top_indent*byte_per_row_inbuffer):
                newbf.insert(0,0)

        if (bottom_indent > 0):
            for i in range(bottom_indent*byte_per_row_inbuffer):
                newbf.append(0)

        #Update ymax and ymin, used in align buffer in height, to avoid discarding real point
        self.__ymax = self.__char_height - self.__get_top(newbf, byte_per_row_inbuffer)
        self.__ymin = self.__char_height - self.__get_bottom(newbf, byte_per_row_inbuffer) -1

        return newbf


    def __align_buffer_width(self, dest_byte_per_row, byte_per_row_inbuffer, bf):
        #align the buffer width to the dest_byte_per_row
        if (dest_byte_per_row>byte_per_row_inbuffer):
            for i in range(self.__char_height):
                for j in range(dest_byte_per_row-byte_per_row_inbuffer):
                    bf.insert(i*dest_byte_per_row+byte_per_row_inbuffer, 0)
        else:
            if (dest_byte_per_row<byte_per_row_inbuffer):
                newbf = []
                for i in range(self.__char_height):
                    newbf.extend(bf[i*byte_per_row_inbuffer:i*byte_per_row_inbuffer+dest_byte_per_row])
                bf = newbf
        return bf

    #shift bitmap buffer x_shift right
    def __shift_buffer(self, bf, byte_per_row, x_shift):
        if (x_shift<=0):
            return bf
        for i in range(self.__char_height):
            dest = 0L
            for j in range(byte_per_row):
                dest |= bf[i*byte_per_row + j]
                dest <<= 8
            dest >>=8
            dest >>= x_shift
            mask = 0xff
            for j in range(byte_per_row,0,-1):
                bf[i*byte_per_row + j-1] = int(dest&mask)
                dest>>=8
                
                
        return bf

    def __get_visible_content(self, buffer,dest_byte_per_row,height):
        if (not VISUAL_MODE):
            return ''

        strlist = []
        for i in range(height):
            temp = ''
            for j in range(dest_byte_per_row):
                binstr = bin(buffer[i*dest_byte_per_row+j])
                temp += binstr[2:].zfill(8)
            temp = temp.replace('0','-')
            temp = temp.replace('1','#')
            strlist.append(temp)
        return '\n'.join(strlist) + '\n'
            

    def __get_font_bounding(self, face, codelist):
        #get bounding box of all given fonts
        bbx_maxas=bbx_maxds=bbx_rbearing=bbx_maxrb=bbx_minlb=0
        slot = face.glyph
        for charcode in codelist:
            self.__curchar = charcode
            gindex = face.get_char_index(charcode)
            if (gindex <= 0):
                continue
            face.load_glyph(gindex, self.__my_loadflags) 
            (wd, ht, xoff, yoff) = self.__get_bounding(slot.bitmap, slot.bitmap_left, slot.bitmap_top)

#            print "code %x yoff is: %d, bitmaptop is %d" % (self.__curchar, yoff, slot.bitmap_top)
            bbx_maxas = max(bbx_maxas, ht + yoff)
            bbx_maxds = max(bbx_maxds, -yoff)
            bbx_rbearing = wd + xoff
            bbx_maxrb = max(bbx_maxrb, bbx_rbearing)
            bbx_minlb = min(bbx_minlb, xoff)

        self.__fbbx = bbx_maxrb - bbx_minlb
        self.__fbby = bbx_maxas + bbx_maxds
        self.__fxoff = bbx_minlb
        self.__fyoff = -bbx_maxds

        #MTK addition requirment: BBh should equal to font height,BBXoffset should be 0  
        self.__fbbx = bbx_maxrb - 0
        self.__fxoff = 0
        self.__fbby = self.__char_height

        self.__font_dscent = bbx_maxds
        self.__font_ascent = self.__char_height - bbx_maxds
        if self.__is_acsent_from_ref():
            self.__get_ascent_inref()

    def __get_bounding(self, bitmap, left, top):
        sx = sy = 0xffff;
        ex = ey = 0;
        bp = bitmap.buffer;
        for  y in range(bitmap.rows):
            for x in range(bitmap.width):
                if (bp[(bitmap.pitch*y) + (x >> 3)] & (0x80 >> (x & 7))) :
                    if (x < sx):
                        sx = x
                    if (x > ex):
                        ex = x
                    if (y < sy):
                        sy = y
                    if (y > ey):
                        ey = y
            

        if (sx == 0xffff and sy == 0xffff and ex == 0 and ey == 0):
            sx = ex = sy = ey = 0
        else:
            ex+=1
            ey+=1

        wd = ex - sx;
        ht = ey - sy;
        xoff = sx + left;
        #yoff = sy + top - bitmap.rows;
        yoff = top - bitmap.rows
        
        #MTK addition requirment: BBX width caculate from 0 to the right most point
        wd = ex
        xoff = left
        #used in align buffer in height, to avoid discarding real point
        self.__ymin = bitmap.rows - ey
        self.__ymax = bitmap.rows - sy
#        yoff = top - bitmap.rows
        #MTK addition requirment: the FONTBOUNDINGBOX xoff should be 0, so here xoff shouldnot be less than 0
        if (xoff < 0):
           xoff = 0

        if (ht )>self.__char_height:
            print hex(self.__curchar) + "exceed height"
        #if (bitmap.rows>self.__char_height):
        #    print "bitmap.rows = %d exceed the height, charcode =%lx " % (bitmap.rows, self.__curchar)

        return (wd, ht, xoff, yoff)


    def __get_code_in_bdf(self, filename):
        #return [0x91cf,0x529b,0x3002]
        code_list_ret = []
        logging.info('pocessing ' + filename)
        inputfile = open(self.__bdfdir+filename,'r')
        all_the_text = inputfile.read()
        inputfile.close()

        #find all matched unicode strings
        pattern = re.compile(r'(?<=STARTCHAR )[0-9A-Fa-f]{4}')
        code_list = pattern.findall(all_the_text)
        code_list.sort()

        #convert string format to char code
        for code in code_list:
            charcode = int(code, 16)
            code_list_ret.append(charcode)
        return code_list_ret


    def __get_face(self, filename, width, height):
        face = Face(self.__ttfdir+filename)
        if (self.__is_gujarati() or self.__is_devanagari()):
            width -= width/6
            height -= height/6

        face.set_pixel_sizes(width,height)
    #    face.set_char_size(width*64,height*64,self.__resolution,self.__resolution)

        face.select_charmap(FT_ENCODING_UNICODE)

        print("family_name = %s" % face.family_name)
        return face

    def __get_ascent_inref(self):
        bdfname = self.__get_out_name(self.__bdfname, self.__char_size)
        inputfile = open(self.__bdfdir+bdfname,'r')
        all_the_text = inputfile.read()
        inputfile.close()
        
        asc = re.findall(r'(?<=FONT_ASCENT )\d+', all_the_text)
        if (len(asc)>0):
            ascv = int(asc[0], 10)
            self.__font_ascent = ascv
            self.__font_dscent = self.__char_height - ascv
            self.__fyoff = -self.__font_dscent



    #Try to use the definition in reference bdf file for those unicode char missed in ttf
    def __get_missedinfo_inref(self, code):
        char_content = self.__get_code_content_in_ref(code)
        if char_content:
           char_content = self.__render_bitmap_info(char_content)
        return char_content

    def __get_code_content_in_ref(self, code):
        bdfname = self.__get_out_name(self.__bdfname, self.__char_size)
        inputfile = open(self.__bdfdir+bdfname,'r')
        all_the_text = inputfile.read()
        inputfile.close()

        char_content = ''
        codestr = "%04lx" % code
        matchstr = r'(STARTCHAR\s' + codestr + r'[\s\S]*?ENDCHAR\n)'
        matchres = re.search(matchstr, all_the_text, re.IGNORECASE)
        if matchres:
            char_content = matchres.groups()[0]
        return char_content

    def __get_bbxoff_in_ref(self, code):
        char_content = self.__get_code_content_in_ref(code)
        bbxoff = 0
        repattern = r'(BBX (\d+) (\d+) (\d+) )(-?\d+)'
        matchres = re.search(repattern, char_content)
        if matchres:
            bbxoff = int( matchres.groups()[3], 10)

        return bbxoff

    def __get_bytes_buffer(self, char_content):
        bf = []
        byte_per_row = 0

        buffer_pattern = r'BITMAP\n((([0-9a-fA-F]+)\n)+)ENDCHAR'
        matchres = re.search(buffer_pattern, char_content)
        if (matchres):
            bf_str = matchres.group(1)
            bfs = re.findall(r'[0-9a-fA-F]+', bf_str)

            rows = len(bfs)
            #get bitmap buffer in file
            for line in bfs:
                bytes = re.findall(r'.{2}', line)
                for byte in bytes:
                    value = int(byte,16)
                    bf.append(value)
            byte_per_row = len(bf)/rows

        return bf, byte_per_row

    def __render_bitmap_info(self, char_content):
        #change the bbx_of to the converted value
        repattern = r'(BBX (\d+) (\d+) (\d+) )(-?\d+)'
        matchres = re.search(repattern, char_content)
        if matchres:
            bbyoff = int( matchres.groups()[4], 10)
            replacestr = matchres.groups()[0] + str(self.__fyoff)
            #extend FBBX if need
            width = int(matchres.groups()[1],10) + int(matchres.groups()[3])
            if (width > self.__fbbx):
                self.__fbbx = width

            char_content = re.sub(repattern, replacestr, char_content)
            char_content = self.__render_bitmap_buffer(char_content, bbyoff-self.__fyoff)
        return char_content
 
    def __render_bitmap_buffer(self, char_content, bottom_intent ):
        bf, byte_per_row = self.__get_bytes_buffer(char_content)

        #used in align buffer in height, to avoid discarding real point
        self.__ymax = self.__char_height - self.__get_top(bf, byte_per_row)
        self.__ymin = self.__char_height - self.__get_bottom(bf, byte_per_row) -1

        # align the buffer with new bbyoff
        bf = self.__align_buffer_height(bf, self.__char_height, byte_per_row, bottom_intent)

        # return the BITMAP 
        bf_str_list=['BITMAP']
        for j in range(self.__char_height):
            line = ''
            for i in range(byte_per_row):
                line += "%02lx" % bf[j*byte_per_row + i]
            bf_str_list.append(line)
        bf_str_list.append('ENDCHAR')

        buffer_pattern = r'BITMAP\n((([0-9a-fA-F]+)\n)+)ENDCHAR'
        char_content = re.sub(buffer_pattern, '\n'.join(bf_str_list), char_content)
        return char_content
 
    def __convert_to_bdf_with_code(self, face, codelist):
        content = []
        slot = face.glyph
        missed = []
        charcount = 0
        for charcode in codelist:
            self.__curchar = charcode
            gindex = face.get_char_index(charcode)
            if (gindex<=0):
                logging.warning("Code %lX is not found in the ttf file")
                missed.append(charcode)
                #continue
                content += self.__get_missedinfo_inref(charcode)
            else:
                logging.info("      0x%04lx => %d" % (charcode, gindex))
                
                face.load_glyph(gindex, self.__my_loadflags) 
                content += self.__get_bdfcharinfo(slot, charcode)
            charcount += 1

        content.append("ENDFONT\n")
        header = self.__bdf_headerinfo(face, charcount)
        content = header + content

        return (content,missed)
    
    def do_convert(self):
        char_sizes = [18, 22, 26]
        if (self.__is_chinese()):
            char_sizes = [18, 22]

        for charsize in char_sizes:
            self.__char_width = self.__char_height = self.__char_size = charsize
            self.__font_ascent = charsize
            self.__font_dscent = 0

            if (self.__is_chinese() and self.__char_width == 18):
                self.__char_width = 17

            print ("Converting %s to bdf file, width = %d, height = %d, codes defined in %s" % (self.__ttfname, self.__char_width, self.__char_height, self.__bdfname))
            face = self.__get_face(self.__ttfname, self.__char_width, self.__char_height)

            self.__font_name = self.__get_font_name(self.__bdfname)
            codeused = self.__get_code_in_bdf(self.__bdfname)
            self.__save_unicode_str(self.__bdfname+"usedcode.txt", ''.join(map(uni_info, codeused)))

            outputfile = self.__get_out_name(self.__bdfname, charsize)
            if (VISUAL_MODE):
                outputfile += "visual"

            self.__get_font_bounding(face, codeused)

            content, missed = self.__convert_to_bdf_with_code(face, codeused)
            self.__save_list(outputfile, content)
            self.__save_list(self.__bdfname+"missed.txt", '\n'.join(map(hex, missed)))



def font_matching_convert():
    font__match_table = {
        'Lohit-Gujarati_Shruti_Win7.TTF':['GujaratiMT18.bdf'],
        'Lohit-Oriya_kalinga.ttf':['OriyaMT18.bdf'],
        'mm3_ZawgyiOne2015.ttf':['MyanmarZawgyi18.bdf'],
        'Lohit-Punjabi_Raavi.TTF':['GurmukhiMT18.bdf'],
        'SimSun.ttf':['CESI_1718_GB2312.bdf','CESI_1718.bdf'],
        'NokiaPureS40ARAB_Rg_Segoe_UI.ttf':['ArabicMT18.bdf'],
        'NokiaPureS40CYRL_Rg_Segoe_UI.ttf':['nsnrCyrillic18.bdf'],
        'NokiaPureS40LATN_Rg_Segoe_UI.ttf':['NOSNR18.bdf'],
        'NokiaPureS40ARMN_Rg_Segoe_UI.ttf':['ArmenianMT18.bdf'],
        'NokiaPureS40BENG_Rg_Vrinda.TTF':['BengaliMT18.bdf'],
        'NokiaPureS40DEVA_Rg_Mangal_Win7.ttf':['DevanagariMT18.bdf'],
        'NokiaPureS40ETHI_Rg_Ebrima.ttf':['EthiopicMT18.bdf'],
        'NokiaPureS40GEOR_Rg_Segoe_UI.ttf':['GeorgianMT18.bdf', 'nsnrGreek18.bdf'],
        'NokiaPureS40HEBR_Rg_Segoe_UI.ttf':['HebrewMT18.bdf'],
        'NokiaPureS40KHMR_Rg_Leelawui_win10.ttf':['KhmerMT18.bdf','LeeLao18.bdf'],
        'NokiaPureS40KNDA_Rg_Tunga_Win7.ttf':['KannadaMT18.bdf'],
        'NokiaPureS40MLYM_Rg_Kartika_Win7.ttf':['MalayalamMT18.bdf'],
        'NokiaPureS40SINH_Rg_iskpota.ttf':['SinhalaMT18.bdf'],
        'NokiaPureS40TAML_Rg_Latha_Win7.ttf':['TamilMT18.bdf'],
        'NokiaPureS40TELU_Rg_Gautami_Win7.ttf':['TeluguMT18.bdf'],
        'NokiaPureS40THAI_Rg_Leelawui.ttf':['ThaiMT18.bdf'],
    }
    #font__match_table = {
    #    'SimSun.ttf':['CESI_1718_GB2312.bdf','CESI_1718.bdf'],
    #} 
    font__match_table = {
        'NokiaPureS40DEVA_Rg_Mangal_Win7.ttf':['DevanagariMT18.bdf'],
    } 
    for fontfile in font__match_table.keys():
        filter_file_list = font__match_table[fontfile]
        for filter_file in filter_file_list:
            convertor = otf2bdf(fontfile, filter_file)
            convertor.do_convert()
            

def uni_info(code):
    return unicode(hex(code)) + u':' + unichr(code) + u'  '

def main():
    #ttf files should be put under .\ttf , origial bdf files should be put under .\bdf, 
    #converted bdf files will be saved to .\out
    global VISUAL_MODE

    opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "visual"])

    for op, value in opts:
        if op == '-v' or op == '--visual':
            VISUAL_MODE = True
        elif op == '-h':
            usage()
            sys.exit()

    init_padding()
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='convertor.log',
                filemode='w')
    logging.info('********************Start converting process******************************')
    path = os.path.join(os.getcwd(), 'out')
    if not os.path.exists(path):
        os.mkdir(path)
    

    
    font_matching_convert()

    logging.info('********************End process******************************')


class A(object):
    def __init__(self):
        self.x = 10
    def increase(self):
        self.do_increase()
        print "x is " + str(self.x)
    def do_increase(self):
        print "in A"
        self.x+=1
class B(A):
    def do_increase(self):
        print "in B"
        self.x += 2
if __name__ == "__main__":
    #a = A()
    #b = B()
    #a.increase()
    #b.increase()

    main()


