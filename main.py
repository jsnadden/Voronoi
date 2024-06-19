import random
import time
from matplotlib import pyplot as plt
from matplotlib import scale

import SiteGenerator
from BeachLine import Point
from FortunesAlgorithm import FortunesAlgorithm

sites = SiteGenerator.RandomSites()
algo = FortunesAlgorithm(sites)

if not algo.RunAlgorithm():
	print("disaster struck!")

