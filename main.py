import random
import time
from matplotlib import pyplot as plt
from matplotlib import scale

import AVLTree
import PriorityQueue
import BeachLine

start_time = time.time()


b = BeachLine.BeachLine()
b.add_arc([0, 1/2], 0)
b.add_arc([4,-1/2], 0)




# print("==============================================")
# print(f"RAN FOR {time.time()-start_time} SECONDS")
# print("==============================================")