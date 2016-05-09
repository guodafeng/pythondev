import sys
import textmining
import nltk
import re
import os
import codecs
import enchant
from nltk.metrics import edit_distance
from autocorrect import spell
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

D_LEVEL = 1
wrong_words = []
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(["n't", "aren't", "doesn't","don't", "i'm", "i'v","i'll", "can't", "couldn't"])
CUR_DIR = os.getcwd()

# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")   

def d_print(info):
    if D_LEVEL==0:
        return
    print info

def fulldatapath(filename):
    return ".\\data\\" + filename

def save_list(filename, lines, param = 'w'):
    fh = open(fulldatapath(filename), param)
    fh.writelines('\n'.join(lines))
    fh.close()
def read_list_in_file(filename):
    fh = open(fulldatapath(filename), 'r')
    lines = fh.readlines()
    fh.close()
    return lines

class SpellingReplacer(object):
    def __init__(self, dict_name = 'en_US', mywords = 'mywords.txt', max_dist = 2):
        self.spell_dict = enchant.DictWithPWL(dict_name, fulldatapath(mywords))
        self.max_dist = 2

    def replace(self, word):
        if len(word)<3 or self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)

        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word
    def testword(self, word):
        return self.spell_dict.check(word)


def termdocumentmatrix(doclines):
    tdm = textmining.TermDocumentMatrix()
    # Add the documents
    for doc in doclines:
        tdm.add_doc(doc)
    # Write out the matrix to a csv file. Note that setting cutoff=1 means
    # that words which appear in 1 or more documents will be included in
    # the output (i.e. every word will appear in the output). The default
    # for cutoff is 2, since we usually aren't interested in words which
    # appear in a single document. For this example we want to see all
    # words however, hence cutoff=1.
    tdm.write_csv(fulldatapath('matrix.csv'), cutoff=1)
    # Instead of writing out the matrix you can also access its rows directly.
    return [row for row in tdm.rows(cutoff=1)]


# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed
def tokenize_and_stem(text):
    return remove_stopwords(stem_words(tokenize_only(text)))

def stem_words(words):
    stems = [stemmer.stem(t) for t in words]
    return stems

def remove_stopwords(words):
    return [word for word in words if word not in stopwords and word.find("'")<0] # normally word contain ' should be stopword, like can't I'v ...

def tokenize_only(text):
    if not is_ascii(text):
        return [] #only english is supported

    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    # tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    #tokens = re.split(r'[,;:.&\[\]\\ /!?()0123456789]', text.lower())
    from enchant.tokenize import get_tokenizer
    tknzr = get_tokenizer("en_US")
    tokens = [w for (w,p) in tknzr(text.lower())]

    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        token.rstrip()
        if re.search('[a-zA-Z]', token) and len(token)>=2:
            filtered_tokens.append(token)

    return correct_words(filtered_tokens)

def correct_words(words):
    #Try correct wrong typed words
    correcter = SpellingReplacer()
    corrected_words = []
    for word in words:
        word = correcter.replace(word)
        # correcter may split one word to 2 words with space delimiter, so..
        corrected_words.extend(word.split())
    return corrected_words

def remove_wrong_words(words):
    outwords = []
    correcter = SpellingReplacer()
    for word in words:
        if correcter.testword(word) or words.count(word)>2:
            outwords.append(word)
        else:
            wrong_words.append(word)

    return outwords

def remove_single_words(words):
    return [word for word in words if words.count(word)>1]

def mergelist(ls1, ls2):
    size = len(ls1)
    if len(ls2) < size:
        size = len(ls2)
    for i in range(size):
        ls1[i].extend(ls2[i])

    return ls1

def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def create_dict(sentences):
    allwords = []
    count = 0
    cent_len = len(sentences)/100
    cent_len = cent_len if cent_len>0 else 1

    # tokenize
    for sent in sentences:
        count += 1
        if count%cent_len==0:
            print count/cent_len
        allwords.extend(tokenize_only(sent))

    allwords = remove_wrong_words(allwords)

    allwords = remove_single_words(allwords)
    #stem and remove stopwords
    allwords = remove_stopwords(stem_words(allwords))

    words = list(set(allwords))
    words_dict = dict(zip(words, [0 for word in words]))

    return words_dict


def load_dict(filename):
    words = read_list_in_file(filename)
    words = [word.rstrip() for word in words]
    print words[:10]
    words_dict = dict(zip(words, [0 for word in words]))
    return words_dict


def create_matrix_with_dict(lines, words_dict):
    wordsinline_list = [ tokenize_and_stem(line) for line in lines]
    matrix = []

    for wordsinline in wordsinline_list:
        matrix_line = words_dict.copy()
        for word in wordsinline:
            if word in matrix_line:
                matrix_line[word] += 1
        matrix.append(matrix_line.values())

    return matrix


class CsvInfo(object):
    content_list = []
    def __init__(self, filename):
        self.__filename = filename
        self.content_list = read_list_in_file(filename)

        self.__feedbacks,self.__labels,self.__emotions=self.getcolumns()

    def match_pattern(self):
        return r'\d+,\d+,(.+),(\d+) - .+,(-?\d+)'
    def getcolumns(self):
        feedbacks = []
        labels = []
        emotions = []
        for line in self.content_list:
            result = re.search(self.match_pattern(), line)
            if result:
                feedback = result.groups()[0]
                feedbacks.append(feedback)
                if len(result.groups())>=3:
                    labels.append(int(result.groups()[1]))
                    emotions.append(int(result.groups()[2]))
            else:
                print 'warning: mismatch----' + line

        return feedbacks, labels, emotions
    def getfeedbacks(self):
        return self.__feedbacks

    def getlabels(self):
        return self.__labels
    def getemotions(self):
        return self.__emotions
    def get_01_labels(self):
        lables_01 = [val if val==0 else 1 for val in self.__labels]
        return lables_01

    def caculate_freq_dtm(self, dtm):
        #caculate frequnce dtm using tfi,j =  rfi,j/sum(rf0..m,j)
        dtm_freq = []
        for row in dtm:
            total = sum(row)
            freqs=[]
            for val in row:
                if total == 0:
                    freq = 0
                else:
                    freq = float(val)/total
                freqs.append(freq)

            dtm_freq.append(freqs)
        return dtm_freq

    def create_DTM_with_dict(self,dictname = 'mydict.txt'):
        tdm = textmining.TermDocumentMatrix()

        feedbacks = self.getfeedbacks()

        feedback_dict = load_dict(dictname)
        dtm = create_matrix_with_dict(feedbacks, feedback_dict)
        dtm_freq = self.caculate_freq_dtm(dtm)
        return dtm, dtm_freq
        
    def create_DTM(self):
        tdm = textmining.TermDocumentMatrix()

        feedbacks = self.getfeedbacks()

        wordsinline_list = [ ' '.join(tokenize_and_stem(line)) for line in feedbacks]

        dtm = termdocumentmatrix(wordsinline_list)
        dtm = dtm[1:] # remove the line of words

        dtm_freq = self.caculate_freq_dtm(dtm)
        return dtm, dtm_freq

class CsvInfo_NoLabel(CsvInfo):
   def match_pattern(self):
       return r'\d+,\d+,(.+)'


def create_and_save_dict():
    lines = read_list_in_file("feedback.txt")
    words_dict = create_dict(lines)
    save_list("mydict.txt", words_dict.keys())
    save_list("wrong_words.txt", wrong_words)
 
def create_dtm_from_csv():
    #nltk.download()
    csvinfo = CsvInfo("filtered_300_classify.csv")
    dtm, dtm_freq = csvinfo.create_DTM_with_dict()
    if len(dtm) != len(csvinfo.getlabels()):
        print "WARNING!!!"
    print dtm
    labels01 = csvinfo.get_01_labels()
    labels01_vec = [[val] for val in labels01]
    dtm_withlabel = mergelist(dtm, labels01_vec)
    save_list("dtm_withlabel.txt", [' '.join([str(val) for val in row]) for row in dtm_withlabel])


def test_csvinfo():
    csvinfo = CsvInfo_NoLabel("filtered_2000_0426.csv")
    feedbacks = csvinfo.getfeedbacks()
    print "From non labeled file, print the first 20 feedbacks"
    print feedbacks[:20]
    csvinfo = CsvInfo("filtered_300_classify.csv")
    feedbacks = csvinfo.getfeedbacks()
    print "From labeled file: print the first 20 feedbacks"
    print feedbacks[:20]


def classify_bayes():
    csvinfo = CsvInfo("filtered_300_classify.csv")
    dtm, dtm_freq = csvinfo.create_DTM_with_dict()
    #dtm, dtm_freq = csvinfo.create_DTM()
    if len(dtm) != len(csvinfo.getlabels()):
        print "WARNING!!!"
    labels01 = csvinfo.get_01_labels()

    X = np.array(dtm[:250])
    Y = np.array(labels01[:250])

    # Create Naive Bayes classifier and train
    clf = GaussianNB()
    clf.fit(X, Y)

    predicts = clf.predict(dtm[250:300])

    from sklearn.metrics import classification_report
    target_name=['non-informative', 'informative']
    print(classification_report(predicts, labels01[250:300], target_names=target_name))

    cls_labels = csvinfo.getlabels()
    Y = np.array(cls_labels[:250])
    clf.fit(X, Y)
    predicts = clf.predict(dtm[250:300])
    target_name = ['non-', 'other', 'giving', 'seeking', 'feature','problem']
    print(classification_report(predicts, cls_labels[250:300], target_names=target_name))

    print zip(predicts, cls_labels[250:300])
#    print "Accuracy Rate, which is calculated by accuracy_score() is: %f" % accuracy_score(labels01[250:300], predicts)
if __name__ == "__main__":
#    reload(sys)  
#    sys.setdefaultencoding('utf8')
    #create_and_save_dict()
    #create_dtm_from_csv()
    classify_bayes()
    #test_csvinfo()