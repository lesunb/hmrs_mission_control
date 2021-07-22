from deeco.sim import Scheduler
from deeco.core import Node, NodePlugin
from deeco.packets import KnowledgePacket


class KnowledgePublisher(NodePlugin):
	DEFAULT_PUBLISHING_PERIOD_MS = 1000

	def __init__(self, node: Node, publishing_period_ms = DEFAULT_PUBLISHING_PERIOD_MS):
		super().__init__(node)
		self.publishing_period_ms = publishing_period_ms

	def run(self, scheduler: Scheduler):
		scheduler.set_periodic_timer(self.publish, period_ms=self.publishing_period_ms)

	def publish(self, time_ms):
		# print("Publishing knowledge on " + str(self.node.id))

		for component in self.node.components:
			self.node.networkDevice.broadcast(KnowledgePacket(component.uuid, component.knowledge, time_ms, from_node_id=self.node.id))
