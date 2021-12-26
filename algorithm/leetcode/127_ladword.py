class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        return 0
        
    def transferable(self, beginWord, endWord):
        # beginWord -> endWord with one letter change
        if len(beginWord) != len(endWord):
            return False
        for i in range (len(beginWord)):
            if beginWord[:i] != endWord[:i] or beginWord[i+1:] !=
            endWord[i+1:]:
                return False
                
        return True


