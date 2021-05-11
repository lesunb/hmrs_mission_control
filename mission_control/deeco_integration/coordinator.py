from random import Random
from typing import List

from deeco.core import BaseKnowledge, Component, Role, Node
from deeco.core import process
from deeco.position import Position

from ..core import MissionContext, Worker
from ..manager.integration import MissionHandler, MissionUnnexpectedError
from ..manager.coalition_formation import CoalitionFormationProcess
from ..manager.supervision import SupervisionProcess


class MissionCoordinator(Role):
    def __init__(self):
        self.missions = None
        self.active_workers: List[Worker] = None


class Coordinator(Component, MissionHandler):
    COLORS = ["yellow", "pink"]
    random = Random(0)

    @staticmethod
    def gen_position():
        return Position(0, 0)

    # Knowledge definition
    class Knowledge(BaseKnowledge, MissionCoordinator):
        def __init__(self):
            super().__init__()


    # Component initialization
    def __init__(self, node: Node, required_skills = None,
            cf_process: CoalitionFormationProcess = None,
            supervision_proces: SupervisionProcess = None):
        
        super().__init__(node)
        self.cf_process = cf_process
        self.supervision_process = supervision_proces

        # Initialize knowledge

        print("Coordinator " + str(self.knowledge.id) + " created")

    @process(period_ms=10)
    def update_time(self, node: Node):
        self.knowledge.time = node.runtime.scheduler.get_time_ms()

    @process(period_ms=1000)
    def coalition_formation(self, node: Node):
        for mission_context in self.get_missions_with_pending_assignments():        
            workers = self.get_free_workers()
            self.cf_process.run(mission_context, workers, self)

    def get_missions_with_pending_assignments(self):
        for mission_context in self.knowledge.missions:
            print('some pending assignments')
            if self.has_pending_assignment(mission_context):
                yield mission_context
        
        for new_mission_context in self.handle_requests():
            yield new_mission_context

        return

    @staticmethod
    def has_pending_assignment(mission_context:MissionContext):
        return mission_context.status in [MissionContext.Status.NEW,
                            MissionContext.Status.PENDING_ASSIGNMENTS]

    def handle_requests(self):
        for request in self.node.requests_queue:
            mission_context = MissionContext(request.mission)
            print(f'coordinator {self.id} got has a new mission {mission_context}')
            self.knowledge.missions.append(mission_context)
            yield mission_context
        return

    def start_mission(self, mission_context):
        self.knowledge.missions.append(mission_context)
        print(f'mission started {mission_context}')
    
    def update_assigments(self, mission_context: MissionContext):
        print(f'received an update for {mission_context}')
    
    def no_coalition_available(self, mission_context: MissionContext):
        print(f'no coalition available for {mission_context}')
    
    # @process(period_ms=1000)
    def supervision(self, node):
        for active_mission in self.get_active_missions():
            task_updates = self.get_pending_updates(active_mission)
            assigned_workers = self.get_assigned_workers(active_mission)
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

    def get_free_workers(self):
        workers = self.knowledge.active_workers
        missions = self.knowledge.missions 
        assigned_workers = []
        
        for mission in missions:
            for local_mission in mission.local_missions:
                assigned_workers.append(local_mission.worker)
        
        return set(workers) - set(assigned_workers)

