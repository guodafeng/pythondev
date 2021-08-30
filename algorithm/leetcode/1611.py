class Solution:
    def minimumOneBitOperations(self, n):
        p = n
        def changeTo10(v, i):
            print('10', v,i)
            # i is the highest valid bit index
            if i < 0:
                return 0
            if v & (1 << i) > 0: # hightest valid bit is 1
                return changeTo00(v ^ (1 << i), i - 1)
            else:
                count = changeTo10(v , i - 1)
                count += 1
                if i > 0:
                    count += changeTo00(1 << i-1, i-1)
                return count
            
        def changeTo00(u, i):
            print('00', u)
            if u == 0:
                print(2) 
                return 0
      
            
            # find the position of highest bit '1', -1 means no '1'
            pos = -1
            v = u
            while v:
                v = v >> 1
                pos += 1


            if pos >=0:
                # v = n clear the hightes bit '1'
                mask = 1 << pos
                v = u ^ mask

                # change v to 10..0 format
                count = changeTo10(v, pos - 1) 
                print('step' + str(count), p ^ mask)
                count += 1
                if pos > 0 :
                    count += changeTo00(1 << (pos -1), pos - 2)
                return count 
            else:
                return 0
            
        return changeTo00(n, 0)

if __name__ == "__main__":
    sol = Solution()
    # sol.generateParenthesis(8)
    print(sol.minimumOneBitOperations(333))
