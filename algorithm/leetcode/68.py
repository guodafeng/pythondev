class Solution:
    def fullJustify(self, words, maxWidth):
        """
        :type words: List[str]
        :type maxWidth: int
        :rtype: List[str]
        """
        def padWords(wds, isLast):
            if not wds:
                return
            
            wdCount = len(wds)
            strLen = len(''.join(wds))
            padsLen = maxWidth - strLen
            padCount = wdCount - 1
            pads = []
            if padCount > 0:
                padLen = padsLen // padCount
                padMore = padsLen % padCount
                padLen1 = padLen + 1
                padLen2 = padLen
                padLen3 = 0

                if isLast:
                    padMore = padCount
                    padLen1 = 1
                    padLen2 = 0 
                    padLen3 = padsLen - padCount

                pads1 = []
                if padMore > 0:
                    pads1 = [' ' * padLen1 for i in range(padMore)]
                pads2 = [' ' * padLen2 for i in range(padMore, padCount)]
                pads3 = [' ' * padLen3]
                pads = pads1 + pads2 + pads3
            else:
                pads = [' ' * padsLen]
                
            padded = ''.join([''.join(p) for p in zip(wds,pads)])

            return padded
            

        curLen = 0
        curWords = []
        ret = []
        for word in words:
            if curLen > 0:
                curLen += 1
            curLen += len(word)
            if curLen <= maxWidth:
                curWords.append(word)
            else:
                ret.append(padWords(curWords, False))
                curWords = [word]
                curLen = len(word)

        if curWords:
            ret.append(padWords(curWords, True))

        return ret


words = ["This", "is", "an", "example", "of", "text", "justification."]
maxWidth = 16
sol = Solution()
print(sol.fullJustify(words, maxWidth))
words = ["What","must","be","acknowledgment","shall","be"]
maxWidth = 16
print(sol.fullJustify(words, maxWidth))

