from BinaryTreeClass import BinaryTree
class LinkedBinaryTree(BinaryTree):
    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'
        def __init__(self, element, parent=None,left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
        class Position(BinaryTree.Position):
            def __init__(self, container,node):
                self._container = container
                self._node = node
            def element(self):
                return self._node._element
            def __eq__(self,other):
                return type(other) is type(self) and other._node is self._node
    def validate(self,p):
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:
            raise ValueError('p is no longer valid')
        return p._node
    def _make_position(self,node):
        return self.Position(self,node) if node is not None else None
    def __init__(self):
        self._root = None
        self._size = 0
    def __len__(self):
        return self._size
    def root(self):
        return self._make_position(self._root)
    def parent(self,p):
        node = self._validate(p)
        return self._make_position(node._parent)
    def left(self,p):
        node = self._validate(p)
        return self._make_position(node._left)
    def right(self,p):
        node = self.validate(p)
        return self._make_position(node._right)
    def num_children(self,p):
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
    def _add_root(self,e):
        if self._root is not None: raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)
    def _add_left(self,p,e):
        node = self._validate(p)
        if node._left is not None: raise ValueError('left child exists')
        self._size += 1
        node._left = self._Node(e,node)
        return self._make_position(node._left)
    def _add_right(self,p,e):
        node = self._validate(p)
        if node._left is not None: raise ValueError('right child exists')
        self._size += 1
        node._left = self._Node(e,node)
        return self._make_position(node._right)
    def _replace(self,p,e):
        node = self._validate(p)
        old = node._element
        node._element = e
        return old
    def _delete(self,p):
        node = self._validate(p)
        if self.num_children(p) == 2: raise ValueError('p has two children')
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        if node is self._root:
            self._root = child
        else:
            parents = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
            self._size -= 1
            node._parent = node
            return node._element

    def _attach(self, p, t1, t2):
        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError('position must be leaf')
        if not type(p) is type(t1) is type(t2):
            raise TypeError('tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node

            node._right = t2._root
            t2._root = None
            t2._size = 0
    def __iter__(self):
        for p in self.positinos():
            yield p.element()
    def preorder(self):
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p
    def _subtree_preorder(self,p):
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other
    def postorder(self):
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p
    def _subtree_postorder(self,p):
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p

    def breadthfirst(self):
        if not self.is_empty():
            fringe = LinkedQueue()
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                p = fringe.dequeue()
                yield p
                for c in self.children(p):
                    fringe.enqueue(c)
    def inorder(self):
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p
    def _subtree_inorder(self,p):
        if self.left(p) is not None:
            for other in self._subtree_inorder(self.left(p)):
                yield other
        if self.right(p) is not None:
            for other in self._subtree_inorder(self.right(p)):
                yield other
    def positions(self):
        return self.inorder()
