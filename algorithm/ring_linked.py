class Node:
    def __init__(self,x):
        self.val = x
        self.next = None

def create_list(arr):

    """
    ['a', 'b',..'g']  to 'a->b->..->g'
    """
    head = None
    cur = None
    created = {}
    for val in arr:
        # to support linked list with ring
        if val in created:
            node = created[val]
        else:
            node = Node(val)
            created[val] = node

        if head is None:
            head = node
            cur = head
        else:
            cur.next = node
            cur = node
    return head


def print_list(node):
    out = ''
    visited = {}
    while node is not None and node not in visited:
        visited[node] = node
        out += node.val
        out += ' -> '

        node = node.next
    if node is not None:
        out += node.val
    else:
        out += 'None'

    print(out)


def find_ring_start(head):
    node1 = head
    node2 = head
    i = 0
    while node1 is not None and node2 is not None:
        i += 1
        node2 = node2.next
        if node2 is None:
            break
        else: 
            node2 = node2.next
        node1 = node1.next

        if node1 == node2:
            # ring found
            print(i)
            break
    node1 = head
    while node2 is not None:
        node2 = node2.next
        node1 = node1.next
        if node1 == node2:
            # start found
            break

    return node2


def test():
    arr = list('abcdefghijk')
    print_list(create_list(arr))

    arr = list('abcdefghijkd')
    print_list(create_list(arr))

    arr = list('abcdefghijklmnopqrstuvwxyz1234567893')
    start = find_ring_start(create_list(arr))
    print(start.val)
test()
