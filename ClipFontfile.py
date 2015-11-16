import os
import os.path
import re
import logging


def get_used_code_fromdat(filelist):
    code_list_ret = []
    for filename in filelist:
        logging.info('pocessing ' + filename)
        inputfile = open('txt\\'+filename,'r')
        all_the_text = inputfile.read()

        #find all matched unicode strings
        pattern = re.compile(r'(?<=\")[0-9A-Fa-f]*(?=")')
        matched_strings = pattern.findall(all_the_text)

        #get each unicode and filter by set
        matched_strings = ''.join(matched_strings)
        pattern2 = re.compile(r'[0-9A-Fa-f]{4}')
        code_list = pattern2.findall(matched_strings)

#        save_list(filename + ".dat", code_list)
        code_list_ret += code_list
        inputfile.close()

    code_list_ret = list(set(code_list_ret))
    code_list_ret.sort()

#    save_list("tout2.txt", code_list_ret)
#    save_list_byline("tout3.txt", code_list_ret)
    return code_list_ret



def filter_code_in_fontfile(filename, codelist):
    logging.info('filter ' + filename)

    content_ret = ''
    inputfile = open('bdf\\' + filename,'r')
    all_the_text = inputfile.read()

    #find the head
    head_pattern = re.compile(r'([\s\S]*?)CHARS \d+')
    head = head_pattern.search(all_the_text)
    headstr = ''
    if head:
        headstr = head.groups()[0]

    #find all code definition in codelist from fontfile
    code_definitions = []
    for code in codelist:
        matchstr = r'(STARTCHAR\s' + code + r'[\s\S]*?ENDCHAR\n)'
        matchres = re.search(matchstr, all_the_text, re.IGNORECASE)
        if matchres:
            code_definitions.append( matchres.groups()[0] )
        else:
            logging.warn(code + ' is not matched in ' + filename)

    #output
    headstr += 'CHARS ' + str(len(code_definitions)) +'\n'
    content_ret = headstr + ''.join(code_definitions) + 'ENDFONT\n'

    inputfile.close()
    return content_ret


def save_str(filename, str, param = 'w'):
    filename = 'out\\' + filename
    fh = open(filename, param)
    fh.write(str)
    fh.close()


def save_list(filename, codelist, param = 'w'):
    filename = 'out\\' + filename
    fh = open(filename, param)
    fh.writelines(codelist)
    fh.close()


def save_list_byline(filename, codelist, param = 'w'):
    filename = 'out\\' + filename
    fh = open(filename, param)
    fh.write('\n'.join(codelist))
    fh.close()

def get_filename_list(folder):
    for rt, dirs, files in os.walk(folder):
       return files
#        for f in files:
            #fname = os.path.splitext(f)



def matchingtable_filter():
    #todo: read from a matching file
    #file_match_table = {'EthiopicMT26':['Amharic'], 
    #                    'ArabicMT26':['Arabic','pushto','urdu'],
    #                    'ArmenianMT26':['Armenian'],
    #                    'BengaliMT26':['Assamese'],
    #                    'nsnrCyrillic26':['belarusian','Bulgarian','Kazakh','kirghiz','Macedonian','Mongolian','russian','tajik','ukrainian'],
    #                    'BengaliMT26':['bengali-bd','bengali-in'],
    #                    'CESI_1726':['chinese-hk','chinese-tw'],
    #                    'CESI_1718_GB2312':['chinese-cn'],
    #                    'ArabicMT26':['persian-fa','pushto'],
    #                    'GeorgianMT26':['Georgian'],
    #                    'nsnrGreek26':['Greek'],
    #                    'GujaratiMT26':['Gujarati'],
    #                    'HebrewMT26':['Hebrew'],
    #                    'DevanagariMT26':['Hindi','Marathi'],
    #                    'KannadaMT26':['Kannada'],
    #                    'KhmerMT26':['Khmer'],
    #                    'MalayalamMT26':['Malayalam'],
    #                    'OriyaMT26':['Oriya'],
    #                    'GurmukhiMT26':['punjabi'],
    #                    'SinhalaMT26':['sinhala'],
    #                    'TamilMT26':['Tamil'],
    #                    'TeluguMT26':['Telugu'],
    #                    'ThaiMT26':['Thai'],
    #                    'MyanmarZawgyi26':['Burmese'],
    #                    }
    
    #for fontfile in file_match_table.keys():
    #    used_code_list = get_used_code_fromdat(file_match_table[fontfile])
    #    save_list_byline(fontfile+'usedcode.txt', used_code_list)

    #    clipped_content = filter_code_in_fontfile(fontfile+'.bdf', used_code_list)
    #    save_str(fontfile+'_clip.bdf', clipped_content)    
    file_match_table = {'CESI_1718.bdf':['chinese-hk.txt','chinese-tw.txt'],
                        'CESI_1718_GB2312.bdf':['chinese-cn.txt'],
                        'CESI_2222.bdf':['chinese-hk.txt','chinese-tw.txt'],
                        'CESI_2222_GB2312.bdf':['chinese-cn.txt'],                        	
                        }
    
    for fontfile in file_match_table.keys():
        used_code_list = get_used_code_fromdat(file_match_table[fontfile])
        save_list_byline(fontfile+'usedcode.txt', used_code_list)

        clipped_content = filter_code_in_fontfile(fontfile, used_code_list)
        print ("Clipping " + fontfile)
        save_str(fontfile, clipped_content)    
		
	
def allused_filter():
    datfiles = get_filename_list('.\\txt\\')
    print ("Get all used unicode under txt folder...")
    used_code_list = get_used_code_fromdat(datfiles)
    save_list_byline('allusedcode.txt', used_code_list)

    bdffiles = get_filename_list('.\\bdf\\')
    for fontfile in bdffiles:
        print ("Clipping " + fontfile)
        clipped_content = filter_code_in_fontfile(fontfile, used_code_list)
        save_str(fontfile, clipped_content)	
        
        
def main():
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='a')

    logging.info('********************Start process******************************')
    path = os.path.join(os.getcwd(), 'out')
    if not os.path.exists(path):
        os.mkdir(path)

    matchingtable_filter()
    #allused_filter()

       




    logging.info('********************End process******************************')

if __name__ == '__main__':
    main()
