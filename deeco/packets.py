from enum import Enum
from copy import deepcopy


class PacketType(Enum):
	RAW = 0
	KNOWLEDGE = 1
	TEXT = 2
	DEMAND = 3
	ASSIGNMENT = 4


class Packet:
	def __init__(self):
		self.type = PacketType.RAW

	def __init__(self, type: PacketType):
		self.type = type

	def __str__(self):
		return self.__class__.__name__


class TimestampedPacket(Packet):
	def __init__(self, type: PacketType, time_ms: int):
		super().__init__(type)
		self.timestamp_ms = time_ms


class KnowledgePacket(TimestampedPacket):
	def __init__(self, id: int, knowledge, time_ms: int):
		super().__init__(PacketType.KNOWLEDGE, time_ms)
		self.id = id
		self.knowledge = deepcopy(knowledge)


class TextPacket(Packet):
	def __init__(self, text: str):
		super().__init__(PacketType.TEXT)
		self.text = text

	def __str__(self):
		return self.text


class DemandPacket(TimestampedPacket):
	def __init__(self, time_ms: int, component_id: int, node_id: int, fitness_difference: float):
		super().__init__(PacketType.DEMAND, time_ms)
		self.component_id = component_id
		self.node_id = node_id
		self.fitness_difference = fitness_difference

	def __str__(self):
		return "[node " + str(self.node_id) + " wants component " + str(self.component_id)\
			+ " to increase fitness by " + str(self.fitness_difference) + "]"


class AssignmentPacket(TimestampedPacket):
	def __init__(self, time_ms: int, component_id: int, node_id: int, fitness_difference: float):
		super().__init__(PacketType.ASSIGNMENT, time_ms)
		self.component_id = component_id
		self.node_id = node_id
		self.fitness_difference = fitness_difference

	def __str__(self):
		return "[node " + str(self.node_id) + " is assigned component " + str(self.component_id)\
			+ " for " + str(self.fitness_difference) + " fitness ]"
