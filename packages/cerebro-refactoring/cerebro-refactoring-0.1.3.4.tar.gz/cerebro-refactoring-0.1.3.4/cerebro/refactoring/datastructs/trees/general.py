# ------------------------------------------------------------------------------
#  MIT License
#
#  Copyright (c) 2021 Hieu Pham. All rights reserved.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# ------------------------------------------------------------------------------

from typing import Union, List
from cerebro.refactoring.objects import Object


class Tree(Object):
    """
    This is base node to build general tree. The tree node can have children nodes.
    ---------
    @author:    Hieu Pham.
    @created:   10.10.2021.
    @updated:   11.10.2021.
    """

    @property
    def parent(self):
        """
        Get node parent.
        :return: node parent.
        """
        return self._parent

    @property
    def is_root(self):
        """
        Check if this is root.
        :return: is root.
        """
        return self._parent is None

    @property
    def root(self):
        """
        Get tree root.
        :return: root node.
        """
        node = self
        while not node.is_root:
            node = node.parent
        return node

    @property
    def level(self):
        """
        Get node level.
        :return: node level.
        """
        return self._level

    @property
    def index(self):
        """
        Get node index.
        :return: node index.
        """
        return self._index

    @property
    def children(self):
        """
        Get children nodes.
        :return: children nodes.
        """
        return [node for node in self._children]

    @property
    def is_leaf(self):
        """
        Check if this is a leaf.
        :return: is leaf.
        """
        return len(self._children) == 0

    def __init__(self, children=None, **kwargs):
        """
        Create new object.
        "param children: children nodes.
        :param kwargs:   keyword arguments.
        """
        super(Tree, self).__init__(**kwargs)
        # Initialize attributes.
        self._parent = None
        self._level = 0
        self._index = 0
        # Attach children nodes.
        self._children = list()
        self.attach(children=children, **kwargs)

    def data(self, **kwargs) -> dict:
        """
        Get object data.
        :param kwargs:  keyword arguments.
        :return:        object data.
        """
        data = super().data(**kwargs)
        if not self.is_leaf:
            data.update({'children': [node.data(**kwargs) for node in self._children]})
        return data

    def attach(self, children=None, **kwargs):
        """
        Attach children node(s) to tree.
        :param children:   node(s) to be attached.
        :param kwargs:     additional keyword arguments.
        :return:           node(s).
        """
        if children is None:
            return self, None
        # Attach single node.
        elif isinstance(children, Tree):
            children._parent = self
            children._level = self._level + 1
            children._index = len(self._children)
            self._children.append(children)
            return self, children
        # Attach list of nodes
        elif isinstance(children, list):
            return self, [self.attach(node, **kwargs)[-1] for node in children]
        # Otherwise raise error because of invalid nodes.
        raise TypeError("Tree can only attach tree node(s).")

    def detach(self, indexes: Union[None, int, List[int]] = None, **kwargs):
        """
        Detach node(s) from tree.
        :param indexes: index(es) of node(s) to be detached.
        :param kwargs:  additional keyword arguments.
        :return:        node(s).
        """
        if indexes is None:
            return self, None
        # Detach single node.
        elif isinstance(indexes, int):
            node = self._children.pop(indexes)
            node._parent = None
            node._level = 0
            node._index = 0
            for i in range(len(self._children)):
                self._children[i]._index = i
            return self, node
        # Detach list of indexes.
        elif isinstance(indexes, list):
            return self, [self.detach(i, **kwargs)[-1] for i in indexes]
        # Otherwise raise error because of invalid indexes.
        raise TypeError("Tree can only detach node(s) base on index(es) of them.")

    def clean(self, **kwargs):
        """
        Clean all children.
        :param kwargs:  keyword arguments.
        """
        return self.detach([i for i in range(len(self._children))])

    def move(self, steps: Union[None, int, List[int]] = 0, **kwargs):
        """
        Move to another node from current node.
        :param steps:   steps to go.
        :param kwargs:  keyword arguments.
        :return:        destination node.
        """
        if steps is None:
            return self.root
        # Go single step.
        elif isinstance(steps, int):
            current = self
            # Go forward.
            if steps > 0:
                current = self._children[steps]
            # Go backward.
            elif steps < 0:
                move = abs(steps)
                if move < self.level:
                    for _ in range(move):
                        current = current.parent
                else:
                    raise IndexError("Out of tree index.")
            # Return result
            return current
        # Go list of steps.
        elif isinstance(steps, list):
            current = self
            for step in steps:
                current = current.go(step, **kwargs)
            return current
        # Otherwise raise error because of invalid steps.
        raise TypeError("Can only move on tree based on integer step(s).")
