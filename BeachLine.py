import math
import sys
import time
import graphviz
import subprocess

DEFAULT = object()

# encodes, and provides an interface for, parabolics arcs with fixed focus, and a variable (horizontal) directrix
class Arc:
    def __init__(self, focus):

        # geometric data
        self.focus = focus
        self.event = None
        self.left_halfedge = None
        self.right_halfedge = None

        # data for tree structure
        self.parent = None
        self.left = None
        self.right = None
        self.previous = None
        self.next = None
        self.height = 0

    # produce a list of the coefficients for the associated quadratic function, given the current directrix y-value
    def Coefficents(self, directrix):
        a = 1 / (2 * (self.focus[1] - directrix))
        b = -2 * a * self.focus[0]
        c = a * (self.focus[0]**2 + self.focus[1]**2 - directrix**2)
        return [a,b,c]

    # evaluate value of the quadratic at x, given the current directrix y-value
    def Evaluate(self, x, directrix):
        return ((x - self.focus[0])**2 / (2 * (self.focus[1] - directrix))) + ((self.focus[1] + directrix) / 2)

    # returns a list of all (real, internal) intersection points (in list form [x,y]) between two parabolic arcs
    def Intersections(self, other, directrix):
        # get the coefficients and form a difference of quadratic functions
        A = self.coefficents(directrix)[0] - other.coefficents(directrix)[0]
        B = self.coefficents(directrix)[1] - other.coefficents(directrix)[1]
        C = self.coefficents(directrix)[2] - other.coefficents(directrix)[2]
        discriminant = B**2 - 4*A*C
        out = []
        
        if A == 0:
            if B==0:
                if C==0:
                    print("Infinitely many intersections: parabolae overlap on an interval.", file=sys.stderr)
                    return None

            else: # the parabolae are horizontal translations of one another, and have a single intersection
                out.append(-C/B)

        else:
            if discriminant == 0: # double root
                intersection_x = -B / (2 * A)
                out.append(intersection_x)
            
            elif discriminant > 0: # distinct real roots
                intersection_x1 = (-B + math.sqrt(discriminant))/(2*A)
                intersection_x2 = (-B - math.sqrt(discriminant))/(2*A)
                out.append(intersection_x1)
                out.append(intersection_x2)
        
        return out



class FortuneTree: # basically a combination of an AVL tree and a doubly-linked list, with parabolic arcs at each node
    def __init__(self, arc):

        self.root = arc      

    def GetHeight(self, arc):

        if arc == None:
            return -1
        
        return arc.height

    def GetBalance(self, arc):

        return self.GetHeight(arc.left) - self.GetHeight(arc.right)

    def RecalculateHeight(self, arc):

        if arc == None:
            return -1
        
        return 1 + max(self.GetHeight(arc.left), self.GetHeight(arc.right))

    def RotateRight(self, arc):

        x = arc.left
        y = x.right
        
        # do the rotation
        x.right = arc
        x.parent = arc.parent
        arc.parent = x
        arc.left = y
        if y != None:
            y.parent = arc
        
        # recalculate heights
        self.RecalculateHeight(arc)
        self.RecalculateHeight(x)

        return x
    
    def RotateLeft(self, arc):

        x = arc.right
        y = x.left
        
        # do the rotation
        x.left = arc
        x.parent = arc.parent
        arc.parent = x
        arc.right = y
        if y != None:
            y.parent = arc
        
        # recalculate heights
        self.RecalculateHeight(arc)
        self.RecalculateHeight(x)

        return x

    def Rebalance(self, arc, balance):

        if balance > 1:
            # left-heavy
            x = arc.left
            
            if self.GetBalance(x) < 0:
                # do left-right rotation
                arc.left = self.RotateLeft(x)
                arc = self.RotateRight(arc)
            else:
                # just do right rotation
                arc = self.RotateRight(arc)
        
        if balance < -1:
            # right-heavy
            x = arc.right
            
            if self.GetBalance(x) > 0:
                # do right-left rotation
                arc.right = self.RotateRight(x)
                arc = self.RotateLeft(arc)
            else:
                # do left rotation
                arc = self.RotateLeft(arc)

        return self.GetBalance(arc)

    def FixSubtree(self, arc = DEFAULT):

        if arc == DEFAULT:
            arc = self.root

        if arc == None:
            return
        
        self.FixSubtree(arc.left)
        self.FixSubtree(arc.right)
        
        balance = self.GetBalance(arc)

        while abs(balance) > 1:
            balance = self.Rebalance(arc, balance)
        
        return

    def Min(self, subtree):

        arc = subtree

        while arc.left != None:
            arc = arc.left
        
        return arc

    def Max(self, subtree):
        
        arc = subtree

        while arc.right != None:
            arc = arc.right
        
        return arc

    def Successor(self, arc):

        if arc.right != None:
            return self.Min(arc.right)
                
        successor = arc

        while successor.parent != None:
            if successor == successor.parent.left:
                return successor.parent
            successor = successor.parent
        
        return None
    
    def Predecessor(self, arc):

        if arc.left != None:
            return self.Max(arc.left)
                
        predecessor = arc

        while predecessor.parent != None:
            if predecessor == predecessor.parent.right:
                return predecessor.parent
            predecessor = predecessor.parent
        
        return None

    def InsertBefore(self, arc, newarc):

        if arc.left == None:
            arc.left = newarc
            newarc.parent = arc
        
        else:
            pred = self.Predecessor(arc)
            pred.right = newarc
            newarc.parent = pred
        
        newarc.previous = arc.previous
        newarc.next = arc
        if newarc.previous != None:
            newarc.previous.next = newarc
        arc.previous = newarc
        
        self.FixSubtree()
        return
    
    def InsertAfter(self, arc, newarc):

        if arc.right == None:
            arc.right = newarc
            newarc.parent = arc
        
        else:
            succ = self.Successor(arc)
            succ.left = newarc
            newarc.parent = succ
        
        newarc.next = arc.next
        newarc.previous = arc
        if newarc.next != None:
            newarc.next.previous = newarc
        arc.next = newarc
        
        self.FixSubtree()
        return
    
    def Replace(self, arc, replacement):

        if arc.parent == None:
            self.root = replacement
            replacement.parent = None
        elif arc == arc.parent.left:
            arc.parent.left = replacement
            replacement.parent = arc.parent
        else:
            arc.parent.right = replacement
            replacement.parent = arc.parent

        return

    def Delete(self, arc):

        if arc.left == None:
            replacement = arc.right
            self.Replace(arc, arc.right)
        
        elif arc.right == None:
            replacement = arc.left
            self.Replace(arc, arc.left)
        
        else: # node has two children, crown its successor!
            replacement = arc.next
            
            if replacement.parent != arc:
                self.Replace(replacement, replacement.right)
                replacement.right = arc.right
                arc.right.parent = replacement
            
            self.Replace(arc, replacement)
            replacement.left = arc.left
            arc.left.parent = replacement

        if arc.previous != None:
            arc.previous.next = arc.next
        if arc.next != None:
            arc.next.previous = arc.previous

        arc = None
        self.FixSubtree()

        return replacement

    # generates a pdf file containing a plot of the tree, via the graphviz package
    def PlotTree(self):
        current_time = time.time()
        # TODO: fix this
        # nodes = self.list_tree()
        # dot = graphviz.Digraph()

        # for node in nodes:
        #     dot.node(f"{node.value}")

        #     if node.left_child != None:
        #         dot.edge(f"{node.value}",f"{node.left_child.value}")

        #     if node.right_child != None:
        #         dot.edge(f"{node.value}",f"{node.right_child.value}")
        
        # file_path = f"graphviz_outputs/avl_tree_{current_time}"
        # dot.render(file_path, cleanup=True)


class BeachLine(FortuneTree):
    def __init__(self, site):
        FortuneTree.__init__(self, Arc(site))
    
    def GetBreakpoints(self, sweepline):
        breakpoints = []
        # TODO: figure this shit out
        return breakpoints













