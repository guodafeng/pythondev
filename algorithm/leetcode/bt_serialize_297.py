from printbtree import print_tree, random_tree

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        return str(self._serialize(root))
        
    def _serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        if root is None:
            return [None]
        else:
            return [root.val] + self._serialize(root.left) +\
        self._serialize(root.right)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        arr = eval(data)
        root = self._create_node(arr[0])
        if root is None:
            return root

        self._deserialize(root, arr, 1)

        return root
        
    def _deserialize(self, parent, arr, index):
        offset = 0
        left = self._create_node(arr[index])
        offset += 1
        if left is not None:
            offset += self._deserialize(left, arr, index + offset)

        right = self._create_node(arr[index + offset])
        offset += 1
        if right is not None:
            offset += self._deserialize(right, arr, index + offset)
        parent.left = left
        parent.right = right
        return offset


    def _create_node(self, elm):
        return elm if elm is None else TreeNode(elm)




# Your Codec object will be instantiated and called as such:
root = random_tree(30)
print_tree(root)

codec = Codec()
print(str(codec.serialize(root))) 
root2 = codec.deserialize(codec.serialize(root))
print_tree(root2)
