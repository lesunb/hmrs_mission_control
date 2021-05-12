from typing import List
from deeco.runnable import NodePlugin
from deeco.core import EnsembleDefinition
from deeco.core import EnsembleInstance
from deeco.core import Node
from deeco.packets import Packet
from deeco.packets import KnowledgePacket, PatchPacket
from deeco.packets import PacketType
from deeco.packets import DemandPacket
from deeco.mapping import Mapping

class DemandRecord:
	def __init__(self, component_id: int, fitness_difference: float, target_ensemble: EnsembleInstance):
		self.component_id = component_id
		self.fitness_difference = fitness_difference
		self.target_ensemble = target_ensemble

	def __hash__(self):
		return self.component_id.__hash__()


class AssignmentRecord:
	def __init__(self, node_id: int, fitness_gain: float, last_update = None):
		self.node_id = node_id
		self.fitness_gain = fitness_gain
		self.last_update = last_update


class EnsembleReactor(NodePlugin):
	def __init__(self, node: Node, ensemble_definitions: List[EnsembleDefinition]):
		super().__init__(node)
		self.node.networkDevice.add_receiver(self.receive)
		
		self.definitions = ensemble_definitions
		self.instances: List[EnsembleInstance] = []
		self.demands = {}

		self.membership = []

	def run(self, scheduler):
		# Add assignment records to knowledge
		for component in self.node.get_components():
			component.knowledge.assignment = AssignmentRecord(None, 0)

		scheduler.set_periodic_timer(self.react, period_ms=1000)
		self.initial_instances()

	def get_coordinator(self, definition):
		for component in self.node.get_components():
			if isinstance(component.knowledge, definition.coordinator):
				return component
		return None

	def initial_instances(self):
		""" create instances for roles that are coordinators in definitions the node knows """
		for component in self.node.get_components():
			for definition in self.definitions:
				if isinstance(component.knowledge, definition.coordinator):
					instance = definition.instantiate(component)
					self.assign(component.id, self.node.id, 0)
					self.instances.append(instance)

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
		# advertise existing ensembles? 
		# TODO suspend ensemble advertisement
		#
		for instance in self.instances:
			if instance.membership():
				print("### Active instance: " + str(instance))
				member_mappings = instance.knowledge_exchange()
				for (node_id, component_id, patch) in member_mappings:
					packet = PatchPacket(node_id, patch, time_ms)
					self.node.networkDevice.send(node_id, packet)

	def receive(self, packet: Packet):
		if packet.type == PacketType.PATCH and isinstance(packet, PatchPacket):
			self.process_patch(packet)

		elif packet.type == PacketType.KNOWLEDGE and isinstance(packet, KnowledgePacket):
			self.process_knowledge(packet)

		elif packet.type == PacketType.DEMAND and isinstance(packet, DemandPacket):
			self.process_demand(packet)
		else:
			print(f'no identified {packet}')


	def process_patch(self, patch_packet: PatchPacket):
		id = patch_packet.id
		comp = self.node.get_component_by_id(id)
		comp.knowledge.assignment.last_update = patch_packet.timestamp_ms
		if patch_packet.patch is not None:
			Mapping.apply_all(patch_packet.patch, comp.knowledge)
		print(comp)


	def process_knowledge(self, knowledge_packet: KnowledgePacket):
#		print("Reactor processing knowledge packet")
		print(f'{self.node.id} recieved a package of type {knowledge_packet.knowledge.__class__}')
		if not hasattr(knowledge_packet.knowledge, 'assignment'):
			return 
		
		if knowledge_packet.knowledge.assignment.node_id is self.node.id:
			# Already assigned to us, lets process demands
			self.process_assignment(knowledge_packet)
		elif self.is_update_from_ensemble(knowledge_packet.knowledge):
			# update components with knowledge from ensembles		
			self.merge_knwoledge_from_ensemble(knowledge_packet.knowledge)
		else:
			# candidate advertising himself / ensemble publishing knowledge
			# Not assigned to us, lets create demand
			self.create_demand(knowledge_packet)

	def is_update_from_ensemble(self, knowledge_packet: KnowledgePacket):
		if not hasattr(knowledge_packet, 'members') or \
			not isinstance(knowledge_packet.members, list):
			return False
		else:
			for member in knowledge_packet.members:
				component = self.node.get_component_by_id(member.id)
				if component is not None:
					return True
		return False
	
	def merge_knwoledge_from_ensemble(self, knowledge_packet: KnowledgePacket):
		for member in knowledge_packet.members:
			component = self.node.get_component_by_id(member.id)
			if component is not None:
				component.knowledge.merge(member)

	@staticmethod
	def evaluate_assignment(current_impact: float, current_node_id: int, new_impact: float, new_node_id: int):
		fitness_upgrade = new_impact > current_impact
		fitness_clash = new_impact == current_impact
		id_superior = current_node_id is None or new_node_id < current_node_id
		return fitness_upgrade or (fitness_clash and id_superior)

	def create_demand(self, knowledge_packet: KnowledgePacket):
		proposals = []

		# recruit for existing ensembles
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
			coordinator =  self.get_coordinator(definition)
			if coordinator is None:
				continue
			instance = definition.instantiate(coordinator)
			impact = instance.add_impact(knowledge_packet.knowledge)
			if self.evaluate_assignment(
					knowledge_packet.knowledge.assignment.fitness_gain,
					knowledge_packet.knowledge.assignment.node_id,
					impact,
					self.node.id):
				print(f'N{self.node.id} demanding new {str(instance)} from pkg from {knowledge_packet.id}, add impact: ' + str(impact))
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
		""" Process external demands to assign reactor managed components """
		if demand.component_id not in map(lambda x: x.id, self.node.get_components()):
			return

		print("Reactor processing demand packet")

		assignment = self.node.get_component_by_id(demand.component_id).knowledge.assignment

		# Assign free component
		if assignment.node_id is None:
			self.assign(demand.component_id, demand.node_id, demand.fitness_difference)
			return

		# Re-assign component
		if self.evaluate_assignment(assignment.fitness_gain, assignment.node_id, demand.fitness_difference, demand.node_id):
			self.assign(demand.component_id, demand.node_id, demand.fitness_difference)
			return

	def assign(self, component_id: int, node_id: int, fitness_difference: float):
		""" Assign a component of this node to another node """
		# TODO: One more vote for keeping components in a dictionary
		print(f'assigning {component_id} to {node_id}')
		for component in self.node.get_components():
			if component.id == component_id:
				component.knowledge.assignment = AssignmentRecord(node_id, fitness_difference)

	def process_assignment(self, knowledge_packet: KnowledgePacket):
		""" Assign/Update a component of another node to a ensemble in this node """
		assignment = knowledge_packet.knowledge.assignment

		# Already in ensemble, update
		for instance in self.instances:
			if instance.contains(knowledge_packet.id):
				# updates member knowledge
				new_knowledge = []
				for mk in instance.memberKnowledge:
					if mk.id is knowledge_packet.knowledge.id:
						new_knowledge.append(knowledge_packet.knowledge)
					else:
						new_knowledge.append(mk)
				instance.memberKnowledge = new_knowledge
				# TODO: Record assignment timestamps
				return
		# TODO: Moves between ensembles on the same node

		# We received assignment for non existent demand
		if knowledge_packet.id not in self.demands:
			return

		# Process according to demand
		demand = self.demands[knowledge_packet.id]
		if isinstance(demand.target_ensemble, EnsembleDefinition):
			print("Reactor: Node " + str(self.node.id) + " creating new " + str(demand.target_ensemble) + " with component " + str(knowledge_packet.id))
			instance = demand.target_ensemble.instantiate()
			knowledge = knowledge_packet.knowledge
			setattr(knowledge, 'node_id', knowledge_packet.from_node_id)
			instance.add(knowledge)
			self.instances.append(instance)

		elif isinstance(demand.target_ensemble, EnsembleInstance):
			print("Reactor: Node " + str(self.node.id) + " Adding to ensemble " + str(demand.target_ensemble) + " component " + str(knowledge_packet.id))
			demand.target_ensemble.add(knowledge_packet.knowledge)
		else:
			raise Exception("demand.target_ensemble should contain definition or instance", demand.target_ensemble)
