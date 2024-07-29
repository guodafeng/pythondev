def maxsublen(astr):
    recent_pos = {}
    # lens[i] meaths the maxsublen of astr which end at index i
    maxlen = 0
    maxlen_i = 0
    curlen = 0
    for i, s in enumerate(astr):
        curlen = min(curlen + 1, i - recent_pos.get(s,-1) )
        if curlen >= maxlen:
            maxlen = curlen
            maxlen_i = i
            
        recent_pos[s] = i

    return astr[maxlen_i - maxlen + 1: maxlen_i + 1]


if __name__ == "__main__":
    print(maxsublen("abcabcbb"))
    print(maxsublen("bbbbb"))
    print(maxsublen("pwwkew"))



