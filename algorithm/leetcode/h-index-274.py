class Solution:
    def hIndex(self, citations):
        cit_s = sorted(citations, reverse = True)

        size = len(cit_s)
        if size == 0:
            return 0

        l = 0
        r = size - 1
        m = (l+r) // 2

        while r>l:
            if cit_s[m] > (m + 1):
                l = m + 1
                m = (l+r) // 2
            else:
                r = m
                m = (l+r) // 2

        print(l, r)
        if cit_s[l] >= l:
            return min(cit_s[l], l + 1)
        elif l>0:
            return min(cit_s[l-1], l )
        else:
            return 0





def test():
    sol = Solution()

    cit =  [4, 4, 0, 0]

    print(sol.hIndex(cit))


test()
        
