from random import randint
import numpy as np

class TreeNode:

    def __init__(self, parent) -> None:
        self.parent = parent
        self.lc = None
        self.rc = None
        self.li = None # left and right index, [li, ri] inclusive on both side
        self.ri = None
        self.value = None

class SegmentTree:

    def __init__(self, data: list, operation: callable=None) -> None:
        self.root = TreeNode(None)
        self.root.li = 0
        self.root.ri = len(data) - 1
        self.data = data
        if operation is None:
            self.operation = lambda a, b: a + b # max(a, b)
        else:
            self.operation = operation
        self._build_tree()

    def query(self, li, ri):
        if li > ri:
            li, ri = ri, li
        if li < 0 or ri >= len(self.data):
            raise ValueError("Query out of range.")
        
        return self._query(self.root, li, ri)

    def _query(self, node, li, ri):
        if node.li == li and node.ri == ri:
            return node.value
        if ri <= node.lc.ri:
            return self._query(node.lc, li, ri)
        elif li >= node.rc.li:
            return self._query(node.rc, li, ri)
        else:
           return self.operation(self._query(node.lc, li, node.lc.ri), self._query(node.rc, node.rc.li, ri))

    def update(self, li=None, ri=None):
        if li is None:
            li = 0
        if ri is None:
            ri = len(self.data)
        self._update(self.root, li, ri)

    def _update(self, node, li, ri):
        if node.li == node.ri:
            node.value = self.data[li]
            return
        if ri <= node.lc.ri:
            self._update(node.lc, li, ri)
        elif li >= node.rc.li:
            self._update(node.rc, li, ri)
        else:
            self._update(node.lc, li, node.lc.ri)
            self._update(node.rc, node.rc.li, ri)
        node.value = self.operation(node.lc.value, node.rc.value)

    def __str__(self):
        return self._traverse_inorder(self.root)

    def _traverse_inorder(self, node):
        if node is None:
            return ''
        if node.is_leaf():
            return str(node.value)
        else:
            return f'({self._traverse_inorder(node.lc)}, {str(node.value)}, {self._traverse_inorder(node.rc)})'

    def _build_tree(self):
        self._build(self.root)

    def _build(self, node):
        if node.li == node.ri:
            node.value = self.data[node.li]
            return

        node.lc = TreeNode(node)
        node.lc.li = node.li
        node.lc.ri = node.li + (node.ri - node.li) // 2
        node.rc = TreeNode(node)
        node.rc.li = node.li + (node.ri - node.li) // 2 + 1
        node.rc.ri = node.ri
        
        self._build(node.lc)
        self._build(node.rc)
        
        node.value = self.operation(node.lc.value, node.rc.value)


def test():
    data = np.array([randint(-100, 100) for _ in range(100)], dtype=np.int64)
    tree = SegmentTree(data)
    num_tests = 100
    for _ in range(num_tests):
        l, r = randint(0, len(data) - 1), randint(0, len(data) - 1)
        if l > r:
            l, r = r, l
        assert tree.query(l, r) == data[l:r+1].sum()
        

if __name__ == '__main__':
    test()