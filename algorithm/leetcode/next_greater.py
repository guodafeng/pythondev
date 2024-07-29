class Solution:
    def next_greater(self, nums):
        if len(nums) < 1:
            return []

        i_st = [0]
        ret = [-1] * len(nums)
        for i, num in enumerate(nums[1:], 1):
            if i == i_st[-1]:
                break
            while len(i_st) > 0 and num > nums[i_st[-1]]:
                ret[i_st[-1]] = num
                i_st.pop()
            i_st.append(i)

        restart = 0
        while len(i_st) > 0:
            if len(i_st) > 1:
                for i in range(restart, i_st[0] + 1):
                    if nums[i_st[-1]] < nums[i]:
                        ret[i_st[-1]] = nums[i]
                        break
                restart = i

            i_st.pop()
        
        return ret


    def cycle_iter(self, nums):
        cur = 0
        length = len(nums)
        while True:
            cur = cur % length
            bar = yield nums[cur]
            print('bar', bar)
            if bar > 100:
                break;
            cur += 1
sol = Solution()
nums = [1,2,3,4,3]
# print(sol.next_greater(nums))
c_iter = sol.cycle_iter(nums)
next(c_iter)
count = 0
while True:
    num = c_iter.send(count)
    print(num)
    count += 1
    if count > 200:
        break


