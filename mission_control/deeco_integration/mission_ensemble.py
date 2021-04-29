from abc import abstractmethod

from deeco.core import EnsembleDefinition, BaseKnowledge
from deeco.core import Role
from deeco.position import Position
from .robot import Robot
from .coordinator import Coordinator


# Role
class Group(Role):
	def __init__(self):
		super().__init__()
		self.center = None
		self.members = []


class MissionEnsemble(EnsembleDefinition):
	class RobotGroupKnowledge(BaseKnowledge, Group):
		def __init__(self):
			super().__init__()

		def __str__(self):
			return self.__class__.__name__ + " centered at " + str(self.center) + " with component ids " + str(list(map(lambda x: x.id, self.members)))

	def fitness(self, a: Robot.Knowledge, b: Robot.Knowledge):
		if type(a) is not Coordinator.Knowledge or type(b) is not Robot.Knowledge:
			return 0
		else:
			for skill in a.required_skills:
				if skill in b.provided_skills:
					return 1
			return 0

	def membership(self, a: Robot, b: Robot):
		assert type(a) == Coordinator.Knowledge
		assert type(b) == Robot.Knowledge
		return True

	def knowledge(self, a: Robot.Knowledge, b: Robot.Knowledge):
		knowledge = self.RobotGroupKnowledge()
		knowledge.center = Position.average(a.position, b.position)
		knowledge.members = [a, b]

		return knowledge

	def __str__(self):
		return self.__class__.__name__
