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


class SpellingCheck(object):
    _mydict = set()
    def add_dict_file(self, filename):
        lines = read_list_in_file(filename)
        for line in lines:
            self._mydict.add(line.rstrip().split('/')[0].lower())
    def save_dict(self, filename):
        import pickle
        with open(filename, 'wb') as fh:
            pickle.dump(self._mydict, fh, protocol=pickle.HIGHEST_PROTOCOL)
    def load_dict(self, filename):
        import pickle
        with open(filename, 'rb') as fh:
            self._mydict = pickle.load(fh)
    def check_word(self, word):
        return word.lower() in self._mydict

class DataSelector(object):
    def __init__(self, filename):
        self._filename = filename
        self._content_list = read_list_in_file(filename)
        self._id_lines = []
        #get id list with format (id, subid, fullline)
        pattern = r'(\d+),(\d+),(.+)'
        for line in self._content_list:
            res = re.search(pattern, line)
            if res:
                self._id_lines.append((res.groups()[0],res.groups()[1], line))

    def get_id_lines(self):
        return self._id_lines

    def random_select(self, data_count, not_in_ids):
        import random
        random.shuffle(self._id_lines)
        count = 0
        selected = []
        for row in self._id_lines:
            if row[0] not in not_in_ids:
                count += 1
                selected.append(row[2].rstrip())
            if count > data_count:
                break
        save_list("selected_informative_feedback.txt", selected)


class CsvInfo(object):
    content_list = []
    def __init__(self, filename):
        self.__filename = filename
        self.content_list = read_list_in_file(filename)

        self.__feedbacks,self.__labels,self.__emotions=self.getcolumns()
        self.__dtm, self.__dtm_freq = self.create_DTM_with_dict()

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
    def get_dtm(self):
        return self.__dtm
    def get_dtm_freq(self):
        return self.__dtm_freq

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

    def filter_by_clf(self, preds):
        filtered = []
        for i in range(len(preds)):
            if preds[i] > 0:
                filtered.append(self.content_list[i].rstrip())
        save_list("informativefeedback.txt", filtered)

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

def d_print(info):
    if D_LEVEL==0:
        return
    print info

def fulldatapath(filename):
    return ".%s%s%s%s" % (os.sep, "data", os.sep, filename)

def save_list(filename, lines, param = 'w'):
    fh = open(fulldatapath(filename), param)
    fh.writelines('\n'.join(lines))
    fh.close()
def read_list_in_file(filename):
    fh = open(fulldatapath(filename), 'r')
    lines = fh.readlines()
    fh.close()
    return lines
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
        if re.search('[a-zA-Z]', token): # and len(token)>=2:
            filtered_tokens.append(token)

    return filtered_tokens

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
    tester = SpellingCheck()
    tester.load_dict("my_en_us.pic")
    for word in words:
        if tester.check_word(word): # or words.count(word)>2:
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

MYDICT = SpellingCheck()
MYDICT.load_dict("my_en_us.pic")

def is_wrong_sentence(line):
    words = tokenize_only(line)
    wrong_num = 0
    for word in words:
        if not MYDICT.check_word(word):
            wrong_num += 1
    return wrong_num * 3 > len(words)

def create_word_count_map(words):
    # create a dict of word->numbers the word occurred in the list
    word_count_map = {}
    for word in words:
        word_count_map[word] = word_count_map.get(word, 0) + 1

    return word_count_map

def create_dict(sentences):
    # create a dict of word->(repeated number in all the sentences), word are original word
    allwords = []
    count = 0
    cent_len = len(sentences)/100
    cent_len = cent_len if cent_len>0 else 1

    # tokenize
    print "tokenize"
    for sent in sentences:
        count += 1
        if count%cent_len==0:
            print "\r",
            print count/cent_len,
        allwords.extend(tokenize_only(sent))

    word_count_map = create_word_count_map(allwords)
    return word_count_map

def filter_dict(word_count_map):
    # create a dict of word->0, word are filtered and stemmed
    allwords = word_count_map.keys()
    print "remove wrong words"
    allwords = remove_wrong_words(allwords)

    #    allwords = remove_single_words(allwords)
    #stem and remove stopwords
    print "remove stopwords"
    allwords = remove_stopwords(stem_words(allwords))

    words = list(set(allwords))
    words_dict = dict(zip(words, [0 for word in words]))
    return words_dict


def load_dict(filename):
    words = read_list_in_file(filename)
    words = [word.rstrip() for word in words]
    #print words[:10]
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

def load_dtm(filename):
    lines = read_list_in_file(filename)
    matrix = []
    for line in lines[1:]:
        nums = line.split(',')
        matrix.append([int(num) for num in nums])
    return matrix

# test code below
def create_userdefined_words():
    lines = read_list_in_file("feedback.txt")
    print "creating wrong words from feedback.txt"
    word_count_map = create_dict(lines)

    wrong_but_repeated = []
    tester = SpellingCheck()
    tester.load_dict("my_en_us.pic")
    print tester.check_word("this")
    for word in word_count_map:
        if (not tester.check_word(word)) and word_count_map[word]>=3:
            wrong_but_repeated.append((word ,word_count_map[word]))
    from operator import itemgetter
    wrong_but_repeated = sorted(wrong_but_repeated, key = itemgetter(1), reverse=True)

    save_list("wrong_but_repeated_3.txt", [item[0] + ":" + str(item[1]) for item in wrong_but_repeated])

def create_and_save_dict():
    lines = read_list_in_file("feedback.txt")
    print "creating dict from feedback.txt"
    word_count_map = create_dict(lines)
    words_dict = filter_dict(word_count_map)

    save_list("mydict.txt", words_dict.keys())
    save_list("wrong_words.txt", wrong_words)
 
def create_dtm_from_csv():
    #nltk.download()
    csvinfo = CsvInfo("filtered_300_classify.csv")
    dtm = csvinfo.get_dtm()

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


# return trained bayers classifier
def train_clf():
    csvinfo = CsvInfo("filtered_300_classify.csv")
    dtm = csvinfo.get_dtm()
    if len(dtm) != len(csvinfo.getlabels()):
        print "WARNING!!!"

    labels01 = csvinfo.get_01_labels()
    labels = csvinfo.getlabels()

    # dtm = dtm[:250]
    # labels01 = labels01[:250]
    # labels = labels[:250]
    X = np.array(dtm)
    Y = np.array(labels01)

    # Create Naive Bayes classifier and train
    clf01 = GaussianNB()
    clf01.fit(X, Y)

    Y = np.array(labels)
    clf = GaussianNB()
    clf.fit(X, Y)

    return csvinfo, clf01, clf

def test_clf():
    csvinfo, clf01, clf  = train_clf()
    dtm = csvinfo.get_dtm()
    feedbacks = csvinfo.getfeedbacks()
    labels01 = csvinfo.get_01_labels()
    labels = csvinfo.getlabels()

    # test classifier
    target_names01=['non-informative', 'informative']
    target_names = ['non-', 'other', 'giving', 'seeking', 'feature','problem']

    do_test_clf(clf01, feedbacks[250:300], dtm[250:300], labels01[250:300], target_names01)
    do_test_clf(clf, feedbacks[250:300], dtm[250:300], labels[250:300], target_names)

def do_test_clf(clf, feedbacks, dtm, labels, target_names):
    predicts = clf.predict(dtm)

    if (len(labels)):
        from sklearn.metrics import classification_report
        print(classification_report(predicts, labels, target_names=target_names))
        print zip(predicts, labels)

    results = zip(feedbacks, predicts)
    for res in results:
        print res[0] + ":" + str(res[1]) + "-" + target_names[res[1]]
#
def filter_informative():
    csvinfo, clf01, clf = train_clf()

    csvinfo_test = CsvInfo_NoLabel("allfiltered_en.txt")
    dtm = csvinfo_test.get_dtm()

    preds = []
    step_size = len(dtm)/1000 + 1
    for i in range(1000):
        if (i*step_size > len(dtm)):
            break
        pred_part = clf01.predict(dtm[i*step_size:(i+1)*step_size])
        preds.extend(pred_part)
        print "\r",
        print i,

    csvinfo_test.filter_by_clf(preds)


def random_select_feedback():
    filter = DataSelector("filtered_300_classify.csv")

    filter_ids = filter.get_id_lines()
    filter_ids = [row[0] for row in filter_ids] # these ids are already classified, will be skipped in the random_select

    selector = DataSelector("informativefeedback.txt")
    selector.random_select(2000, filter_ids)

def test_my_own_dic():
    mydict = SpellingCheck()
    mydict.add_dict_file("en_US.dic")
    mydict.add_dict_file("words.txt")
    mydict.add_dict_file("mydict.txt")
    print "this is in: " + str(mydict.check_word("this"))
    print mydict.check_word("thinned")
    print mydict.check_word("thinner")
    mydict.save_dict("my_en_us.pic")
    mydict2 = SpellingCheck()
    mydict2.load_dict("my_en_us.pic")
    print "java is in: " + str(mydict2.check_word("java"))

def filter_wrong_sentences():
    lines = read_list_in_file("2000selected_informative_feedback.txt")
    out = [line.rstrip() for line in lines if not is_wrong_sentence(line)]
    save_list("filter_wrong_sentence.txt", out)


if __name__ == "__main__":
#    reload(sys)  
#    sys.setdefaultencoding('utf8')
    #create_dtm_from_csv()
    #test_csvinfo()
    #test_clf()
    #train_clf()
    #create_and_save_dict()
    #filter_informative()
    # random_select_feedback()
    #create_userdefined_words()
    #test_my_own_dic()
    filter_wrong_sentences()
