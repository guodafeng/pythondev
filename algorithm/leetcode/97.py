class Solution:
    def isInterleave_recur(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool
        """
        len1 = len(s1)
        len2 = len(s2)
        len3 = len(s3)
        if len1==0 and len2==0 and len3==0:
            return True


        if len1>0 and len2>0 and s1[0] == s2[0]:
            if len3>0 and s1[0] == s3[0]:
                return self.isInterleave(s1[1:],s2,s3[1:]) or \
            self.isInterleave(s1,s2[1:],s3[1:])
            else:
                return False
        else:
            if len1 >0 and len3>0 and s1[0] == s3[0]:
                return self.isInterleave(s1[1:],s2,s3[1:])
            elif len2>0 and len3>0 and s2[0] == s3[0]:
                return self.isInterleave(s1,s2[1:],s3[1:])
            else:
                return False


    def isInterleave(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool
        """
        len1 = len(s1)
        len2 = len(s2)
        len3 = len(s3)

        dp = [[False for j in range(len2+1)] for i in range(len1+1)]
        if s3[0] == s1[0]:
            dp[1][0] = True
        if s3[0] == s2[0]:
            dp[0][1] = True

        for i3 in range(1, len3):
            for i1 in range(0,i3+1):
                if i1 <=len1 and i3-i1<= len2 and dp[i1][i3-i1]:
                    print(i1, i3-i1)
                    if i1 < len1 and s1[i1] == s3[i3]:
                        dp[i1+1][i3-i1] = True
                    if i3-i1 < len2 and s2[i3-i1] == s3[i3]:
                        dp[i1][i3-i1+1] = True

        
        return dp[len1][len2]


            






























sol = Solution()

s1 = "bbbbbabbbbabaababaaaabbababbaaabbabbaaabaaaaababbbababbbbbabbbbababbabaabababbbaabababababbbaaababaa"
s2 = "babaaaabbababbbabbbbaabaabbaabbbbaabaaabaababaaaabaaabbaaabaaaabaabaabbbbbbbbbbbabaaabbababbabbabaab"
s3 = "babbbabbbaaabbababbbbababaabbabaabaaabbbbabbbaaabbbaaaaabbbbaabbaaabababbaaaaaabababbababaababbababbbababbbbaaaabaabbabbaaaaabbabbaaaabbbaabaaabaababaababbaaabbbbbabbbbaabbabaabbbbabaaabbababbabbabbab"


# s1 = "aabccc"
# s2 = "dbbca"
# s3 ="aadbbcbcacc"
print(sol.isInterleave(s1,s2,s3))

