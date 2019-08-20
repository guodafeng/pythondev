from typing import List

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        def helper(nums, num, start):
            return len(list(filter(lambda a: a < num, nums[start:])))

        out = []
        for i, num in enumerate(nums):
            out.append(helper(nums, num, i))
        return out


    def merges(self, nums, start, end, indexs):
        if start >= end:
            return

        m = start + (end - start) // 2
        self.merges(nums, start, m, indexs)
        self.merges(nums, m + 1, end, indexs)

        i = start
        j = m + 1

        out = [0] * (end - start + 1)
        out_i = 0

        newindexs = [0] * (end - start + 1)

        while i <= m or j <= end:
            if i>m or (j <= end and nums[i] > nums[j]):
                out[out_i] = nums[j]
                newindexs[out_i] = indexs[j]
                j += 1
            else:
                out[out_i] = nums[i]
                newindexs[out_i] = indexs[i]
                i += 1
            out_i +=1 
        for i in range(start, start + out_i):
            nums[i] = out[i-start]
            indexs[i] = newindexs[i-start]

sol = Solution()
nums = [3, 5, 3, 9, 22, 78, 8, 11, 31, 21, 10]
indexs = [i for i in range(len(nums))]
# nums = [3, 5, 3, 9]
sol.merges(nums, 0, len(nums)-1, indexs)
print(nums)
print(indexs)


