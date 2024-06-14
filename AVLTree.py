import time
import graphviz
import subprocess

class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.height = 0


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
        
        self.validate()
    
    def get_height(self, node):
        if node == None:
            return -1
        return node.height

    def balance_at(self, node):
        return self.get_height(node.left_child) - self.get_height(node.right_child)

    # make sure this is indeed a balanced binary search tree
    def validate(self):
        # TODO: this is very brute-force, refactor with some elegant recursion
        nodes = self.list_tree()

        for node in nodes:
            assert abs(self.balance_at(node)) <= 1
            
            assert node.height == 1 + max(self.get_height(node.left_child), self.get_height(node.right_child))
            
            if node.right_child != None:
                assert node.value < self.subtree_min(node.right_child).value
            
            if node.left_child != None:
                assert node.value > self.subtree_max(node.left_child).value
             
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

    # generates a pdf file containing a plot of the tree, via the graphviz package
    def generate_plot(self, show=False):
        current_time = time.time()
        nodes = self.list_tree()
        dot = graphviz.Digraph()

        for node in nodes:
            dot.node(f"{node.value}")

            if node.left_child != None:
                dot.edge(f"{node.value}",f"{node.left_child.value}")

            if node.right_child != None:
                dot.edge(f"{node.value}",f"{node.right_child.value}")
        
        file_path = f"graphviz_outputs/avl_tree_{current_time}"
        dot.render(file_path, cleanup=True)

        if show:
            subprocess.run(["wslview", file_path+".pdf"])

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
        self.root = self.__insert_at(value, self.root)

    # private insertion method to run recursively
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
            node.left_child.parent = node

            if node.height <= node.left_child.height:
                node.height = node.left_child.height + 1

        if compare > 0:
            node.right_child = self.__insert_at(value, node.right_child)
            node.right_child.parent = node

            if node.height <= node.right_child.height:
                node.height = node.right_child.height + 1

        # rebalance tree, if necessary
        balance = self.balance_at(node)

        if balance == 2:
            # left-heavy
            x = node.left_child
            
            if self.balance_at(x) == -1:
                # do left-right rotation
                node.left_child = self.left_rotation(x)
                node = self.right_rotation(node)
            else:
                # do right rotation
                node = self.right_rotation(node)
        
        if balance == -2:
            # right-heavy
            x = node.right_child
            
            if self.balance_at(x) == 1:
                # do right-left rotation
                node.right_child = self.right_rotation(x)
                node = self.left_rotation(node)
            else:
                # do left rotation
                node = self.left_rotation(node)

        balance = self.balance_at(node)
        assert abs(balance) <= 1, "rebalancing failed!"
        
        return node
        
    def delete(self, value):
        self.root = self.__delete_at(value, self.root)

    def __delete_at(self, value, node):
        
        if node == None:
            return node
        
        # if the current node is not the one to be deleted, pass the call down the chain
        if value < node.value:
            node.left_child = self.__delete_at(value, node.left_child)

        elif value > node.value:
            node.right_child = self.__delete_at(value, node.right_child)

        else:   # kill the node, and deal with its orphans
            if node.left_child == None:
                replacement = node.right_child
                node = None
                return replacement
            
            elif node.right_child == None:
                replacement = node.left_child
                node = None
                return replacement
            
            else:   # node has two children, find the successor and move it into place
                replacement = self.successor(node)
                node.value = replacement.value
                node.right_child = self.__delete_at(replacement.value, node.right_child)

        assert node != None, "not sure how this could happen, but we'll see!"

        node.height = 1 + max(self.get_height(node.left_child), self.get_height(node.right_child))

        # rebalance tree, if necessary
        balance = self.balance_at(node)

        if balance > 1:
            # left-heavy
            x = node.left_child
            
            if self.balance_at(x) < 0:
                # do left-right rotation
                node.left_child = self.left_rotation(x)
                node = self.right_rotation(node)
            else:
                # do right rotation
                node = self.right_rotation(node)
        
        if balance < -1:
            # right-heavy
            x = node.right_child
            
            if self.balance_at(x) > 0:
                # do right-left rotation
                node.right_child = self.right_rotation(x)
                node = self.left_rotation(node)
            else:
                # do left rotation
                node = self.left_rotation(node)

        balance = self.balance_at(node)
        assert abs(balance) <= 1, "rebalancing failed!"

        return node

    def right_rotation(self, node):

        # this will only be called if x exists
        x = node.left_child
        y = x.right_child
        
        # do the rotation
        x.right_child = node
        x.parent = node.parent
        node.parent = x
        node.left_child = y
        if y != None:
            y.parent = node
        
        # recompute heights
        node.height = 1 + max(self.get_height(node.left_child), self.get_height(node.right_child))
        x.height = 1 + max(self.get_height(x.left_child), self.get_height(x.right_child))
        
        return x
    
    def left_rotation(self, node):

        # this will only be called if x exists
        x = node.right_child
        y = x.left_child
        
        # do the rotation
        x.left_child = node
        x.parent = node.parent
        node.parent = x
        node.right_child = y
        if y != None:
            y.parent = node
        
        # recompute heights
        node.height = 1 + max(self.get_height(node.left_child), self.get_height(node.right_child))
        x.height = 1 + max(self.get_height(x.left_child), self.get_height(x.right_child))
        
        return x
        
    def search(self, value):
        return self.search_subtree(self, self.root, value)
    
    def search_subtree(self, node, value):
        # TODO: search tree
        return None
    
    def min(self):
        return self.subtree_min(self.root)
    
    def successor(self, node):

        if node.right_child != None:
            return self.subtree_min(node.right_child)
                
        current_node = node

        while current_node.parent != None:
            if current_node == current_node.parent.left_child:
                return current_node.parent
            current_node = current_node.parent
        
        return node
      
    def subtree_min(self, node):
        current_node = node

        while current_node.left_child != None:
            current_node = current_node.left_child
        
        return current_node
    
    def max(self):
        return self.subtree_max(self.root)
    
    def predecessor(self, node):
        return # TODO
    
    def subtree_max(self, node):
        current_node = node

        while current_node.right_child != None:
            current_node = current_node.right_child
        
        return current_node