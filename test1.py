import urllib2
import pickle
import re

def _isupper(str):
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = True
    for i in range (len(str)):
        if upper.find(str[i])<0:
            res = False
            break
    return res


def level0():
    res = 2
    for i in range(37):
        res = res * 2
    print res

def level1(str):
    print "level1"
    res = ""
    exd = " .()'"
    for i in range(len(str)):
        converted = ord(str[i])
        if  (exd.find(str[i]) < 0 ):
            converted += 2
            if (converted > 0x7a):
                converted -= 26
        res = res + chr(converted)   
    
    print res

def level2(str):
# find charaters in string
    print "level2"
    chartable="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    res = ""
    for i in range(len(str)):
        if (chartable.find(str[i]) >= 0):
            res = res + str[i]
    print res
def level3(str):
#One small letter, surrounded by EXACTLY three big bodyguards on each of its sides.
    print "level3"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    res = ""
    for i in range(3, len(str)-3):
        if (_isupper(str[i-3:i]) and _isupper(str[i+1:i+4]) and str[i].islower()):
            if ( ( (i-4)<0 or str[i-4].islower() ) and ( (i+4)>=len(str) or str[i+4].islower() ) ):
                res += str[i]
    print res

def level4(str):
    print "level4"
    proxy_support = urllib2.ProxyHandler({"http":"http://espcolo-webproxy00:8080"})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    
    nextURL = ''
    while (1):
        if (len(nextURL )== 0):
            nextURL = raw_input('Enter the url:')
        if (len(nextURL )== 0):
            break

        content = urllib2.urlopen(nextURL).read()
        patt = '.* the next nothing is (\d+)' 
        m = re.match(patt, content)
        if(m is None):
            nextURL = ''
            print 'Next url cannot parsed, The page content is:' + content
            continue
        nextID = m.group(1)

        patt2 = '(.+nothing=)\d+'
        m = re.match(patt2, nextURL)
        if (m is None):
            nextURL = ''
            continue
        nextURL = m.group(1) + nextID

        print nextURL
def geturlobj(str):
    proxy_support = urllib2.ProxyHandler({"http":"http://espcolo-webproxy00:8080"})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    
    nextURL=str
    if (len(nextURL )== 0):
        nextURL = raw_input('Enter the url:')
    if (len(nextURL )== 0):
        return 

    return urllib2.urlopen(nextURL)
 
def level5():
    urlobj = geturlobj('http://www.pythonchallenge.com/pc/def/banner.p')
    pickobj = pickle.load(urlobj)

    for item in pickobj:
        #print item
        #print "".join(i[0] * i[1] for i in item) #print characters
        mylist = [] 
        for i in item:
            mylist.append( i[0] * i[1] )
        print ''.join(mylist)



def main():
    level0()
    str = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
    level1(str)
    str = "map"
    level1(str)
    level2(str)

    #level3(str) # linkedlist
    #level4(r"http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=12345")

    level5()
if __name__ == '__main__':
    main()
