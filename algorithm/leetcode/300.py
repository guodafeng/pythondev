from typing import List
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1] * len(nums)
        for i, num in enumerate(nums):
            for j in range(i):
                if num > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)
        
a = [10,9,2,5,3,7,101,18]
sol = Solution()
print(sol.lengthOfLIS(a))
