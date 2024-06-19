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

	def RecalculateHeight(self, arc, recurse=False):
		if arc == None:
			return -1

		if recurse:
			return 1 + max(self.RecalculateHeight(arc.left, True), self.RecalculateHeight(arc.right, True))

		else:
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
		arc.height = self.RecalculateHeight(arc)
		x.height = self.RecalculateHeight(x)

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
		arc.height = self.RecalculateHeight(arc)
		x.height = self.RecalculateHeight(x)

		return x

	def Rebalance(self, arc, balance):

		root = (arc == self.root)

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

		if root:
			self.root = arc

		return arc

	def FixTree(self, arc = DEFAULT):

		if arc == DEFAULT:
			arc = self.root

		if arc == None:
			return

		arc.left = self.FixTree(arc.left)
		arc.right = self.FixTree(arc.right)

		balance = self.GetBalance(arc)

		while abs(balance) > 1:
			arc = self.Rebalance(arc, balance)
			balance = self.GetBalance(arc)
		
		arc.height = self.RecalculateHeight(arc)

		return arc

	def Min(self, subtree=DEFAULT):

		if subtree == DEFAULT:
			subtree = self.root

		arc = subtree

		while arc.left != None:
			arc = arc.left

		return arc

	def Max(self, subtree=DEFAULT):

		if subtree == DEFAULT:
			subtree = self.root

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

		self.root = self.FixTree()

		newarc.previous = arc.previous
		newarc.next = arc

		if newarc.previous != None:
			newarc.previous.next = newarc

		arc.previous = newarc

		return

	def InsertAfter(self, arc, newarc):

		if arc.right == None:
			arc.right = newarc
			newarc.parent = arc

		else:
			succ = self.Successor(arc)
			succ.left = newarc
			newarc.parent = succ

		self.root = self.FixTree()

		newarc.next = arc.next
		newarc.previous = arc

		if newarc.next != None:
			newarc.next.previous = newarc

		arc.next = newarc

		return

	def Replace(self, arc, replacement):

		if arc.parent == None:
			self.root = replacement	
		elif arc == arc.parent.left:
			arc.parent.left = replacement	
		else:
			arc.parent.right = replacement
		
		if replacement != None:
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
		self.root = self.FixTree()

		return replacement

	def ListArcs(self, arc=DEFAULT):

		if arc == None:
			return []

		if arc == DEFAULT:
			arc = self.root

		out = []

		out = out + self.ListArcs(arc.left)
		out.append(arc)
		out = out + self.ListArcs(arc.right)

		return out

	# generates a pdf file containing a plot of the tree, via the graphviz package
	def PlotTree(self, filename=DEFAULT):
		
		if filename == DEFAULT:
			filename = time.time()

		arcs = self.ListArcs()
		dot = graphviz.Digraph()

		for arc in arcs:
			dot.node(f"{arc.focus[0]},{arc.focus[1]}")

			if arc.left != None:
				dot.edge(f"{arc.focus[0]},{arc.focus[1]}",
						 f"{arc.left.focus[0]},{arc.left.focus[1]}")

			if arc.right != None:
				dot.edge(f"{arc.focus[0]},{arc.focus[1]}",
						 f"{arc.right.focus[0]},{arc.right.focus[1]}")

		file_path = f"graphviz_outputs/fortune_tree_{filename}"
		dot.render(file_path, cleanup=True)


class BeachLine(FortuneTree):
	def __init__(self, site):
		FortuneTree.__init__(self, Arc(site))

	def GetBreakpoints(self, sweepline):
		breakpoints = []
		# TODO: figure this shit out
		return breakpoints













