
import SiteGenerator
from FortunesAlgorithm import FortunesAlgorithm

# sites = SiteGenerator.RandomSites(None)
# algo = FortunesAlgorithm(sites)

# if not algo.RunAlgorithm():
# 	print("disaster struck!")


from BeachLine import BeachLine
from BeachLine import Arc
from Point import Point

a = Arc(Point(-1,3))
b = Arc(Point(2,2))
c = Arc(Point(-4,1))

tree = BeachLine(a)
tree.AddArc(b)
tree.AddArc(c)

print(tree.arc_count)
tree.PlotTree("mytree")
tree.PlotEnvelope(0, -10, 10, 1000, save=True, sites=True)
