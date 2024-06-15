import math
import sys

import AVLTree

# encodes, and provides an interface for, parabolics arcs with fixed focus, and a variable (horizontal) directrix
class ParabolicArc:
    def __init__(self, focus=[0,0], start=-math.inf, end=math.inf, label=0):
        
        # order given bounds correctly
        if start > end:
            start, end = end, start

        # set parameters
        self.focus = focus
        self.left_bound = start
        self.right_bound = end
        self.label = label
    
    # produce a list of the coefficients for the associated quadratic function, given the current directrix y-value
    def coefficents(self, directrix):
        a = 1 / (2 * (self.focus[1] - directrix))
        b = -2 * a * self.focus[0]
        c = a * (self.focus[0]**2 + self.focus[1]**2 - directrix**2)
        return [a,b,c]

    # evaluate value of the quadratic at x, given the current directrix y-value
    def evaluate(self, x, directrix):
        return ((x - self.focus[0])**2 / (2 * (self.focus[1] - directrix))) + ((self.focus[1] + directrix) / 2)

    # returns a list of all (real, internal) intersection points (in list form [x,y]) between two parabolic arcs
    def intersections(self, other, directrix):
        # an intersection point must be in the relative interior of both arcs
        if self.right_bound <= other.left_bound or other.right_bound <= self.left_bound:
            return []
        
        # non-parallel quadratic case - use quadratic formula!
        A = self.coefficents(directrix)[0] - other.coefficents(directrix)[0]
        B = self.coefficents(directrix)[1] - other.coefficents(directrix)[1]
        C = self.coefficents(directrix)[2] - other.coefficents(directrix)[2]

        discriminant = B**2 - 4*A*C
        out = []
        
        if A == 0:
            if B==0: # in this instance, we have either no intersections (return []), or infintitely many (return None)
                if C==0:
                    print("Infinitely many intersections: parabolae overlap on an interval.", file=sys.stderr)
                    return None
                
            else: # the parabolae are horizontal translations of one another, and have a single intersection
                out.append([-C/B, self.evaluate(-C/B, directrix)])

        else:
            if discriminant == 0: # double root
                intersection_x = -B / (2 * A)

                # check if intersection within interior of both arcs
                if intersection_x < self.right_bound and intersection_x < other.right_bound and intersection_x > self.left_bound and intersection_x > other.left_bound:
                    out.append([intersection_x, self.evaluate(intersection_x, directrix)])
            
            elif discriminant > 0: # distinct real roots
                intersection_x1 = (-B + math.sqrt(discriminant))/(2*A)
                intersection_x2 = (-B - math.sqrt(discriminant))/(2*A)
                

                if intersection_x1 < self.right_bound and intersection_x1 < other.right_bound and intersection_x1 > self.left_bound and intersection_x1 > other.left_bound:
                    out.append([intersection_x1, self.evaluate(intersection_x1, directrix)])

                if intersection_x2 < self.right_bound and intersection_x2 < other.right_bound and intersection_x2 > self.left_bound and intersection_x2 > other.left_bound:
                    out.append([intersection_x2, self.evaluate(intersection_x2, directrix)])
        
        return out


class BeachLine:
    def __init__(self):
        self.arc_tree = AVLTree.AVLTree(comparison_fn = lambda arc : arc.label)
        self.arcs = 0
    
    def add_arc(self, site, sweepline):
        # TODO: construct new arc, make room for it by clipping/removing other arcs, add it to the tree

        arc = self.arc_tree.min()

        while arc.value.right_bound < site[0]:
            arc = self.arc_tree.successor(arc)
        
        print(arc.value.label)

        arcs += 1 # or two, depending...