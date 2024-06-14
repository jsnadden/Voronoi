import random
import time
from matplotlib import pyplot as plt
from matplotlib import scale

import AVLTree
import PriorityQueue

start_time = time.time()

trees = 3
size = 20

for i in range(trees):
    my_values = range(size)
    my_values = random.sample(my_values, k=size)

    a = AVLTree.AVLTree(values=my_values)

    a.generate_plot(show=True)

    #print("==============================================")
    # print(f"TREE {i}:")
    # print("----------------------------------------------")
    # a.print()

#print("==============================================")

