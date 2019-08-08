# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def rotateRight(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """
        listLen = 0
        node = head
        while node != None:
            node = node.next
            listLen += 1

        if listLen <= 1:
            return head

        # rotate place 
        rp = listLen - k % listLen
        if rp == listLen:
            return head

        i = 0
        node = head
        while i < rp - 1:
            node = node.next
            i += 1
        
        temp = head
        head = node.next
        node.next = None
        node = head
        while node.next != None:
            node = node.next
        node.next = tmp

        return head



        
