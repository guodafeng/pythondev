import sys
import textmining
import nltk
import re
import os
import collections
import fileinput
import enchant
from nltk.metrics import edit_distance
from autocorrect import spell
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import pickle

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(["n't", "aren't", "doesn't","don't", "i'm", "i'v","i'll", "can't", "couldn't"])
CUR_DIR = os.getcwd()
DTM_DICT_F = "dtmdict.pic"

# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")   


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SpellingReplacer(object):
    __metaclass__ = Singleton
    def __init__(self, dict_name = 'en_US', mywords = 'mywords.txt', max_dist = 1):
        self.spell_dict = enchant.DictWithPWL(dict_name, fulldatapath(mywords))
        self.max_dist = max_dist

    def correct(self, word):
        # used distance for correcting word
        dist = len(word)/3 + 1
        if  SpellingCheck().check_word(word):
            return word

        suggestions = self.spell_dict.suggest(word)
        if word == 'amprove':
            print "correct word amprove to:"
            print suggestions[0]
        if suggestions and edit_distance(word, suggestions[0]) <= dist:
            return suggestions[0]
        else:
            return word

    def testword(self, word):
        return self.spell_dict.check(word)

class SpellingCheck(object):
    __metaclass__ = Singleton

    def __init__(self, filename = 'my_en_us.pic'):
        self._mydict = set()

        self.load_dict(filename)

    def add_dict_file(self, filename):
        lines = read_list_in_file(filename)
        for line in lines:
            self._mydict.add(line.rstrip().split('/')[0].lower())
    def save_dict(self, filename):
        filename = fulldatapath(filename)
        with open(filename, 'wb') as fh:
            pickle.dump(self._mydict, fh, protocol=pickle.HIGHEST_PROTOCOL)
    def load_dict(self, filename):
        filename = fulldatapath(filename)
        if os.path.exists(filename):
            with open(filename, 'rb') as fh:
                self._mydict = pickle.load(fh)

    def check_word(self, word):
        return word.lower() in self._mydict

class SpellCorrecter(object):
    __metaclass__ = Singleton
    def __init__(self):
        self.model = collections.defaultdict(lambda: 1)
        self.NWORDS = self.train(self.words(file(fulldatapath('big.txt')).read()))
        self.NWORDS = self.train(self.words(file(fulldatapath('original_feedback_with_ids_en.csv')).read()))
        self.words_map = self.load_word_map('mywordsmap.txt')
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz\''

    def load_word_map(self, filename):
        lines = read_list_in_file(filename)
        words_map = {}
        for line in lines:
            line = line.rstrip()
            words = line.split(':')
            words_map[words[0]] = words[1]
        return words_map

    def words(self,text): return re.findall('[a-z\']+', text.lower())

    def train(self, features):
        for f in features:
            if SpellingCheck().check_word(f):
                self.model[f] += 1
        return self.model

    def edits1(self, word):
       splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
       deletes    = [a + b[1:] for a, b in splits if b]
       transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
       replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
       inserts    = [a + c + b     for a, b in splits for c in self.alphabet]
       return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.NWORDS)

    def known(self, words): return set(w for w in words if w in self.NWORDS)

    def correct(self, word):
        if  SpellingCheck().check_word(word):
            return word
        if word in self.words_map:
            return self.words_map[word]

        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        candidate = max(candidates, key=self.NWORDS.get)

        dist = len(word)/5 + 1
        if  edit_distance(word, candidate) <= dist:
            return candidate
        else:
            return word


class DataSelector(object):
    def __init__(self, filename):
        self._filename = filename
        self._content_list = read_list_in_file(filename)
        self.create_id_lines()

    def create_id_lines(self):
        #get id list with format (id, subid, fullline)
        pattern = r'(\d+),(\d+),(.+)'
        self._id_lines = []
        for line in self._content_list:
            line = line.rstrip()
            res = re.search(pattern, line)
            if res:
                self._id_lines.append((res.groups()[0],res.groups()[1], line))

    def get_id_lines(self):
        return self._id_lines
    def get_ids(self):
        return [(row[0], row[1]) for row in self._id_lines]

    def split_line(self):
        self._content_list = split_sentence(self._content_list)
        self.create_id_lines()

    # filter out wrong lines and lines of which id are in exclude_ids
    def filter_out(self, exclude_ids):
        return [row[2] for row in self._id_lines if (row[0],row[1]) not in exclude_ids and not is_wrong_sentence(row[2])]

    def random_select(self, data_count, exclude_ids):
        import random
        random.shuffle(self._id_lines)
        filtered_rows = self.filter_out(exclude_ids)
        return filtered_rows[:data_count]

class DTM_dict(object):
    @classmethod
    def word_count_map(cls,filename):
        # create a dict of word->(repeated number in all the sentences). word may be wrong spelled
        sentences = read_list_in_file(filename)
        count_map = collections.defaultdict(lambda : 0)

        for idx, sent in enumerate(sentences):
            print "\r",
            print "tokenizing: %d" % idx
            for word in tokenize_only(sent):
                count_map[word] += 1
        return count_map

    @classmethod
    def dtm_set(cls, filename):
        # create a set of words, words are corrected, filtered and stemmed
        word_count_map = DTM_dict.word_count_map(filename)
        allwords = word_count_map.keys()
        print "try to correct wrong words"
        allwords = correct_words(allwords)
        print "remove wrong words which cannot be corrected"
        allwords = remove_wrong_words(allwords)

        #stem and remove stopwords
        print "remove stopwords"
        allwords = remove_stopwords(stem_words(allwords))

        wordset = set(allwords)
        return wordset

    @classmethod
    def save_set(cls, wordset, filename):
        with open(fulldatapath(filename), 'wb') as fh:
            pickle.dump(wordset, fh)
    @classmethod
    def load_set(cls, filename):
        with open(fulldatapath(filename), 'rb') as fh:
            return pickle.load(fh)

class CsvInfo(object):
    def __init__(self, filename, create_dtm = True):
        self.__filename = filename
        self.content_list = read_list_in_file(filename)

        self._columns = (self._ids,self._subids,self.__feedbacks,self.__labels,self.__emotions) =self.getcolumns()
        self.__dtm = None
        self.__dtm_freq = None


    def match_pattern(self):
        return r'(\d+),(\d+),(.+),(\d+) - .+,(-?\d+)?'
    def getcolumns(self):
        ids = []
        subids = []
        feedbacks = []
        labels = []
        emotions = []
        for line in self.content_list:
            result = re.search(self.match_pattern(), line)
            if result:
                ids.append(result.groups()[0])
                subids.append(result.groups()[1])
                feedback = result.groups()[2]
                feedbacks.append(feedback)
                if len(result.groups())>=5:
                    labels.append(result.groups()[3])
                    emotion = result.groups()[4]
                    emotion = emotion if emotion else ''
                    emotions.append(emotion)
            else:
                print 'warning: mismatch----' + line

        return ids, subids, feedbacks, labels, emotions
    def getfeedbacks(self):
        return self.__feedbacks

    def getlabels(self):
        return [int(label) for label in self.__labels]
    def getemotions(self):
        return [int(emotion) for emotion in self.__emotions]
    def get_01_labels(self):
        lables_01 = [int(val) if val=='0' else 1 for val in self.__labels]
        return lables_01
    def get_dtm(self):
        if self.__dtm is None:
            self.__dtm = self.__create_DTM_with_dict()
        return self.__dtm
    def get_dtm_freq(self):
        if self.__dtm_freq is None:
            dtm = self.get_dtm()
            self.__dtm_freq = self.__caculate_freq_dtm(dtm)
        return self.__dtm_freq

    def __caculate_freq_dtm(self, dtm):
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

    def __create_DTM_with_dict(self):
        feedbacks = self.getfeedbacks()

        wordset = DTM_dict.load_set(DTM_DICT_F)
        dtm = create_matrix_with_dict(feedbacks, wordset)
        return dtm

    def __create_DTM(self):
        tdm = textmining.TermDocumentMatrix()

        feedbacks = self.getfeedbacks()

        wordsinline_list = [ ' '.join(tokenize_and_stem(line)) for line in feedbacks]

        dtm = termdocumentmatrix(wordsinline_list)
        dtm = dtm[1:] # remove the line of words

        dtm_freq = self.__caculate_freq_dtm(dtm)
        return dtm, dtm_freq

    def correct_feedback(self):
        new_contents, words_changed = correct_sentences(self.__feedbacks)
        self._columns += (new_contents, words_changed)

    def save_columns(self, filename):
        clmns = [clm for clm in self._columns if len(clm)>0]
        new_contents = zip(*clmns)
        new_contents.insert(0, self.column_names())
        format_contents = ['^'.join(line) for line in new_contents]
        save_list(filename, format_contents)

    def column_names(selfs):
        return ('ID','SubID','Feedback','Tag','Emotion','Corrected Feedback', 'Words corrected')

class CsvInfo_NoLabel(CsvInfo):
   def match_pattern(self):
       return r'(\d+),(\d+),(.+)'
   def column_names(selfs):
       return ('ID','SubID','Feedback','Corrected Feedback', 'Words corrected')

# Another approch to correct feedback in place
class FeedbackCorrect(object):
    def __call__(self,*args, **kwargs):
        pattern = kwargs['pattern']
        rex = re.compile(pattern)
        filenames = [fulldatapath(filename) for filename in args]

        for line in fileinput.input(filenames,inplace=True,backup=".bak"):
            match = rex.match(line)
            if match:
                sent,words = correct_sent(match.groups()[0])
                print "%s,%s,%s" % (line.rstrip(),sent,words)
            else:
                print line.rstrip()

# utility functions below ####################################

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
    return remove_stopwords(stem_words(correct_words(tokenize_only(text))))

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
    return [SpellCorrecter().correct(word) for word in words]

def correct_sent(sent):
    words = tokenize_only(sent)
    changed = []
    for word in words:
        corrected = SpellCorrecter().correct(word)
        if corrected != word:
            changed.append("'%s -> %s'" %(word, corrected))
            sent = re.sub(word, corrected, sent,flags=re.IGNORECASE)
    return sent, ' '.join(changed)

def correct_sentences(sentences):
    new_sentences = []
    words_changed = []
    for line in sentences:
        line, changed = correct_sent(line)
        words_changed.append(changed)
        new_sentences.append(line)

    return new_sentences, words_changed

def remove_wrong_words(words):
    outwords = []
    tester = SpellingCheck()
    for word in words:
        if tester.check_word(word): # or words.count(word)>2:
            outwords.append(word)

    return outwords

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def is_wrong_sentence(line):
    words = tokenize_only(line)
    wrong_num = 0
    for word in words:
        if not SpellingCheck().check_word(word):
            wrong_num += 1

    #if (len(words)*4 > len(line)) and wrong_num*3<=len(words):
    if wrong_num*2>=len(words):
        print "possible wrong line:" + line
    return wrong_num * 3 > len(words)


def create_matrix_with_dict(lines, wordset):
    wordsinline_list = [ tokenize_and_stem(line) for line in lines]
    matrix = []

    for wordsinline in wordsinline_list:
        matrix_line = dict.fromkeys(wordset, 0)
        for word in wordsinline:
            if word in matrix_line:
                matrix_line[word] += 1
        matrix.append(matrix_line.values())

    return matrix

def is_tooshort(sentence):
    return len(sentence) <= 6 or len(sentence.split(' '))<=2

def split_sentence(lines):
    split_list = []
    for line in lines:
        pattern = r'(\d+),(\d+),(.+)'
        res = re.search(pattern, line)
        if res:
            line_id = res.groups()[0]
            subid =int(res.groups()[1])
            feedback = res.groups()[2]
            sentences = feedback.split('.')
            for sentence in sentences:
                if is_tooshort(sentence):
                    continue
                splitline = "%s,%d,%s" % (line_id, subid, sentence)
                split_list.append(splitline)
                subid+=1
    return split_list

#  create words set from the input filename, and save the set to DTM_DICT_F
def create_dtm_dict(filename):
    wordset = DTM_dict.dtm_set(filename)
    DTM_dict.save_set(wordset,DTM_DICT_F)

def create_my_own_dic():
    #en_US.dic and words.txt are from internet, mywords.txt is used to define our own dictory
    en_dict = SpellingCheck()
    en_dict.add_dict_file("en_US.dic")
    en_dict.add_dict_file("words.txt")
    en_dict.add_dict_file("mywords.txt")
    print "this is in: " + str(en_dict.check_word("this"))
    print en_dict.check_word("thinned")
    print en_dict.check_word("thinner")
    en_dict.save_dict("my_en_us.pic")
    mydict2 = SpellingCheck()
    print "java is in: " + str(mydict2.check_word("java"))

# test code below ###################################

def count_wrong_words()
    word_count_map = DTM_dict.word_count_map("feedback.txt")
    wrong_but_repeated = []
    tester = SpellingCheck()
    for word in word_count_map:
        if (not tester.check_word(word)) and word_count_map[word]>=3:
            wrong_but_repeated.append((word ,word_count_map[word]))
    from operator import itemgetter
    wrong_but_repeated = sorted(wrong_but_repeated, key = itemgetter(1), reverse=True)
    save_list("wrong_but_repeated_3.txt", [item[0] + ":" + str(item[1]) for item in wrong_but_repeated])

def test_csvinfo():
    csvinfo = CsvInfo_NoLabel("filtered_2000_0426.csv")
    feedbacks = csvinfo.getfeedbacks()
    print "From non labeled file, print the first 20 feedbacks"
    print feedbacks[:20]
    csvinfo.get_dtm()
    csvinfo = CsvInfo("filtered_300_classify.csv")
    feedbacks = csvinfo.getfeedbacks()
    print "From labeled file: print the first 20 feedbacks"
    csvinfo.get_dtm()
    print feedbacks[:20]


# return trained bayers classifier
def train_clf():
    csvinfo = CsvInfo("nps_900.csv")
    dtm = csvinfo.get_dtm()
    if len(dtm) != len(csvinfo.getlabels()):
        print "WARNING!!!"

    labels01 = csvinfo.get_01_labels()
    labels = csvinfo.getlabels()

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

def split_filter_feedback():
    filter = DataSelector("nps_900.csv")
    exclude_ids = filter.get_ids()

    selector = DataSelector("original_feedback_with_ids_en.csv")
    selector.split_line()

    save_list("test_en.txt", selector.filter_out( exclude_ids))

def random_select_feedback():
    filter = DataSelector("filtered_300_classify.csv")

    exclude_ids = filter.get_ids()

    selector = DataSelector("informativefeedback.txt")
    save_list("rand2000.txt", selector.random_select(2000, exclude_ids))


def correct_wrong_words():
    csvinfo = CsvInfo("nps_900.csv",False)
    csvinfo.correct_feedback()
    csvinfo.save_columns("nps_900_correct.txt")

    csvinfo2= CsvInfo_NoLabel("test_en.txt",False)
    csvinfo2.correct_feedback()
    csvinfo2.save_columns("test_en_correct.txt")


if __name__ == "__main__":
#    reload(sys)  
    #create_dtm_from_csv()
    #test_csvinfo()
    #test_clf()
    #train_clf()
    create_dtm_dict("original_feedback_with_ids_en.csv")
    #filter_informative()
    # random_select_feedback()
    #create_userdefined_words()
    #create_my_own_dic()
    #correct_wrong_words()
    #split_filter_feedback()
    #FeedbackCorrect()("t900.csv",pattern = r'\d+,\d+,(.+),\d+ - .+,-?\d+?')

"""
First step:
 call create_my_own_dic to create our own defined English dict to check word spelling

Usage:
 comment/uncomment function for your purpose
 1. call create_dtm_dict to create a words set file used by  dtm(document-term matrix) creation
 2. DataSelector is for select specific data from feedback file,refer to split_filter_feedback() and random_select_feedback()
 3. CsvInfo : handle the csv file which has been labeled,
    CsvInfo_NoLable: handle the csv file which hasnot be labeled,
    a. create dtm from feedback, used for classify purpose, refer to filter_informative()
    b. correct wrong word in feedback , refer to correct_wrong_words()

"""

