from typing import List

from deeco import (BaseKnowledge, Component, ComponentRole, Node, Position,
                   process)

from ..data_model.restrictions import POI, Battery, LocalMission


# Roles
class Worker(ComponentRole):
	def __init__(self):
		super().__init__()
		self.name = None
		self.skills = None
		self.local_mission: LocalMission = None
		self.location: POI = None
		self.battery: Battery = None
		self.battery_discharge_rate: float = None
		self.avg_speed: float = None

# Component
class Robot(Component):
	@staticmethod
	def gen_position():
		return Position(Robot.random.uniform(0, 1), Robot.random.uniform(0, 1))

	# Knowledge definition
	class Knowledge(BaseKnowledge, Worker):
		pass

	# Component initialization
	def __init__(self,node: Node = None,
				name: str = None,
				skills: List[str] = None,
				location: POI = None,
				battery: Battery = None,
				battery_discharge_rate = None,
				local_mission: LocalMission=None,
				avg_speed = 0, 
				id = 0):

		super().__init__(node)

		# Initialize knowledge
		self.name = name
		self.knowledge.name = name
		self.knowledge.skills = skills
		self.knowledge.location = location
		self.knowledge.battery = battery
		self.knowledge.battery_discharge_rate = battery_discharge_rate
		self.knowledge.local_mission = local_mission
		self.knowledge.avg_speed = avg_speed

		print(f"Robot {self.name} created")
	
	# Processes follow
	@process(period_ms=10)
	def update_time(self, node: Node):
		self.knowledge.time = node.runtime.scheduler.get_time_ms()
		
	@process(period_ms=1000)
	def sequencing(self, node: Node):
		if self.knowledge.local_mission:
			print(self.knowledge.local_mission)


	@process(period_ms=10)
	def sense_task_execution_status(self, node: Node):
		pass
		# TODO 

	# @process(period_ms=100)
	# def sense_position(self, node: Node):
	# 	self.knowledge.position = node.positionProvider.get()
