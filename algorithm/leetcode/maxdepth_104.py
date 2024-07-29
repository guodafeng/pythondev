# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def maxDepth(root):
    if root:
        return max(maxDepth(root.left), maxDepth(root.right)) + 1
    else:
        return 0
