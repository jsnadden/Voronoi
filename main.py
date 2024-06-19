import random
import time
from matplotlib import pyplot as plt
from matplotlib import scale

import AVLTree
import PriorityQueue
import BeachLine


a = BeachLine.Arc([-4,2])
b = BeachLine.Arc([0,1])
c = BeachLine.Arc([1,7])

print({f"a and b intersect at x={a.Breakpoint(b,0)}"})
print({f"b and c intersect at x={b.Breakpoint(c,0)}"})

tree = BeachLine.BeachLine(b)
tree.InsertAfter(b,c)
tree.InsertBefore(b,a)
tree.PlotEnvelope(0,-5,5,200)
	



# arc = tree.Min()

# tree.PlotTree(height=True)

# while arc.next != None:
# 	next_arc = arc.next.next
# 	tree.Delete(arc)
# 	arc = next_arc
# tree.Delete(arc)

# tree.PlotTree(height=True)

# trees = 1
# size = 200

# for i in range(trees):
#     print("==============================================")
#     print(f"TREE {i}:")
#     print("----------------------------------------------")
	
#     my_values = range(size)
#     my_values = random.sample(my_values, k=size)

#     a = AVLTree.AVLTree(values=my_values)
	
#     a.print()
#     a.generate_plot(show=(trees == 1))
#     ancestors = a.list_ancestors(a.search(50))
	
#     for node in ancestors:
#         print(node.value)

#     print("==============================================")
#     print(f"TREE {i} after deleting node 50:")
#     print("----------------------------------------------")
	
#     a.delete(50)
#     a.print()
#     a.generate_plot(show=(trees == 1))

# print("==============================================")
# print(f"RAN FOR {time.time()-start_time} SECONDS")
# print("==============================================")
