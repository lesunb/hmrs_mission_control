from random import Random

from deeco.core import BaseKnowledge
from deeco.core import Component
from deeco.core import Node
from deeco.core import Role
from deeco.core import process
from deeco.position import Position
from deeco.packets import TextPacket

from .request import Request
from ..core import MissionContext
from ..manager.integration import MissionHandler

# Role
class Rover(Role):
    def __init__(self):
        super().__init__()
        self.position = None
        self.goal = None

class GlobalMissionManager(Role):
    def __init__(self):
        self.mission_contexts = {}
        self.required_skills = None
    
    def handle_request(self, request: Request):
       ctx = MissionContext(request)
       self.mission_contexts.put(request.id, request) 


# Component
class Coordinator(Component, MissionHandler):
    COLORS = ["yellow", "pink"]
    random = Random(0)

    @staticmethod
    def gen_position():
        return Position(0, 0)

    # Knowledge definition
    class Knowledge(BaseKnowledge, Rover, GlobalMissionManager):
        def __init__(self):
            super().__init__()
            self.color = None
            self.required_skills = []
            self.active_missions: [MissionContext] = []

    # Component initialization
    def __init__(self, node: Node, required_skills = []):
        super().__init__(node)
        

        # Initialize knowledge
        self.knowledge.required_skills = required_skills
        self.knowledge.position = node.positionProvider.get()
        self.knowledge.goal = self.gen_position()
        self.knowledge.color = self.random.choice(self.COLORS)

        self.cf_process = node.get_cf_process(mission_handler=self)
        self.supervision_process = node.get_supervision_process(mission_handler=self)
#		# Register network receive method
#		node.networkDevice.add_receiver(self.__receive_packet)

        node.position = self.knowledge.position

        print("Coordinator " + str(self.knowledge.id) + " created")

#	def __receive_packet(self, packet):
#		print((str(self.knowledge.time) + " ms: " + str(self.knowledge.id) + " Received packet: " + str(packet)))

    # Processes follow

    @process(period_ms=10)
    def update_time(self, node: Node):
        self.knowledge.time = node.runtime.scheduler.get_time_ms()

    @process(period_ms=1000)
    def status(self, node: Node):
        print(str(self.knowledge.time) + " ms: " + str(self.knowledge.id) + " at " + str(self.knowledge.position))

    @process(period_ms=100)
    def sense_position(self, node: Node):
        self.knowledge.position = node.positionProvider.get()

    @process(period_ms=1000)
    def set_goal(self, node: Node):
        if self.knowledge.position == self.knowledge.goal:
            self.knowledge.goal = self.gen_position()
            node.walker.set_target(self.knowledge.goal)
        node.walker.set_target(self.knowledge.goal)


    @process(period_ms=10)
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
        
    @process(period_ms=1000)
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

    def on_no_coalition_available(request: Request):
        pass

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

#	@process(period_ms=2500)
#	def send_echo_packet(self, node: Node):
#		node.networkDevice.send(node.id, TextPacket("Echo packet payload from: " + str(self.knowledge.id)))
#		node.networkDevice.broadcast(TextPacket("Broadcast echo packet payload from: " + str(self.knowledge.id)))