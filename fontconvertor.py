#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
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
import argparse

class otf2bdf(object):
    __ttfname = ''
    __bdfname = ''
    __resolution = 72
    __font_name = "" 
    __char_width = 18
    __char_height = 18
    __char_size = 18
    #font board box
    __fbbx = 0
    __fbby = 0
    __fxoff = 0
    __fyoff = 0
    #default file dir
    __outdir = 'out\\'
    __bdfdir = 'bdf\\'
    __ttfdir = 'ttf\\'
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

    def __get_out_name(self, filename, charsize):
        outname = filename
        for size in [17,18,22]:
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
        if (bbx_w+bbx_xoff)>dwidth:
            dwidth = bbx_w + bbx_xoff

        charinfo.append("SWIDTH %d\n" % ( swidth ))
        charinfo.append("DWIDTH %d\n" % (dwidth))

        charinfo.append("BBX %ld %ld %hd %hd\n" % (bbx_w, self.__fbby, bbx_xoff, self.__fyoff))

        charinfo.append("BITMAP\n")
        dest_byte_per_row = self.__get_dest_byte_per_row(bbx_w)
        height = self.__get_dest_height()

        #rend bitmap buffer to match mtk requirement
        bf = bitmap.buffer
        bf = self.__align_buffer_height(bf, bitmap.rows, bitmap.pitch, (bbx_yoff - self.__fyoff))
        bf = self.__align_buffer_width(dest_byte_per_row, bitmap.pitch, bf)
        
        for j in range(height):
            for i in range(dest_byte_per_row):
                charinfo.append("%02lx" % bf[j*dest_byte_per_row + i])
            charinfo.append("\n")

        charinfo.append("ENDCHAR\n")

    #    charinfo.append(  get_visible_content(bf,dest_byte_per_row,height) )
        return charinfo

    def __is_chinese(self):
        return self.__ttfname == 'SimSun.ttf'

    def __get_dest_byte_per_row(self, bbx_w):
        bytes = (bbx_w +7)/8
        if (self.__is_chinese()):
             bytes = (self.__char_width + 7)/8
        if (bytes == 0):
            bytes = 1
        return bytes

    def __get_dest_height(self):
        return self.__char_height

    def __align_buffer_height(self, bf, rows, byte_per_row_inbuffer, bottom_indent):
        #bottom_indent should >= 0
        if (bottom_indent<0):
            print ("error: bottem_indent<0")

        top_indent = (self.__char_height - rows - bottom_indent)
        newbf = bf
        #align the buffer height to the font size
        if (top_indent < 0):
            newbf = bf[-top_indent*byte_per_row_inbuffer:]
        else:
            for i in range(top_indent*byte_per_row_inbuffer):
                newbf.insert(0,0)

        for i in range(bottom_indent*byte_per_row_inbuffer):
            newbf.append(0)

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


    def __get_visible_content(self, buffer,dest_byte_per_row,height):

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
        yoff = sy + top - bitmap.rows;
        
        #MTK addition requirment: the FONTBOUNDINGBOX xoff should be 0, so here xoff shouldnot be less than 0
        if (xoff < 0):
           xoff = 0

        if (ht )>self.__char_height:
            print hex(self.__curchar) + "exceed height"
        #if (bitmap.rows>self.__char_height):
        #    print "bitmap.rows = %d exceed the height, charcode =%lx " % (bitmap.rows, self.__curchar)

        return (wd, ht, xoff, yoff)


    def __get_code_in_bdf(self, filename):
        #return [0x00a4,0x718a,0x9878]
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
        face.set_pixel_sizes(width,height)
    #    face.set_char_size(width*64,height*64,self.__resolution,self.__resolution)

        face.select_charmap(FT_ENCODING_UNICODE)

        print("family_name = %s" % face.family_name)
        return face


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
                continue

            logging.info("      0x%04lx => %d" % (charcode, gindex))
            #if (self.__char_width<=18):
            #    my_loadflags = FT_LOAD_RENDER | FT_LOAD_TARGET_MONO | FT_LOAD_NO_HINTING |FT_LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH
            
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
            self.__save_list(self.__bdfname+"usedcode.txt", '\n'.join(map(hex, codeused)))
            outputfile = self.__get_out_name(self.__bdfname, charsize)

            self.__get_font_bounding(face, codeused)

            content, missed = self.__convert_to_bdf_with_code(face, codeused)
            self.__save_list(outputfile, content)
            self.__save_str(self.__bdfname+"missedcode.txt", '\n'.join(map(hex,missed)))



def font_matching_convert():
    font__match_table = {
        'Lohit-Gujarati_Shruti_Win7.TTF':['GujaratiMT18.bdf'],
        'Lohit-Oriya_kalinga.ttf':['OriyaMT18.bdf'],
        'mm3_ZawgyiOne2015.ttf':['MyanmarZawgyi18.bdf'],
        'Lohit-Punjabi_Raavi.TTF':['GurmukhiMT18.bdf'],
#        'SimSun.ttf':['CESI_1718_GB2312.bdf','CESI_1718.bdf'],
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
    font__match_table = {
        'SimSun.ttf':['CESI_1718_GB2312.bdf','CESI_1718.bdf'],
    } 
    #font__match_table = {
    #    'NokiaPureS40LATN_Rg_Segoe_UI.ttf':['NOSNR18.bdf'],
    #} 
    for fontfile in font__match_table.keys():
        filter_file_list = font__match_table[fontfile]
        for filter_file in filter_file_list:
            convertor = otf2bdf(fontfile, filter_file)
            convertor.do_convert()
            

def main():
    #ttf files should be put under .\ttf , origial bdf files should be put under .\bdf, 
    #converted bdf files will be saved to .\out

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



if __name__ == "__main__":
    main()


