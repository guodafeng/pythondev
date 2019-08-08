class Solution:
    def searchMatrix(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        """
        def binarySearch(values, target):
            if not values or not values[0]:
                return -1
            start = 0
            end = len(values) - 1
            while start <= end:
                mid = (start + end) // 2
                if values[mid][0] <= target and values[mid][-1] >= target:
                    return mid
                elif values[mid][0] > target:
                    end = mid
                    if start == mid:
                        return -1
                elif values[mid][-1] < target:
                    start = mid
                    if end == mid:
                        return -1
                if start == mid:
                    start += 1
            return -1

        matchRow = binarySearch(matrix, target)            
        print(matchRow)
        if matchRow >=0:
            matchPos = \
            binarySearch(list(zip(matrix[matchRow],matrix[matchRow])), target)
            print(matchPos)
        if matchRow >=0:
            if matchPos >=0:
                return True
            else:
                return False
        else:
            return False



matrix = [
  [1,   3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 50]
]
target = 3
matrix = [
  [1,   3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 50]
]
target = 13
sol = Solution()
print(sol.searchMatrix(matrix, target))

