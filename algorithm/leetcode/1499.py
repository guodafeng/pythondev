import heapq

class Solution:
    def findMaxValueOfEquation(self, A, k):
        q = []
        res = -float('inf')
        for x, y in A:
            while q and q[0][1] < x - k:
                heapq.heappop(q)
            if q: res = max(res, -q[0][0] + y + x)
            heapq.heappush(q, (x - y, x))
            print(q)
        return res 


sl = Solution()
k = 1
a = [[1,3],[2,0],[5,10],[6,-10]]
res = sl.findMaxValueOfEquation(a, k )
print(res)


