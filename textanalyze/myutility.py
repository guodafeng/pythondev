import os
import enchant
import pickle
from nltk.metrics import edit_distance

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


def fulldatapath(filename):
    return ".%s%s%s%s" % (os.sep, "data", os.sep, filename)

def save_list(filename, lines, param = 'w'):
    fh = open(fulldatapath(filename), param)
    fh.writelines('\n'.join(lines))
    fh.close()
def read_file(filename):
    fh = open(fulldatapath(filename), 'r')
    content = fh.read()
    fh.close()
    return content

def read_list_in_file(filename):
    fh = open(fulldatapath(filename), 'r')
    lines = fh.readlines()
    fh.close()
    return lines

def correct_words(words):
    #Try correct wrong typed words
    return [SpellCorrecter().correct(word) for word in words]
