from dataclasses import dataclass
from key import *


@dataclass
class Trie:
    branch: (any, any)
    key: Key

    def __init__(self):
        self.branch = (None, None)
        self.key = None

    def is_empty(self):
        return not self.key

    def is_leaf(self):
        return not self.branch[0] and not self.branch[1]

    def is_empty_leaf(self):
        return self.is_empty() and self.is_leaf()

    def is_non_empty_leaf(self):
        return not self.is_empty() and self.is_leaf()

    def size(self):
        return self.size_at_depth(0)

    def size_at_depth(self, depth):
        if self.is_leaf():
            return 0 if self.is_empty() else 1
        else:
            return self.branch[0].size_at_depth(depth + 1) + self.branch[1].size_at_depth(depth + 1)

    def add(self, key):
        return self.add_at_depth(0, key)

    def add_at_depth(self, depth, key):
        if self.is_empty_leaf():
            self.key = key
            return depth, True
        elif self.is_non_empty_leaf():
            if key == self.key:
                return depth, False
            else:
                p = self.key
                self.key = None
                self.branch = (Trie(), Trie())
                self.branch[p.bit_at(depth)].key = p
                return self.branch[key.bit_at(depth)].add_at_depth(depth + 1, key)
        else:
            return self.branch[key.bit_at(depth)].add_at_depth(depth + 1, key)

    def remove(self, key):
        return self.remove_at_depth(0, key)

    def remove_at_depth(self, depth, key):
        if self.is_empty_leaf():
            return depth, False
        elif self.is_non_empty_leaf():
            self.key = None
            return depth, True
        else:
            d, removed = self.branch[key.bit_at(depth)].remove_at_depth(depth + 1, key)
            if removed:
                self.shrink()
                return d, True
            else:
                return d, False

    def find(self, key):
        return self.find_at_depth(0, key)

    def find_at_depth(self, depth, key):
        if self.is_empty_leaf():
            return None, depth
        elif self.is_non_empty_leaf():
            return self.key, depth
        else:
            return self.branch[key.bit_at(depth)].find_at_depth(depth + 1, key)

    def list_of_depths(self):
        return self.list_of_depths_at_depth(0)

    def list_of_depths_at_depth(self, depth):
        if self.is_empty_leaf():
            return []
        elif self.is_non_empty_leaf():
            return [depth]
        else:
            l0 = self.branch[0].list_of_depths_at_depth(depth + 1)
            l1 = self.branch[1].list_of_depths_at_depth(depth + 1)
            return l0 + l1

    def shrink(self):
        b0, b1 = self.branch[0], self.branch[1]
        if b0.is_empty_leaf() and b1.is_empty_leaf():
            self.branch = (None, None)
        elif b0.is_empty_leaf() and b1.is_non_empty_leaf():
            self.key = b1.key
            self.branch = (None, None)
        elif b0.is_non_empty_leaf() and b1.is_empty_leaf():
            self.key = b0.key
            self.branch = (None, None)
