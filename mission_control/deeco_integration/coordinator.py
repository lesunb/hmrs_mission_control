from typing import List, Mapping

from deeco import BaseKnowledge, Component, ComponentRole, Node, UUID, EnsembleMember, process


from ..common_descriptors.navigation_sd import Move
from ..data_model import BatteryTimeConstantDischarge, LocalMission, MissionContext, Worker
from ..coordination import MissionHandler, MissionUnnexpectedError, CoalitionFormationProcess, SupervisionProcess


class MissionCoordinator(ComponentRole):
    def __init__(self):
        self.missions: List[MissionContext] = []
        self.active_workers: dict[UUID, Worker] = {}
    
    def update_worker(self, member: EnsembleMember[Worker]):
        self.active_workers[member.uuid] = member.knowledge


class Coordinator(Component, MissionHandler):
    # Knowledge definition
    class Knowledge(MissionCoordinator, BaseKnowledge):
        pass

    # Component initialization
    def __init__(self, node: Node= None, 
            required_skills = None,
            cf_process: CoalitionFormationProcess = None,
            supervision_proces: SupervisionProcess = None,
            name = None):
        super().__init__(node)
        self.cf_process = cf_process
        self.supervision_process = supervision_proces
        self.name = name

        # Initialize knowledge

        print(f"Coordinator {str(self.name)} created")

    @process(period_ms=10)
    def update_time(self, node: Node):
        self.knowledge.time = node.runtime.scheduler.get_time_ms()

    @process(period_ms=1000)
    def coalition_formation(self, node: Node):
        for mission_context in list(self.get_missions_with_pending_assignments()):
            workers = list(map(self.transform_worker, self.get_free_workers().items()))
            self.cf_process.run(mission_context, workers, self)

    def get_missions_with_pending_assignments(self):
        for mission_context in self.knowledge.missions:
            if self.has_pending_assignment(mission_context):
                yield mission_context
        
        for new_mission_context in self.handle_requests():
            yield new_mission_context

        return

    @staticmethod
    def has_pending_assignment(mission_context:MissionContext):
        return any(filter(lambda lm: lm.assignment_status == LocalMission.AssignmentStatus.NOT_ASSIGNED, mission_context.local_missions))

    def handle_requests(self):
        while self.node.requests_queue:
            request = self.node.requests_queue.pop(0)
            mission_context = MissionContext(request_id = request.id, global_plan=request.task)
            print(f'coordinator {self.uuid} got has a new mission {mission_context}')
            self.knowledge.missions.append(mission_context)
            yield mission_context
        return

    def start_mission(self, mission_context):
        print(f'mission started {mission_context}')
    
    def update_assigments(self, mission_context: MissionContext):
        print(f'received an update for {mission_context}')
    
    def no_coalition_availabel(self, mission_context: MissionContext):
        print(f'no coalition available for {mission_context}')
    
    # @process(period_ms=1000)
    def supervision(self, node):
        for active_mission in self.get_active_missions():
            task_updates = self.get_pending_updates(active_mission)
            # assigned_workers = self.get_assigned_workers(active_mission)
            self.supervision_process.run(active_mission, task_updates)

    def report_progress(self, acive_mission):
        def log():
            pass
        return log

    def end_mission(self, mission_context):
        print('mission ended')
        self.knowledge.missions.remove(mission_context)
        self.node.log_mission_end(mission_context)


    def completed_assignment():
        print(f'completed assignment')
    
    def notify_operator():
        print(f'op notification requested')

    def status_update_to_user():
        print(f'user update requested')

    def queue_request(self, request):
        print(f'request received')

    def handle_unnexpected_error(error: MissionUnnexpectedError):
        """ 
            Should handle internal error in the mission management process
        """
        print(error.message)
        print(error.orignal_error)

    @staticmethod
    def transform_worker(uuid_worker):
        uuid, worker_knowledge = uuid_worker
        worker = Worker(
            uuid=uuid,
            name=worker_knowledge.name,
            location=worker_knowledge.location,
            skills=worker_knowledge.skills,
            capabilities=[
                Move(avg_speed = worker_knowledge.avg_speed, u='m/s')
            ],
            resources = [
                BatteryTimeConstantDischarge(
                    battery = worker_knowledge.battery,
                    discharge_rate=worker_knowledge.battery_discharge_rate,
                    minimum_useful_level=0.05
                )
            ])
        return worker

    def get_free_workers(self) -> Mapping[UUID, Worker]:
        workers = dict(self.knowledge.active_workers)
        missions = self.knowledge.missions 
        
        for mission in missions:
            for local_mission in mission.local_missions:
                if local_mission.worker and local_mission.worker.uuid in workers:
                    workers.pop(local_mission.worker.uuid)
        
    
        return workers

