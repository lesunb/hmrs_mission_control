
from deeco.core import BaseKnowledge, ComponentRole, Component, Node


class MissionClient(ComponentRole):
    def __init__(self):
        super().__init__()
        self.requests = []
        self.mission_status = []

# Component
class Client(Component):
	# Knowledge definition
	class Knowledge(BaseKnowledge, MissionClient):
		def __init__(self):
			super().__init__()

	# Component initialization
	def __init__(self, node: Node, provided_skills = []):
		super().__init__(node)
		node.register_handler(self.add_request)
		

		# Initialize knowledge

#		# Register network receive method
#		node.networkDevice.add_receiver(self.__receive_packet)

		print("User " + str(self.knowledge.id) + " created")

#	def __receive_packet(self, packet):
#		print((str(self.knowledge.time) + " ms: " + str(self.knowledge.id) + " Received packet: " + str(packet)))

	# Processes follow
	def add_request(self, request):
		self.knowledge.requests.append(request)
