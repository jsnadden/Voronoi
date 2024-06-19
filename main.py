import random
import time
from matplotlib import pyplot as plt
from matplotlib import scale

import AVLTree
import PriorityQueue
import BeachLine



max_arcs = 1000
sample_size = 1

ave_heights = []
ave_creation_times = []

for num_arcs in range(1,max_arcs, 10):
	start_time = time.time()
	out = 0
	for i in range(sample_size):
		arcs = []

		for x in range(num_arcs):
			arcs.append(BeachLine.Arc([x,0]))
		
		tree = BeachLine.FortuneTree(arcs)
		out += tree.GetHeight()
	
	ave_creation_times.append((time.time() - start_time) / sample_size)
	ave_heights.append(out / sample_size)

plt.plot(range(1,max_arcs, 10), ave_heights)
plt.xlabel('number of nodes')
plt.ylabel('tree height')
plt.savefig('fortune_tree_ave_heights.png')

plt.plot(range(1,max_arcs, 10), ave_creation_times)
plt.xlabel('number of nodes')
plt.ylabel('tree build time')
plt.savefig('fortune_tree_ave_build_times.png')


	



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
