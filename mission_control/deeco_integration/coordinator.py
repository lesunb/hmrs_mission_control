from random import Random

from deeco.core import BaseKnowledge
from deeco.core import Component
from deeco.core import Node
from deeco.core import Role
from deeco.core import process
from deeco.position import Position
from deeco.packets import TextPacket

from .request import Request

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

class MissionContext:
    def __init__(self, request):
        self.request = request
        self.mision_status = 'NOT_STARTED'
        self.missions_local_plans = map()



# Component
class Coordinator(Component):
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
            self.required_skills

    # Component initialization
    def __init__(self, node: Node, required_skills = []):
        super().__init__(node)
        

        # Initialize knowledge
        self.knowledge.required_skills = required_skills
        self.knowledge.position = node.positionProvider.get()
        self.knowledge.goal = self.gen_position()
        self.knowledge.color = self.random.choice(self.COLORS)

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

#	@process(period_ms=2500)
#	def send_echo_packet(self, node: Node):
#		node.networkDevice.send(node.id, TextPacket("Echo packet payload from: " + str(self.knowledge.id)))
#		node.networkDevice.broadcast(TextPacket("Broadcast echo packet payload from: " + str(self.knowledge.id)))