from abc import abstractmethod

from deeco.core import EnsembleDefinition, BaseKnowledge
from deeco.core import Role, Group
from deeco.position import Position
from .robot import Robot, Worker
from .coordinator import Coordinator, MissionsServer, MissionCoordinator

from ..core import MissionContext

# Role
class MissionContextRole(Role, MissionContext):
	def __init__(self):
		super().__init__()

class MissionEnsemble(EnsembleDefinition):
	class MissionKnowledge(BaseKnowledge, MissionContextRole, Group):
		def __init__(self):
			super().__init__()

		def __str__(self):
			return self.__class__.__name__ + " with component ids " + str(list(map(lambda x: x.id, self.members)))

	def __init__(self):
		super().__init__(coordinator=MissionCoordinator, member=Worker)

	def fitness(self, coord: MissionCoordinator, member: Worker):
		if coord.global_mission is None:
			return 0
		else:
			return 1 

	def membership(self, coord: MissionCoordinator, member: Worker):
		assert isinstance(coord, MissionCoordinator)
		assert isinstance(member, Worker)
		return True	

	def knowledge_exchange(self, coord: MissionCoordinator, member: Worker):
		return coord, None

	def __str__(self):
		return self.__class__.__name__
