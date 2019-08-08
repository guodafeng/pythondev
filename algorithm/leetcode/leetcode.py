class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
# Definition for an interval.
class Interval:
    def __init__(self, s=0, e=0):
        self.start = s
        self.end = e

       
class Solution:
    def employeeFreeTime(self, schedule):
        """
        :type schedule: List[List[Interval]]
        :rtype: List[Interval]
        """
        merged = None

        for elm in schedule:
            if not merged:
                merged = elm
            else:
                merged = self._merge_interval(merged, elm)

        return self._combine_merge(merged)

    def _combine_merge(self, merged):
        size = len(merged)
        out = []
        for i in range(1, size):
            out.append(Interval(merged[i-1].end,merged[i].start)
        return out


    def _merge_interval(self, emp1, emp2):
        out = []
        len1 = len(emp1)
        len2 = len(emp2)
        
        i1 = 0
        i2 = 0
        while i1 < len1 and i2 < len2:
            inter1 = emp1[i1]
            inter2 = emp2[i2]
            if inter1.end < inter2.start:
                out.append(inter1)
                i1 += 1
            elif inter2.end < inter1.start:
                out.append(inter2)
                i2 += 1
            elif inter1.end < inter2.end:
                inter2.start = min(inter1.start, inter2.start)
                i1 += 1
            elif inter2.end < inter1.end:
                inter1.start = min(inter1.start, inter2.start)
                i2 += 1
            elif inter1.end == inter2.end:
                inter1.start = min(inter1.start, inter2.start)
                out.append(inter1)
                i1+=1
                i2+=1

        for i in range(i1,len1):
            out.append(emp1[i])
        for i in range(i2,len2):
            out.append(emp2[i])

        return out


                


        
        for interval1 in emp1:
            for interval2 in emp2:


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


     # Definition for a binary tree node.
     # class TreeNode(object):
     #     def __init__(self, x):
     #         self.val = x
     #         self.left = None
     #         self.right = None
    def printTree(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[str]]
        """   

        def get_height(node):
            if node is None:
                return 0
            left_h = get_height(node.left)
            right_h = get_height(node.right)
            return max(left_h, right_h) + 1
        def fill_list(node, col, row, offset, res):
            if node is None:
                return
            res[row][col] = node.val
            fill_list(node.left, col - offset, row + 1, offset >> 1, res) 
            fill_list(node.right, col + offset, row + 1, offset >> 1, res) 

        height = get_height(root)
        col_num = (1 << height) - 1
        ret = [ ["" for i in range(col_num)]  for row in range(height)]

        offset = 1 << height - 1
        fill_list(root, col_num - offset, 0, offset>>1, ret)
        return ret



def random_tree(num):
    vals = [i for i in range(num)]
    root = None
    cur_node = root
    for val in vals:
        node = TreeNode(val)
        if root is None:
            root = node
        else:
            insert_to(root, node)

    return root
        
def insert_to(root, node):
    from random import randint
    cur_node = root
    while True:
        ran = randint(0,1)
        if ran > 0:
            if cur_node.left is None:
                cur_node.left = node
                break
            else:
                cur_node = cur_node.left
        else:
            if cur_node.right is None:
                cur_node.right = node
                break
            else:
                cur_node = cur_node.right

def test_close_ele():
    arr = [1,2,3,4,5]
    k = 4
    x = -1
    print (Solution().findClosestElements(arr, k, x))


def test_print_tree():
    root = random_tree(3)
    sol = Solution()
    res = sol.printTree(root)
    for row in res:
        print(row)

test_print_tree()
