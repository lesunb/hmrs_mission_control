from random import Random

from deeco.core import BaseKnowledge
from deeco.core import Component
from deeco.core import Node
from deeco.core import Role
from deeco.core import process
from deeco.position import Position
from deeco.packets import TextPacket

# Role
class Rover(Role):
	def __init__(self):
		super().__init__()
		self.position = None
		self.goal = None


# Component
class Robot(Component):
	SPEED = 0.01
	COLORS = ["red", "blue", "green"]
	random = Random(0)

	@staticmethod
	def gen_position():
		return Position(Robot.random.uniform(0, 1), Robot.random.uniform(0, 1))

	# Knowledge definition
	class Knowledge(BaseKnowledge, Rover):
		def __init__(self):
			super().__init__()
			self.color = None

	# Component initialization
	def __init__(self, node: Node):
		super().__init__(node)

		# Initialize knowledge
		self.knowledge.position = node.positionProvider.get()
		self.knowledge.goal = self.gen_position()
		self.knowledge.color = self.random.choice(self.COLORS)

#		# Register network receive method
#		node.networkDevice.add_receiver(self.__receive_packet)

		node.position = self.knowledge.position

		print("Robot " + str(self.knowledge.id) + " created")

#	def __receive_packet(self, packet):
#		print((str(self.knowledge.time) + " ms: " + str(self.knowledge.id) + " Received packet: " + str(packet)))

	# Processes follow

	@process(period_ms=10)
	def update_time(self, node: Node):
		self.knowledge.time = node.runtime.scheduler.get_time_ms()

	@process(period_ms=1000)
	def status(self, node: Node):
		print(str(self.knowledge.time) + " ms: " + str(self.knowledge.id) + " at " + str(self.knowledge.position) + " goal " + str(
			self.knowledge.goal) + " dist: " + str(self.knowledge.position.dist_to(self.knowledge.goal)))

	@process(period_ms=100)
	def sense_position(self, node: Node):
		self.knowledge.position = node.positionProvider.get()

	@process(period_ms=1000)
	def set_goal(self, node: Node):
		if self.knowledge.position == self.knowledge.goal:
			self.knowledge.goal = self.gen_position()
			node.walker.set_target(self.knowledge.goal)
		node.walker.set_target(self.knowledge.goal)

#	@process(period_ms=2500)
#	def send_echo_packet(self, node: Node):
#		node.networkDevice.send(node.id, TextPacket("Echo packet payload from: " + str(self.knowledge.id)))
#		node.networkDevice.broadcast(TextPacket("Broadcast echo packet payload from: " + str(self.knowledge.id)))