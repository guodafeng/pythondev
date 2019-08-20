from typing import List

def maxNumber2(nums1: List[int], nums2: List[int], k: int) -> List[int]:
    def maxNumber(nums, k):
        drop = len(nums) - k # count number can be dropped
        out = []
        for num in nums:
            while out and out[-1] < num and drop > 0:
                out.pop()
                drop -= 1
            out.append(num)
        return out[:k]

    def merge(a, b, k):
        return [max(a, b).pop() for _ in a + b]

    out = []
    for i in range(k + 1):
        a = maxNumber(nums1, i)
        b = maxNumber(nums2, k-i)
        out.append(merge(a, b, k))

    return max(out)

def maxNumber(nums1, nums2, k):
    def prep(nums, k):
        drop = len(nums) - k
        out = []
        for num in nums:
            while drop and out and out[-1] < num:
                out.pop()
                drop -= 1
            out.append(num)
        return out[:k]

    def merge(a, b):
        return [max(a, b).pop(0) for _ in a+b]

    return max(merge(prep(nums1, i), prep(nums2, k-i))
               for i in range(k+1)
               if i <= len(nums1) and k-i <= len(nums2))

# too time consuming
# count = 0
# def max_till(nums):
    # # return list contain index which has max num till current
    # # index
    # size = len(nums)
    # if size == 0:
        # return []
    # else:
        # maxs = [0] * size
        # for i, num in enumerate(nums[1:]):
            # if num > nums[maxs[i]]:
                # maxs[i+1] = i+1
            # else:
                # maxs[i+1] = maxs[i]
        # return maxs

# def maxNumber(nums1: List[int], nums2: List[int], k: int) -> List[int]:
    # global count
    # count += 1
    # if k==0:
        # return []
    # size1 = len(nums1)
    # size2 = len(nums2)

    # if size1 == 0:
        # maxs2 = max_till(nums2)
        # max2_i = maxs2[min(size2-1, size1 + size2 - k)]
        # return [nums2[max2_i]] + maxNumber(nums1, nums2[max2_i+1:], k-1)
    # elif size2 == 0:
        # maxs1 = max_till(nums1)
        # max1_i = maxs1[min(size1-1, size1 + size2 - k)]
        # return [nums1[max1_i]] + maxNumber(nums1[max1_i+1:], nums2, k-1)

    # maxs1 = max_till(nums1)
    # maxs2 = max_till(nums2)

    # max1_i = maxs1[min(size1-1, size1 + size2 - k)]
    # max2_i = maxs2[min(size2-1, size1 + size2 - k)]

    # if nums1[max1_i] > nums2[max2_i]:
        # return [nums1[max1_i]] + maxNumber(nums1[max1_i+1:], nums2, k-1)
    # elif nums1[max1_i] < nums2[max2_i]: 
        # return [nums2[max2_i]] + maxNumber(nums1, nums2[max2_i+1:], k-1)
    # else: #equal
        # nextMax1 = maxNumber(nums1[max1_i+1:], nums2, k-1)
        # nextMax2 = maxNumber(nums1, nums2[max2_i+1:], k-1)
        # return [nums1[max1_i]] + max(nextMax1, nextMax2)


if __name__ == '__main__':

    a = [6,4,7,8,6,5,5,3,1,7,4,9,9,5,9,6,1,7,1,3,6,3,0,8,2,1,8,0,0,7,3,9,3,1,3,7,5,9,4,3,5,8,1,9,5,6,5,7,8,6,6,2,0,9,7,1,2,1,7,0,6,8,5,8,1,6,1,5,8,4]
    b = [3,0,0,1,4,3,4,0,8,5,9,1,5,9,4,4,4,8,0,5,5,8,4,9,8,3,1,3,4,8,9,4,9,9,6,6,2,8,9,0,8,0,0,0,1,4,8,9,7,6,2,1,8,7,0,6,4,1,8,1,3,2,4,5,7,7,0,4,8,4]
    print(maxNumber2(a, b, 70))
