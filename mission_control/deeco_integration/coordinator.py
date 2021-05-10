from random import Random
from queue import SimpleQueue

from deeco.core import BaseKnowledge
from deeco.core import Component
from deeco.core import Node
from deeco.core import Role
from deeco.core import process
from deeco.position import Position
from deeco.packets import TextPacket

from ..core import MissionContext
from ..manager.integration import MissionHandler

# Roles
class RequestsHandler(Role):
    __curr_requests_ids = None

    def __init__(self):
        super().__init__()
        self.requests = []
        self.mission_status = []
        

    def merge(self, o):
        n_ids = map(lambda n: n.id, o.requests)
        if self.curr_ids is None:
            self.__curr_requests_ids = map(lambda n: n.id, self.requests)
        
        diff = set(n_ids) - set(curr_ids)
        if diff is None:
            return 
        __curr_requests_ids = None
        to_add = filter(lambda n: __curr_requests_ids.contains(n.id), o.requests)
        self.requests.extends(to_add)


class MissionCoordinator(Role):
    def __init__(self):
        self.global_mission = None



# Components
class MissionsServer(Component, RequestsHandler):

   # Knowledge definition
    class Knowledge(RequestsHandler, BaseKnowledge):
        def __init__(self):
            super().__init__()


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
    def __init__(self, node: Node, required_skills = []):
        super().__init__(node)
        

        # Initialize knowledge

        # self.cf_process = node.get_cf_process(mission_handler=self)
        #self.supervision_process = node.get_supervision_process(mission_handler=self)

        print("Coordinator " + str(self.knowledge.id) + " created")

    @process(period_ms=10)
    def update_time(self, node: Node):
        self.knowledge.time = node.runtime.scheduler.get_time_ms()

    @process(period_ms=1000)
    def get_mission(self, node: Node):
        if self.knowledge.global_mission == None and not node.requests_queue.empty():
            request = node.requests_queue.get()
            print(f'coordinator {self.id} got a new mission {self.global_mission}')
            self.knowledge.global_mission = request
            self.local_missions = divide(request)

    @process(period_ms=1000)
    def status(self, node: Node):
        print(str(self.knowledge.time) + " ms: " + str(self.knowledge.id))


    # @process(period_ms=10)
    def handle_mission_requests(self, node):
        """ handle quests sequentially from a queue. 
        Non parallel in order to avoid conflict in the scheduling workers """
        # TODO guarantee single active 
        requests_without_plan = []
        for request in self.knowledge.pending_requests():
            if request.timmeout > self.current_time():
                self.handle_expired_request(request)
                continue
            
            mission_context = request.mission_context
            workers = self.get_available_workers()
            self.cf_process.run(mission_context, workers)
        
    # @process(period_ms=1000)
    def handle_mission_updates(self, node):
        for active_mission in self.get_active_missions():
            task_updates = self.get_pending_updates(active_mission)
            assigned_workers = self.get_assigned_workers(active_mission)
            supervision_process.run(active_mission, updates)
    
    def on_mission_start(mission_context: MissionContext):
        self.active_missions.add(mission_context)
        self.node.log_mission_start(mission_context)
        self.assign_coalition_to_mission(mission_context)

    def on_mission_end(mission_context: MissionContext):
        self.active_missions.remove(mission_context)
        self.node.log_mission_end(mission_context)

    def assign_coalition_to_mission(mission_context: MissionContext):
        for assignment in mission_context:
            self.knowledge.workers_schedule_table[worker_id]= ('assigned')
            mission_context.assignments = None

    def update_assigment(self, assignment_update):
        """ free or fail update """
        # TODO check the assignment to update
        self.knowledge.workers_schedule_table[assignment_update.target].status = assignment_update.satus

    def report_progress(self, acive_mission):
        def log():
            pass
        return log
