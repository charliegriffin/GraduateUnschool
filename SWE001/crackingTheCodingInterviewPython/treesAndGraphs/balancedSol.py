#I'm copying the solution online so I can play with and understand it

import random

#binary tree python
class BinaryTree:
    def __init__(self, content):
        self.content = content
        self.left = None
        self.right = None
        #-1 means depth has not been calculated yet.
        self.depth = -1
    
    def __str__(self):
        return "( " + str(self.content) + " (" + str(self.left) + " | " + str(self.right) + "))"
        
#implement a function to check if a binary tree is balanced.

#O(n^2) naive algorithm
def is_balanced_binary_tree(btree):
    #compare depths of both sides
    if btree is None: return True
    return (abs(depth(btree.left) - depth(btree.right)) <= 1) and \
        is_balanced_binary_tree(btree.left) and is_balanced_binary_tree(btree.right)

def depth(btree):
    if btree is None:
       return 0
    else:
        if btree.depth != -1:
            return btree.depth
        else:
            btree.depth = 1 + max(depth(btree.left), depth(btree.right))
            return btree.depth
            
#testing
bt = BinaryTree(random.randint(0, 100))
for c1 in xrange(0,19):
    bt2 = BinaryTree(random.randint(0, 100))
    bt2.left = bt
    bt = bt2

unbalanced_tree = bt