class Solution:
    def candyol(self, ratings):
        sort_r = sorted(ratings)
        prev_r = -1
        candies = [1] * len(ratings)
        for r in sort_r:
            if r == prev_r:
                prev_r = r
                continue
            prev_r = r
            for i, rate in enumerate(ratings):
                if rate == r:
                    if i >0 and ratings[i-1] > ratings[i] and \
                    candies[i-1] <= candies[i]:
                        candies[i-1] = candies[i] + 1
                    if i < (len(ratings)-1) and ratings[i+1] > ratings[i] and \
                    candies[i+1] <= candies[i]:
                        candies[i+1] = candies[i] + 1
        print(candies)
        return sum(candies)

    def candy(self, ratings):
        length = len(ratings)
        allocs = [1] * length
        for i in range(length):
            if i > 0 and ratings[i] > ratings[i-1]:
                allocs[i] = allocs[i-1] + 1

        for i in range(length-1,-1,-1):
            if i > 0 and ratings[i-1] > ratings[i]:
                allocs[i-1] = allocs[i] + 1

        print(allocs)


if __name__ == '__main__':
    sol = Solution()
    sol.candy([1,3,2,2,1])
    # sol.candy([1,0,2])
