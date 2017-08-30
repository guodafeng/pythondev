class Solution:
    def findClosestElements(self, arr, k, x):
        """
        :type arr: List[int]
        :type k: int
        :type x: int
        :rtype: List[int]
        """
        
        # find the closest one element
        size = len(arr)
        l = 0
        r = size - 1
        
        mid = (l + r) // 2
        dist = x - arr[mid]
        while dist != 0 and l < r:
            if dist > 0:
                l = mid + 1
            else:
                r = l if l == mid else mid - 1

            mid = (l + r) // 2
            dist = x - arr[mid]
            print(dist, mid)

        print(mid)
        # the closet element might be one in mid-1, mid, mid+1
        closet = mid
        if dist > 0 and mid < size -1 and arr[mid+1] - x < dist:
            closet = mid + 1
        elif dist < 0 and mid > 0 and arr[mid-1] -x > dist:
            closet = mid - 1

        print(closet)
        l = r = closet
        while r - l + 1 < k:
            if r == size -1 or (l > 0 and x - arr[l-1] <= arr[r+1] - x):
                l = l - 1
            else:
                r = r + 1

        return arr[l : r+1 ]


arr = [1,2,3,4,5]
k = 4
x = -1
print (Solution().findClosestElements(arr, k, x))
