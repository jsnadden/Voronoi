import math
import copy
import time
from matplotlib import pyplot as plt

from FortuneTree import Node, FortuneTree
from Point import Point




# encodes, and provides an interface for, parabolics arcs with fixed focus, and a variable (horizontal) directrix
class Arc(Node):
	def __init__(self, focus):
		super().__init__()

		# geometric data
		self.focus = focus
		self.left_halfedge = None
		self.right_halfedge = None

		# auxilliary data
		self.label = 0

	# produce a list of the coefficients for the associated quadratic function, given the current directrix y-value
	def Coefficents(self, directrix):
		a = 1 / (2 * (self.focus.y - directrix))
		b = -2 * a * self.focus.x
		c = a * (self.focus.x**2 + self.focus.y**2 - directrix**2)
		return [a,b,c]

	# evaluate value of the quadratic at x, given the current directrix y-value
	def Evaluate(self, x, directrix):
		return ((x - self.focus.x)**2 / (2 * (self.focus.y - directrix))) + ((self.focus.y + directrix) / 2)

	# returns a list of all (real, internal) intersection points (in list form [x,y]) between two parabolic arcs
	def Breakpoint(self, other, directrix):
		# get the coefficients and form a difference of quadratic functions
		A = self.Coefficents(directrix)[0] - other.Coefficents(directrix)[0]
		B = self.Coefficents(directrix)[1] - other.Coefficents(directrix)[1]
		C = self.Coefficents(directrix)[2] - other.Coefficents(directrix)[2]
		discriminant = B**2 - 4*A*C
		x = None

		if A == 0:
			if B == 0: # the parabolae are vertical translations of one another, or are equal
				assert C, "Intersected a parabola with itself"
				x = None

			else: # the parabolae are horizontal translations of one another, and have a single intersection
				x = -C/B

		else:
			if discriminant == 0: # double root
				x = -B / (2 * A)

			elif discriminant > 0: # distinct real roots, the correct one will be the + option
				x = (-B + math.sqrt(discriminant))/(2*A)

		if x == None:
			return None

		return x


# augments the above tree structure with application-specific methods
class BeachLine(FortuneTree):
	def __init__(self, root):
		super().__init__(root)
		
		if root == None:
			self.arc_count = 0
		else:
			self.arc_count = 1
			root.label = 1

# find the arc on the beachfront immediately above a given point in the plane
	def GetArcAbove(self, x, sweepline):
		arc = self.root;
		found = False;

		while not found:
			left = -math.inf
			right = math.inf

			if arc.previous != None:
				left = arc.previous.Breakpoint(arc, sweepline)

			if arc.next != None:
				right = arc.Breakpoint(arc.next, sweepline)

			if x < left:
				arc = arc.left
			elif x >= right:
				arc = arc.right
			else:
				found = True
		
		return arc

	def AddArc(self, arc):

		left = self.GetArcAbove(arc.focus.x, arc.focus.y)
		right = copy.deepcopy(left)

		# TODO: initialise each arc's voronoi graph data

		self.InsertAfter(left, arc)
		arc.label = self.arc_count + 1
		self.arc_count +=1

		self.InsertAfter(arc, right)
		right.label = self.arc_count + 1
		self.arc_count +=1

	def ListBreakpoints(self, sweepline):
		arc = self.Min()
		points = []

		while arc.next != None:
			x = arc.Breakpoint(arc.next, sweepline)
			y = arc.Evaluate(x, sweepline)
			points.append(Point(x,y))
			arc = arc.next

		return points

	def PlotEnvelope(self, sweepline, left_limit, right_limit, samples=100, show=True, save=False, sites=False):
		
		X, Y = [], []

		for i in range(samples):
			xi = left_limit + i * (right_limit - left_limit) / samples
			arc = self.GetArcAbove(xi, sweepline)
			yi = arc.Evaluate(xi, sweepline)
			X.append(xi)
			Y.append(yi)
		
		plt.plot(X, Y)

		if sites:
			arcs = self.ListNodes()
			siteX = [arc.focus.x for arc in arcs]
			siteY = [arc.focus.y for arc in arcs]
			plt.scatter(list(siteX), list(siteY))
		
		if save: plt.savefig("pyplot_outputs/envelope.png")
		if show: plt.show()
		plt.clf()

		return

	def FormatArcLabel(self, arc):
		node_label = f"Arc {arc.label} ({arc.focus.x},{arc.focus.y})"
		return node_label
	
	def PlotTree(self, filename=time.time()):
		super().PlotTree(f"beachline_{filename}", self.FormatArcLabel)

	

	
