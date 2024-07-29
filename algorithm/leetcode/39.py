from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        if target == 0:
            return [[]]
        if not candidates:
            return []
        ret = []
        for i, candi in enumerate(candidates):
            count = 1
            while candi * count <= target:
                ret += self.merge([candi] * count,
                        self.combinationSum(candidates[i+1:], target - candi*count))
                count += 1
        return ret


    def merge(self, res1, res2):
        res = []
        if res2:
            res = [res1 + r for r in res2]
        return res

        

if __name__ == "__main__":
    sol = Solution()
    candidates = [2,3,6,7]
    target = 7
    # Output: [[2,2,3],[7]]
    print(sol.combinationSum(candidates, target))
    candidates = [2,3,5]
    target = 8
# Output: [[2,2,2,2],[2,3,3],[3,5]]
    print(sol.combinationSum(candidates, target))
