#!/usr/bin/env python
from typing import List
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        length = len(nums)
        start = 0
        end = length - 1
        color = 0
        print(start, end)
        
        while color < 2 and end >= start:
            if nums[start] > color:
                (nums[start], nums[end]) = (nums[end], nums[start])
                end = end - 1
            else:
                start += 1

            if start == end:
                color += 1
                end = length - 1

            print([start, end], nums)


if __name__=='__main__':
    sol = Solution()
    sol.sortColors([1, 0, 2])


