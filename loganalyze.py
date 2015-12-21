
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#1.	The successful rate for recording voice
#2.	The successful rate for the voice uploading
#3.	The successful rate for the voice to Text rate
#4.	The successful rate for the LUIS understanding
#5.	The successful rate for the whole function.
# -----------------------------------------------------------------------------
import re
import logging
import os
import os.path
import argparse
import getopt
import sys
import time

class LogInfo(object):
    __content = ''
    __content_list = []
    def __init__(self, filename):
        self.__filename = filename
        fh = open(filename, 'r')
        self.__content = fh.read()
        self.__content_list = self.__content.split('\\n')
        fh.close()
        
    def is_service_start(self):
        return  self.__content.find('[service]') > -1
    def is_upload_start(self):
        return  self.__content.find('[voice upload]') > -1
    def is_stt_start(self):
        return  self.__content.find('[STT]') > -1
    def is_luis_start(self):
        return  self.__content.find('[LUIS]') > -1
    def is_tts_start(self):
        return  self.__content.find('[TTS]') > -1
    def is_record_start(self):
        return self.__content.find('[record]') > -1


    def is_service_ok(self):
        return  self.__content.rfind('[service ok]') > -1
    def is_upload_ok(self):
        return  self.__content.rfind('[voice upload ok]') > -1
    def is_stt_ok(self):
        return  self.__content.rfind('[STT ok]') > -1
    def is_luis_ok(self):
        return  self.__content.rfind('[LUIS ok]') > -1
    def is_tts_ok(self):
        return  self.__content.rfind('[TTS ok]') > -1
    def is_record_ok(self):
        return self.__content.rfind('[record ok]') > -1



    def last_key(self, keyword):
        reversed_list = self.__content_list[::-1]
        for line in reversed_list:
            if line.find(keyword) > -1:
                return line
 
    def last_ok(self):
        return self.last_key(' ok]')
    def last_fail(self):
        return self.last_key(' fail]')
        


def save_str(filename, str, param = 'w'):
    fh = open(filename, param)
    fh.write(str)
    fh.close()

def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path + '\\'
     elif os.path.isfile(path):
         return os.path.dirname(path) +'\\'
     
def get_logfile_list(folder):
    ret_list = []
    for rt, dirs, files in os.walk(folder):
        for f in files:
            if (f[-7:] == 'log.txt'):
                ret_list.append(f)
            #fname = os.path.splitext(f)
    return ret_list


def analyze_log_dir(folder):

    logfiles = get_logfile_list(folder)
    service_ok = ttsok_count = luisok_count = sttok_count = uploadok_count = recordok_count = 0

    service_start = ttsstart_count = luisstart_count = sttstart_count = uploadstart_count = recordstart_count = 0
    count = len(logfiles)
    if (count ==0):
        print "No log files found, please check your input folder"
        return

    for logfile in logfiles:
        loginfo = LogInfo(folder + '\\' + logfile)
        if (loginfo.is_service_start()):
            service_start+=1
        if (loginfo.is_luis_start()):
            luisstart_count +=1
        if loginfo.is_stt_start():
            sttstart_count +=1
        if loginfo.is_tts_start():
            ttsstart_count +=1
        if loginfo.is_upload_start():
            uploadstart_count += 1
        if loginfo.is_record_start():
            recordstart_count += 1
            
        if (loginfo.is_service_ok()):
            service_ok+=1
        if (loginfo.is_luis_ok()):
            luisok_count +=1
        if loginfo.is_stt_ok():
            sttok_count +=1
        if loginfo.is_tts_ok():
            ttsok_count +=1
        if loginfo.is_upload_ok():
            uploadok_count += 1
        if loginfo.is_record_ok():
            recordok_count += 1
    localtime = time.asctime( time.localtime(time.time()) )
    report = []
    report.append("***************** Adya user experience results till %s*****************" % str(localtime))
    report.append("******************The rate is caculated for the specific action which has been started***********************")
    report.append("Successful rate for recording voice:(%d/%d) %.4f " % (recordok_count, recordstart_count, 1.0 * recordok_count/recordstart_count))
    report.append("Successful rate for voice upload:(%d/%d) %.4f " % (uploadok_count, uploadstart_count, 1.0 * uploadok_count/uploadstart_count))
    report.append("Successful rate for voice to text(stt):(%d/%d) %.4f " % (sttok_count, sttstart_count, 1.0 * sttok_count/sttstart_count))
    report.append("Successful rate for LUIS understanding:(%d/%d) %.4f " % (luisok_count, luisstart_count, 1.0 * luisok_count/luisstart_count))
    report.append("Successful rate for TTS ok:(%d/%d) %.4f " % (ttsok_count, ttsstart_count, 1.0 * ttsok_count/ttsstart_count))
    report.append("Successful rate of whole function:(%d/%d) %.4f " % (service_ok, count, 1.0 * service_ok/service_start))
    report.append("======================================End==============================================\n\n")
    save_str(cur_file_dir() + 'report.txt', '\n'.join(report), 'a')

def usage():
        print sys.argv[0] + ' -i log folder, default will be .\\log\\'
        print sys.argv[0] + ' -h #get help info'

def main():
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "input=", "output="])
    logfolder = '.\\log'

    for op, value in opts:
        if op == '-i' or op == '--input':
            logfolder = value
        elif op == '-h':
            usage()
            sys.exit()

    analyze_log_dir(logfolder)


if __name__ == "__main__":
    main()


