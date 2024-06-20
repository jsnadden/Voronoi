import time
import graphviz

DEFAULT = object()

class Node:
	def __init__(self, data=None):
		self.data = data
		self.parent = None
		self.left = None
		self.right = None
		self.previous = None
		self.next = None
		self.height = 0

# basically a combination of an AVL tree and a doubly-linked list
class FortuneTree:
	def __init__(self, root):
		self.root = root

	def GetHeight(self, node=DEFAULT):

		if node == DEFAULT:
			node = self.root

		if node == None:
			return -1

		return node.height

	def GetBalance(self, node):

		return self.GetHeight(node.left) - self.GetHeight(node.right)

	def RecalculateHeight(self, node, recurse=False):
		if node == None:
			return -1

		if recurse:
			return 1 + max(self.RecalculateHeight(node.left, True), self.RecalculateHeight(node.right, True))

		else:
			return 1 + max(self.GetHeight(node.left), self.GetHeight(node.right))

	def RotateRight(self, node):

		x = node.left
		y = x.right

		# do the rotation
		x.right = node
		x.parent = node.parent
		node.parent = x
		node.left = y
		if y != None:
			y.parent = node

		# recalculate heights
		node.height = self.RecalculateHeight(node)
		x.height = self.RecalculateHeight(x)

		return x

	def RotateLeft(self, node):

		x = node.right
		y = x.left

		# do the rotation
		x.left = node
		x.parent = node.parent
		node.parent = x
		node.right = y
		if y != None:
			y.parent = node

		# recalculate heights
		node.height = self.RecalculateHeight(node)
		x.height = self.RecalculateHeight(x)

		return x

	def Rebalance(self, node, balance):

		root = (node == self.root)

		if balance > 1:
			# left-heavy
			x = node.left

			if self.GetBalance(x) < 0:
				# do left-right rotation
				node.left = self.RotateLeft(x)
				node = self.RotateRight(node)
			else:
				# just do right rotation
				node = self.RotateRight(node)

		if balance < -1:
			# right-heavy
			x = node.right

			if self.GetBalance(x) > 0:
				# do right-left rotation
				node.right = self.RotateRight(x)
				node = self.RotateLeft(node)
			else:
				# do left rotation
				node = self.RotateLeft(node)

		if root:
			self.root = node

		return node

	def FixTree(self, node = DEFAULT):

		if node == DEFAULT:
			node = self.root

		if node == None:
			return

		node.left = self.FixTree(node.left)
		node.right = self.FixTree(node.right)

		balance = self.GetBalance(node)

		while abs(balance) > 1:
			node = self.Rebalance(node, balance)
			balance = self.GetBalance(node)

		node.height = self.RecalculateHeight(node)

		return node

	def Min(self, subtree=DEFAULT):

		if subtree == DEFAULT:
			subtree = self.root

		node = subtree

		while node.left != None:
			node = node.left

		return node

	def Max(self, subtree=DEFAULT):

		if subtree == DEFAULT:
			subtree = self.root

		node = subtree

		while node.right != None:
			node = node.right

		return node

	def Successor(self, node):

		if node.right != None:
			return self.Min(node.right)

		successor = node

		while successor.parent != None:
			if successor == successor.parent.left:
				return successor.parent
			successor = successor.parent

		return None

	def Predecessor(self, node):

		if node.left != None:
			return self.Max(node.left)

		predecessor = node

		while predecessor.parent != None:
			if predecessor == predecessor.parent.right:
				return predecessor.parent
			predecessor = predecessor.parent

		return None

	def InsertBefore(self, node, newnode):

		if node.left == None:
			node.left = newnode
			newnode.parent = node

		else:
			pred = self.Predecessor(node)
			pred.right = newnode
			newnode.parent = pred

		self.root = self.FixTree()

		newnode.previous = node.previous
		newnode.next = node

		if newnode.previous != None:
			newnode.previous.next = newnode

		node.previous = newnode

		return

	def InsertAfter(self, node, newnode):

		if node.right == None:
			node.right = newnode
			newnode.parent = node

		else:
			succ = self.Successor(node)
			succ.left = newnode
			newnode.parent = succ

		self.root = self.FixTree()

		newnode.next = node.next
		newnode.previous = node

		if newnode.next != None:
			newnode.next.previous = newnode

		node.next = newnode

		return

	def Replace(self, node, replacement):

		if node.parent == None:
			self.root = replacement
		elif node == node.parent.left:
			node.parent.left = replacement
		else:
			node.parent.right = replacement

		if replacement != None:
			replacement.parent = node.parent

		return

	def Delete(self, node):

		if node.left == None:
			replacement = node.right
			self.Replace(node, node.right)

		elif node.right == None:
			replacement = node.left
			self.Replace(node, node.left)

		else: # node has two children, crown its successor!
			replacement = node.next

			if replacement.parent != node:
				self.Replace(replacement, replacement.right)
				replacement.right = node.right
				node.right.parent = replacement

			self.Replace(node, replacement)
			replacement.left = node.left
			node.left.parent = replacement

		if node.previous != None:
			node.previous.next = node.next
		if node.next != None:
			node.next.previous = node.previous

		node = None
		self.root = self.FixTree()

		return replacement

	def ListNodes(self, node=DEFAULT):

		if node == None:
			return []

		if node == DEFAULT:
			node = self.root

		nodes = []

		nodes = nodes + self.ListNodes(node.left)
		nodes.append(node)
		nodes = nodes + self.ListNodes(node.right)

		return nodes

	# generates a pdf file containing a plot of the tree, via the graphviz package
	def PlotTree(self, filename=DEFAULT, label_fn=lambda node : f"{node.data}"):

		if filename == DEFAULT:
			filename = f"fortune_tree_{time.time()}"

		nodes = self.ListNodes()
		dot = graphviz.Digraph()

		for node in nodes:
			dot.node(label_fn(node))

			if node.left != None:
				dot.edge(label_fn(node),
						 label_fn(node.left))

			if node.right != None:
				dot.edge(label_fn(node),
						 label_fn(node.right))

		file_path = f"graphviz_outputs/{filename}"
		dot.render(file_path, cleanup=True)
