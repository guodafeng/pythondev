from typing import List

class Solution:
    def cost_gap(self, nums, cost, dest):
        return sum(cost[i] * abs(dest-num) for (i, num) in enumerate(nums))
        # for i, num in enumerate(nums):

    def minCost(self, nums: List[int], cost: List[int]) -> int:
        lo = min(nums)
        hi = max(nums)

        while lo < hi:
            m = (lo + hi) // 2
            gap_pre = self.cost_gap(nums, cost, m - 1)
            gap_cur = self.cost_gap(nums, cost, m )
            gap_next =  self.cost_gap(nums, cost, m + 1)

            if gap_pre >= gap_cur and gap_next >= gap_cur:
                return gap_cur

            if gap_pre >= gap_cur and gap_next < gap_cur:
                if lo == m:
                    return gap_next
                else:
                    lo = m

            if gap_pre < gap_cur and gap_next >= gap_cur:
                hi = m

        return self.cost_gap(nums, cost, lo)

        

if __name__ == "__main__":
    sol = Solution()

    nums = [1,3,5,2]
    cost = [2,3,1,14]       
    print(sol.minCost(nums, cost))
    nums = [2,2,2,2,2]
    cost = [4,2,8,1,3]
    print(sol.minCost(nums, cost))
