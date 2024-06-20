import Events
import PriorityQueue
import BeachLine
import Graphs

# TODO: think carefully about chain of "imports" i.e. which structures know about each other
class FortunesAlgorithm:
	def __init__(self, sites):
		sites.sort(key=lambda point : point.y)
		events = [Events.SiteEvent(site) for site in sites]
		starting_event = events.pop()

		self.Q = PriorityQueue.PriorityQueue(events)
		self.B = BeachLine.BeachLine(BeachLine.Arc(starting_event.site))
		self.G = Graphs.VoronoiDiagram() # TODO whatever args this guy needs

	def RunAlgorithm(self):
		success = False

		while not self.Q.is_empty():
			event = self.Q.pop()

			if isinstance(event, Events.SiteEvent):
				success = self.HandleSiteEvent()
			elif isinstance(event, Events.CircleEvent):
				success = self.HandleCircleEvent()
		
		return success


	def HandleSiteEvent(self):
		# TODO
		return True

	def HandleCircleEvent(self):
		# TODO
		return True