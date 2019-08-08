class Solution:
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        newIndex = 0
        prenum = nums[0]
        sameCount = 0
        for num in nums:
            if num == prenum:
                sameCount += 1
            else:
                sameCount = 1
                prenum = num

            if sameCount <= 2:
                nums[newIndex] = num
                newIndex += 1
        return newIndex
            

nums = [0,0,1,1,1,1,2,3,3] 

sol = Solution()
print(sol.removeDuplicates(nums))
print(nums)
        
