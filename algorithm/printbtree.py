# Definition for a binary tree node.
from collections import namedtuple, deque
from itertools import zip_longest

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

Size = namedtuple('Size', ['left', 'right'])
MIN_GAP = 4

class Solution(object):
    def getBounder(self, root):
        """
        :type root:TreeNode
        :rtype [Size]
        """
        if root is None:
            return [],[]

        box = []
        tree = []

        left_box, left_tree = self.getBounder(root.left)
        right_box, right_tree = self.getBounder(root.right)
        offset = self.caculateGap(left_box, right_box)
        if offset < 0:
            left_box = [Size(sz.left - offset, sz.right - offset) for sz in
                    left_box]
            left_tree = [' ' * (-offset) + line for line in left_tree]
        elif offset > 0:
            right_box = [Size(sz.left + offset, sz.right + offset) for sz in
                    right_box]
            right_tree = [' ' * offset + line for line in right_tree]

        pos = 0
        if len(left_box)>0 and len(right_box)>0:
            pos = (right_box[0].left + left_box[0].right)//2
        elif len(left_box) > 0:
            pos = left_box[0].right + MIN_GAP//2
        elif len(right_box) > 0:
            pos = right_box[0].left - MIN_GAP//2
        box.append(Size(pos, pos))

        #merge left_box and right_box
        for sz_l, sz_r in zip_longest(left_box, right_box):
            if sz_l is not None and sz_r is not None:
                box.append( Size(sz_l.left, sz_r.right)) 
            if sz_l is None:
                box.append(sz_r)
            elif sz_r is None:
                box.append(sz_l)

        tree.append(' ' * pos + str(root.val))
        line = ''
        if root.left is not None:
            line = ' ' * ((pos + left_box[0].right)//2) + '/'

        if root.right is not None:
            line += ' ' * (((pos + right_box[0].left)//2) - len(line)) + '\\'
        tree.append(line)

        #merge left_tree and right_tree
        for line_l, line_r in zip_longest(left_tree, right_tree):
            line = ''
            if line_l is not None and line_r is not None:
                line = line_l + line_r[len(line_l):]
            elif line_l is not None:
                line = line_l
            elif line_r is not None:
                line = line_r
            tree.append(line)

        if root.val == 2:
            for t in right_tree:
                print(t)
            print(offset)
            for t in tree:
                print(t)
        return (box, tree)



    def caculateGap(self, left_box, right_box):
        if len(left_box) > 0 and len(right_box) > 0:
            dists = list(map(lambda x1, x2:x1.right - x2.left + MIN_GAP, left_box,
                    right_box))
            return max(dists)
        elif len(right_box) > 0 and right_box[0].left == 0:
            return MIN_GAP // 2
        else:
            return 0

class A(object):
    def run(self):
        print(self.getname())
    def getname(self):
        return "A"

class B(A):
    def getname(self):
        return "B"

def make_btree(vals):
    root = None
    cur_node = root
    for index, val in enumerate(vals):
        node = TreeNode(val)
        if cur_node is not None:
            if index % 2 == 0:
                cur_node.right = node
            else:
                cur_node.left = node

            

        cur_node = node
        if root is None:
            root = cur_node

    return root
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


def test_printtree():
    root = random_tree(40)
    sol = Solution()
    box, tree = sol.getBounder(root)
    print(box)
    for t in tree:
        print(t)

test_printtree()
