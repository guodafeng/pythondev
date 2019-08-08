# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def generateTrees(self, n):
        """
        :type n: int
        :rtype: List[TreeNode]
        """
        if n == 0:
            return []  
        memo = {}
        self.recur(1,n+1,memo)
        return memo[(1,n+1)]
        
    def recur(self,start,end,memo): #[start,end)
        if (start,end) in memo:
            return memo[(start,end)]
        if start >= end:
            memo[(start,end)] = [None]
            return [None]
        if start +1 == end:
            memo[(start,end)] = [TreeNode(start)]
            return [TreeNode(start)]
        
        ans =  []
        for root in range(start,end):
            for left in self.recur(start, root,memo):
                for right in self.recur(root+1,end   ,memo):
                    newTree = TreeNode(root)
                    newTree.left = left
                    newTree.right = right
                    ans.append(newTree)
        memo[(start,end)]  = ans   
        return ans
