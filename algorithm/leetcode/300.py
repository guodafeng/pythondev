# from typing import List
# class Solution:
    # def lengthOfLIS(self, nums: List[int]) -> int:
        # dp = [1] * len(nums)
        # for i, num in enumerate(nums):
            # for j in range(i):
                # if num > nums[j]:
                    # dp[i] = max(dp[i], dp[j] + 1)

        # return max(dp)
        
# a = [10,9,2,5,3,7,101,18]
# sol = Solution()
# print(sol.lengthOfLIS(a))

class Solution:
    def generateParenthesis(self, n):
        left,right = 0,0
        ret = []
        pair = [''] * (2 * n)

        st = []
        st.append(('(',0,0,0))
        while True:
            if len(st) == 0:
                break
            elm = st.pop()
            pair[elm[1]] = elm[0]
            left,right = elm[2],elm[3]
            if elm[0] == '(':
                left += 1
            else:
                right += 1

            if left == n and right == n: # found one pair
                ret.append(''.join(pair))
                continue

            if left > right:
                if left < n:
                    st.append(('(', elm[1] + 1,left, right))
                    st.append((')', elm[1] + 1,left, right))
                else:
                    st.append((')', elm[1] + 1,left, right))
            else:
                st.append(('(', elm[1] + 1,left, right))

        print(ret)
        return ret
    
    def generate(self, numRows):
        if numRows < 1:
            return []
        ret = [] * numRows
        row = [1]
        ret.append(row)
        for i in range(1, numRows):
            row = [0] * (i+1)
            print(ret)
            for j in range(i+1):
                print(i,j)
                row[j] = (0 if j==0 else ret[i-1][j-1]) + (0 if j==i else ret[i-1][j])

            ret.append(row)
                
        return ret
        
if __name__ == "__main__":
    sol = Solution()
    # sol.generateParenthesis(8)
    sol.generate(5)
