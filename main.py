


class PriorityQueue:
    def __init__(self, init_list=[], sort_fn=False):
        self.queue = init_list
        if sort_fn:
            self.queue.sort(key=sort_fn)
    
    def is_empty(self):
        return len(self) == 0

    def max(self):
        return self.queue.pop()
    
    def insert(self, element, priority):
        self.queue.insert(priority, element)


class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.height = 0


# my implementation of an AVL (self-balanced binary search) tree data structure
class AVLTree:

    def __init__(self, value = None, values=[], comparison_fn=lambda x : x):

        # the comparison_fn needs to be injective in order for this data structure to function as expected
        self.comparison_fn = comparison_fn

        self.root = None
        self.height = 0

        # initialise a root node
        if value is not None:
            self.root = Node(value)
            self.height = 1
        
        for x in values:
            self.insert(x)
    
    # returns an ordered list of every node in the tree
    def list_tree(self):
        return self.list_subtree(self.root)

    # returns an ordered list of every node in the subtree starting at a specified node
    def list_subtree(self, node):
        L = []

        if node != None:
            L += self.list_subtree(node.left_child)
            L.append(node)
            L += self.list_subtree(node.right_child)
        
        return L

    # print value, parent value, and height for each node in the tree (assuming printable values)
    def print(self):
        self.print_subtree(self.root)

    # print value, parent value, and height for each node in the subtree starting at a given node (assuming printable values)
    def print_subtree(self, node):
        L = self.list_subtree(node)

        for l in L:
            if l is not self.root:
                print("Node", l.value, "is the child of", l.parent.value, ", at height", l.height)
            else:
                print("Node", l.value, "is the root, at height", l.height)

    # insert a given value into the tree (if it isn't already present), while maintaining order and balance.
    # (requires injectivity of comparison_fn to behave in the expected manner)
    def insert(self, value):
        self.__insert_at(value, self.root)

    # insert a value into the tree, subordinate to a given node
    # (potential undesired behaviour for non-None nodes not already present in the tree... try saying that quickly five times)
    def __insert_at(self, value, node):

        # initialise root, if necessary
        if self.root == None:
            self.root = Node(value)
            return self.root
        
        # instantiate new leaf node
        elif node == None:
            node = Node(value)
            return node

        # find valid location for new node, if not already present
        compare = self.comparison_fn(value) - self.comparison_fn(node.value)

        if compare < 0:
            node.left_child = self.__insert_at(value, node.left_child)

            if node.height <= node.left_child.height:
                node.height = node.left_child.height + 1

            node.left_child.parent = node

        if compare > 0:
            node.right_child = self.__insert_at(value, node.right_child)

            if node.height <= node.right_child.height:
                node.height = node.right_child.height + 1

            node.right_child.parent = node
            
        self.__rebalance_at(node)
        return node
    
    def delete(self, value):
        self.__delete_at(value, self.root)

    def __delete_at(self, value, node):
        # TODO: delete value from tree
        return

    def balance_at(self, node):
        left_height = right_height = -1

        if node.left_child != None:
            left_height = node.left_child.height

        if node.right_child != None:
            right_height = node.right_child.height
        
        return left_height - right_height
    
    def __rebalance_at(self, node):
        balance = self.balance_at(node)

        # early out if already balanced
        if abs(balance) > 1:
            # TODO: rotate things til balanced
            return
    
    def search(self, value):
        return self.search_subtree(self, self.root, value)
    
    def search_subtree(self, node, value):
        # TODO: search tree
        return
    
    def min(self):
        node = self.root

        while node.left_child != None:
            node = node.left_child
        
        return node
    
    def max(self):
        node = self.root

        while node.right_child != None:
            node = node.right_child
        
        return node
        

import random

my_values = [4,3,6,1,5,0,2]
my_values = random.sample(my_values, k = len(my_values))

a = AVLTree(values=my_values)

a.print()

    
