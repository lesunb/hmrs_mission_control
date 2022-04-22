from deeco import EnsembleMember,EnsembleDefinition, BaseKnowledge, \
					ComponentRole, Group, \
					SetValue

from .robot import Worker
from .coordinator import MissionCoordinator
from ..data_model.restrictions import MissionContext, LocalMission

# Role
class MissionContextRole(ComponentRole, MissionContext):
	def __init__(self):
		super().__init__()

class MissionCoordinationEnsemble(EnsembleDefinition):
	class MissionKnowledge(BaseKnowledge, MissionContextRole, Group):
		def __init__(self):
			super().__init__()

		def __str__(self):
			return f'{self.__class__.__name__} with component ids ' + str(
			    list(map(lambda x: x.id, self.members)))

	def __init__(self):
		super().__init__(coordinator=MissionCoordinator, member=Worker)

	def fitness(self, coord: MissionCoordinator, member: Worker):
		return 1 if member else 0

	def membership(self, coord: MissionCoordinator, member: Worker):
		assert isinstance(coord, MissionCoordinator)
		assert isinstance(member, Worker)
		return True	

	def knowledge_exchange(self, coord: MissionCoordinator, member: EnsembleMember[Worker]):
		# member to coordinator
		coord.update_worker(member)
		worker = member.knowledge
		if worker.local_mission:
			mission_assigned = self.get_mission_member_is_assigned(coord, worker)
			# update coordinator about progress
			self.update_mission_progress(mission_assigned, worker.local_mission)

		# coordinator to member
		exchanges_coord_member = []
		assigned_local_mision, assigned_mission = self.get_local_mission_member_should_be_assigned(coord, member)		
		if worker.local_mission is not assigned_local_mision:
			# plan distribuition
			print(f'assigning mission {assigned_local_mision}')
			set_local_mission = SetValue('local_mission', assigned_local_mision)
			exchanges_coord_member.append(set_local_mission)
		return (coord, exchanges_coord_member)


	@staticmethod
	def get_mission_member_is_assigned(coord: MissionCoordinator, member: Worker):
		if not member.local_mission:
			return None
		else:
			for mission in coord.missions:
				if mission == member.local_mission.global_mission:
					return mission

	def update_mission_progress(self, mission_context:MissionContext, local_mission: LocalMission):
		print('update progress')
		pass
	
	@staticmethod
	def get_local_mission_member_should_be_assigned(coord: MissionCoordinator, member: EnsembleMember[Worker]):
		for mission in coord.missions:
			for local_mission in mission.local_missions:
				if member.same_uuid(local_mission.worker):
					return (local_mission, mission)
		return None, None

	@staticmethod
	def is_not_committed(member: Worker):
		return member.local_mission is None
	

	def __str__(self):
		return self.__class__.__name__
