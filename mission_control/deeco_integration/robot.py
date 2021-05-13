from random import Random
from typing import List

from deeco.core import BaseKnowledge
from deeco.core import Component
from deeco.core import Node
from deeco.core import ComponentRole
from deeco.core import process
from deeco.position import Position

from mission_control.core import LocalMission, POI

# Roles
class Worker(ComponentRole):
	def __init__(self):
		super().__init__()
		self.skills = None
		self.local_mission: LocalMission = None
		self.location: POI = None
		self.battery_level: float = None
		self.battery_consumption_rate: float = None
		self.avg_speed: float = None

# Component
class Robot(Component):
	@staticmethod
	def gen_position():
		return Position(Robot.random.uniform(0, 1), Robot.random.uniform(0, 1))

	# Knowledge definition
	class Knowledge(Worker, BaseKnowledge):
		def __init__(self):
			super().__init__()

	# Component initialization
	def __init__(self, node: Node = None,
				skills: List[str] = None,
				location: POI = None,
				battery_level: float = None,
				battery_consumption_rate: float = None,
				local_mission: LocalMission=None,
				avg_speed = 0):

		super().__init__(node)

		# Initialize knowledge
		self.knowledge.node_id = node.id
		self.knowledge.skills = skills
		self.knowledge.location = location
		self.knowledge.battery_level = battery_level
		self.knowledge.battery_consumption_rate = battery_consumption_rate
		self.knowledge.local_mission = local_mission
		self.knowledge.avg_speed = avg_speed

		print("Robot " + str(self.knowledge.id) + " created")
	
	# Processes follow
	@process(period_ms=10)
	def update_time(self, node: Node):
		self.knowledge.time = node.runtime.scheduler.get_time_ms()

	@process(period_ms=10)
	def sense_task_execution_status(self, node: Node):
		pass
		# TODO 

	# @process(period_ms=100)
	# def sense_position(self, node: Node):
	# 	self.knowledge.position = node.positionProvider.get()
