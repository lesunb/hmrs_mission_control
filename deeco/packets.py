from deeco.core import UUID
from enum import Enum
from copy import deepcopy


class PacketType(Enum):
	RAW = 0
	KNOWLEDGE = 1
	TEXT = 2
	DEMAND = 3
	ASSIGNMENT = 4
	PATCH = 5

class Packet:
	def __init__(self):
		self.type = PacketType.RAW

	def __init__(self, type: PacketType, from_node_id:int = None):
		self.type, self.from_node_id = type, from_node_id

	def __str__(self):
		return self.__class__.__name__


class TimestampedPacket(Packet):
	def __init__(self, type: PacketType, time_ms: int, from_node_id = None):
		super().__init__(type, from_node_id)
		self.timestamp_ms = time_ms


class KnowledgePacket(TimestampedPacket):
	def __init__(self, component_uuid: UUID, knowledge, time_ms: int, from_node_id:int = None):
		super().__init__(PacketType.KNOWLEDGE, time_ms, from_node_id)
		self.component_uuid = component_uuid
		self.knowledge = deepcopy(knowledge)

class PatchPacket(TimestampedPacket):
	def __init__(self, component_uuid: UUID, patch, time_ms: int):
		super().__init__(PacketType.PATCH, time_ms)
		self.component_uuid = component_uuid
		self.patch = patch

class TextPacket(Packet):
	def __init__(self, text: str):
		super().__init__(PacketType.TEXT)
		self.text = text

	def __str__(self):
		return self.text


class DemandPacket(TimestampedPacket):
	def __init__(self, time_ms: int, component_uuid: UUID, node_id: int, fitness_difference: float):
		super().__init__(PacketType.DEMAND, time_ms)
		self.component_uuid = component_uuid
		self.node_id = node_id
		self.fitness_difference = fitness_difference

	def __str__(self):
		return "[node " + str(self.node_id) + " wants component " + str(self.component_uuid)\
			+ " to increase fitness by " + str(self.fitness_difference) + "]"


class AssignmentPacket(TimestampedPacket):
	def __init__(self, time_ms: int, component_uuid: UUID, node_id: int, fitness_difference: float):
		super().__init__(PacketType.ASSIGNMENT, time_ms)
		self.component_uuid = component_uuid
		self.node_id = node_id
		self.fitness_difference = fitness_difference

	def __str__(self):
		return "[node " + str(self.node_id) + " is assigned component " + str(self.component_uuid)\
			+ " for " + str(self.fitness_difference) + " fitness ]"
