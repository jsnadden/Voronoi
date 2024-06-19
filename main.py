import random
import time
from matplotlib import pyplot as plt
from matplotlib import scale

import AVLTree
import PriorityQueue
import BeachLine

start_time = time.time()

arc = BeachLine.Arc([0,0])
tree = BeachLine.FortuneTree(arc)

for i in range(1,11):
	newarc = BeachLine.Arc([i,0])
	tree.InsertAfter(arc, newarc)
	tree.PlotTree(filename=f"adding arc {i}")
	arc = newarc

arc = tree.Min()

while arc.next != None:
	next_arc = arc.next
	tree.Delete(arc)
	tree.PlotTree(filename=f"deleted arc {arc.focus[0]}")
	arc = next_arc


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
