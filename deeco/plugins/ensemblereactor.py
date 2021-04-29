from deeco.runnable import NodePlugin
from deeco.core import EnsembleDefinition
from deeco.core import EnsembleInstance
from deeco.core import Node
from deeco.packets import Packet
from deeco.packets import KnowledgePacket
from deeco.packets import PacketType
from deeco.packets import DemandPacket


class DemandRecord:
	def __init__(self, component_id: int, fitness_difference: float, target_ensemble: EnsembleInstance):
		self.component_id = component_id
		self.fitness_difference = fitness_difference
		self.target_ensemble = target_ensemble

	def __hash__(self):
		return self.component_id.__hash__()


class AssignmentRecord:
	def __init__(self, node_id: int, fitness_gain: float):
		self.node_id = node_id
		self.fitness_gain = fitness_gain


class EnsembleReactor(NodePlugin):
	def __init__(self, node: Node, ensemble_definitions: []):
		super().__init__(node)
		self.definitions = ensemble_definitions
		self.node.networkDevice.add_receiver(self.receive)
		self.instances = []
		self.demands = {}

	def run(self, scheduler):
		# Add assignment records to knowledge
		for component in self.node.get_components():
			component.knowledge.assignment = AssignmentRecord(None, 0)

		scheduler.set_periodic_timer(self.react, period_ms=1000)

	def react(self, time_ms):
		#print("Reactor invoked, sending demands and assignments")

		for component_id, demand in self.demands.items():
			packet = DemandPacket(time_ms, demand.component_id, self.node.id, demand.fitness_difference)
			self.node.networkDevice.broadcast(packet)

		# TODO: Maintain ensembles check timestamps

		self.run_ensembles(time_ms)

		for instance in self.instances:
			print("### Node " + str(self.node.id) + " ensemble instance " + str(instance) + " with components: " + str(list(map(lambda x: x.id, instance.memberKnowledge))))

	def run_ensembles(self, time_ms: int):
		for instance in self.instances:
			if instance.membership():
				knowledge = instance.knowledge()
				knowledge.assignment = AssignmentRecord(None, 0)
				print("### Active instance: " + str(instance) + " : " + str(knowledge))
				packet = KnowledgePacket(instance.id(), knowledge, time_ms)
				self.node.networkDevice.broadcast(packet)

	def receive(self, packet: Packet):
		if packet.type == PacketType.KNOWLEDGE and isinstance(packet, KnowledgePacket):
			self.process_knowledge(packet)

		if packet.type == PacketType.DEMAND and isinstance(packet, DemandPacket):
			self.process_demand(packet)

	def process_knowledge(self, knowledge_packet: KnowledgePacket):
#		print("Reactor processing knowledge packet")

		if knowledge_packet.knowledge.assignment.node_id is self.node.id:
			# Already assigned to us, lets process demands
			self.process_assignment(knowledge_packet)
		else:
			# Not assigned to us, lets create demand
			self.create_demand(knowledge_packet)

	@staticmethod
	def evaluate_assignment(current_impact: float, current_node_id: int, new_impact: float, new_node_id: int):
		fitness_upgrade = new_impact > current_impact
		fitness_clash = new_impact == current_impact
		id_superior = current_node_id is None or new_node_id < current_node_id
		return fitness_upgrade or (fitness_clash and id_superior)

	def create_demand(self, knowledge_packet: KnowledgePacket):
		proposals = []

		# Try to demand ensemble upgrade
		for instance in self.instances:
			impact = instance.add_impact(knowledge_packet.knowledge)
			if self.evaluate_assignment(
					knowledge_packet.knowledge.assignment.fitness_gain,
					knowledge_packet.knowledge.assignment.node_id,
					impact,
					self.node.id):
				print("Demanding to upgrade ensemble instance, add impact: " + str(impact))
				demand = DemandRecord(knowledge_packet.id, impact, instance)
				proposals.append(demand)

		# Build new ensemble instance if possible
		for definition in self.definitions:
			instance = EnsembleInstance(definition)
			impact = instance.add_impact(knowledge_packet.knowledge)
			if self.evaluate_assignment(
					knowledge_packet.knowledge.assignment.fitness_gain,
					knowledge_packet.knowledge.assignment.node_id,
					impact,
					self.node.id):
				print("Demanding to create new ensemble instance, add impact: " + str(impact))
				demand = DemandRecord(knowledge_packet.id, impact, definition)
				proposals.append(demand)

		# Create demand for existing local ensemble instance
		for instance in filter(lambda x: x.contains(knowledge_packet.id), self.instances):
			demand = DemandRecord(knowledge_packet.id, knowledge_packet.knowledge.assignment.fitness_gain, instance)
			proposals.append(demand)

		# Pick best demand
		demand = None
		for proposal in proposals:
			if demand is None or proposal.fitness_difference > demand.fitness_difference:
				demand = proposal

		# Set best demand
		if knowledge_packet.id in self.demands:
			del self.demands[knowledge_packet.id]
		if demand is not None:
			self.demands[knowledge_packet.id] = demand

	def process_demand(self, demand: DemandPacket):
		if demand.component_id not in map(lambda x: x.id, self.node.get_components()):
			return

		#print("Reactor processing demand packet")

		assignment = self.node.get_component_by_id(demand.component_id).knowledge.assignment

		# Assign free component
		if assignment.node_id is None:
			self.assign(demand.component_id, demand.node_id, demand.fitness_difference)
			return

		# Re-assign component
		if self.evaluate_assignment(demand.fitness_difference, demand.node_id, assignment.fitness_gain, assignment.node_id):
			self.assign(demand.component_id, demand.node_id, demand.fitness_difference)
			return

	def assign(self, component_id: int, node_id: int, fitness_difference: float):
		# TODO: One more vote for keeping components in a dictionary
		for component in self.node.get_components():
			if component.id == component_id:
				component.knowledge.assignment = AssignmentRecord(node_id, fitness_difference)

	def process_assignment(self, knowledge_packet: KnowledgePacket):
		assignment = knowledge_packet.knowledge.assignment

		if assignment.node_id != self.node.id:
			return

		# Already in ensemble, update
		# TODO: Moves between ensembles on the same node
		for instance in self.instances:
			if instance.contains(knowledge_packet.id):
				# TODO: Record assignment timestamps
				return

		# We received assignment for non existent demand
		if knowledge_packet.id not in self.demands:
			return

		# Process according to demand
		demand = self.demands[knowledge_packet.id]
		if isinstance(demand.target_ensemble, EnsembleDefinition):
			print("Reactor: Node " + str(self.node.id) + " Creating new ensemble of type " + str(demand.target_ensemble) + " with component " + str(knowledge_packet.id))
			instance = demand.target_ensemble.instantiate()
			instance.add(knowledge_packet.knowledge)

			self.instances.append(instance)

		elif isinstance(demand.target_ensemble, EnsembleInstance):
			print("Reactor: Node " + str(self.node.id) + " Adding to ensemble " + str(demand.target_ensemble) + " component " + str(knowledge_packet.id))
			demand.target_ensemble.add(knowledge_packet.knowledge)
		else:
			raise Exception("demand.target_ensemble should contain definition or instance", demand.target_ensemble)
