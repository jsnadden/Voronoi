import math
from matplotlib import pyplot as plt

import FortuneTree


# 2d point, pretty self-explanatory
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y


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
class BeachLine(FortuneTree.FortuneTree):
	def __init__(self, root):
		super().__init__(self, root)

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

	def ListBreakpoints(self, sweepline):
		arc = self.Min()
		points = []

		while arc.next != None:
			x = arc.Breakpoint(arc.next, sweepline)
			y = arc.Evaluate(x, sweepline)
			points.append(Point(x,y))
			arc = arc.next

		return points

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
















