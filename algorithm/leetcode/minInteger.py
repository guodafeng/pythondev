class Solution:
    def minInteger(self, num: str, m: int) -> str:
        ni = []
        ret = [] 
        moved = set() 
        nums = list(num)
        for i, e in enumerate(num):
            ni.append((e, i))
        
        ni.sort(key = lambda a : a[0])

        print(ni)
        distance = (len(num), 0)
        for a in ni:
            if m <= 0:
                break
            # count the index which has be move to the head and is
            # before this element
            t = sum((1 for e in moved if e <= a[1]))
            print(a,t, m)
            if a[1]-t <= m:
                ret.append(a[0])
                m -= (a[1] - t)
                moved.add(a[1])
                distance = (len(num), 0)
            else: # can not move to head, so we find the small elment
                # can be moved to head closest
                if a[1] -t - m < distance[0]:
                    distance = (a[1] - t -m, a[1]) 
        if distance[1] > 0:
            i = distance[1]
            j = i - distance[0]
            nums[i],nums[j] = nums[j], nums[i]

        for i, e in enumerate(nums):
            if i not in moved:
                ret.append(e)
        return ''.join(ret)



if __name__ == "__main__":

    sol = Solution()
    # num = '4321'
    # k = 4
    # num = "9438957234785635408"
    # k = 23
    # num = "294984148179"
    # k = 11
    num = '196954'
    k = 2
    print(num)
    print(sol.minInteger(num, k))
