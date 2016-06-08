#!/usr/bin/python
import openpyxl
from myutility import *

class ExcelInfoFilter(object):
    def __init__(self, filename):
        self._ws = openpyxl.load_workbook(filename = fulldatapath(filename), read_only=True ).active
    def get_en_feedback(self):
        #Get original EN feedback and split feedback by '.'
        feedbacks=[]
        feedbacks_withIDs = []
        lang_column = None
        feedback_column = None
        for row_index, row in enumerate(self._ws.iter_rows()):
            if row_index == 0: #find the language and feedback column
                for i, cell in enumerate(row):
                    if "Language" == cell.value:
                        lang_column = i
                    elif "Original Feedback" == cell.value:
                        feedback_column = i
            elif lang_column and feedback_column:
                if row[lang_column].value == "en":
                    for subid, subsent in enumerate(split_sentence(row[feedback_column].value)):
                        feedbacks_withIDs.append((row_index, subid, subsent))

        return feedbacks_withIDs

    def get_correct_en_feedback(self):
        # remove wrong feedback and try to fix wrong-spelled word
        feedbacks_withIDs = self.get_en_feedback()
        correct_fd_IDs = []
        for id_and_feedback in feedbacks_withIDs:
            if not is_wrong_sentence(id_and_feedback[2]):
                corrected, changed_words = correct_sent(id_and_feedback[2])
                correct_fd_IDs.append((id_and_feedback[0], id_and_feedback[1], corrected))
                #print some debug info, can be removed
                if (id_and_feedback[0] < 100):
                    print ("index %d: %s, %s, %s " % (id_and_feedback[0], id_and_feedback[2], corrected, changed_words))
            else:
                print "wrong line index %d: %s" % (id_and_feedback[0], id_and_feedback[2])

        return correct_fd_IDs



if __name__ == "__main__":
    exl = ExcelInfoFilter("npsfeedback_test.xlsx")
    #exl = ExcelInfoFilter("npsfeedback-searchresults-2016-04-22T07_45.xlsx")
    exl.get_correct_en_feedback()



