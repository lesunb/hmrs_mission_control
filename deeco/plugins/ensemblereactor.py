from typing import Generic, List, TypeVar
from deeco.core import BaseKnowledge, Component, EnsembleDefinition, Identifiable, NodePlugin, UUID
from deeco.core import Node
from deeco.packets import Packet
from deeco.packets import KnowledgePacket, PatchPacket
from deeco.packets import PacketType
from deeco.packets import DemandPacket
from deeco.mapping import Mapping

class DemandRecord:
    def __init__(self, component_uuid: int, fitness_difference: float, target_ensemble):
        self.component_uuid = component_uuid
        self.fitness_difference = fitness_difference
        self.target_ensemble = target_ensemble

    def __hash__(self):
        return self.component_uuid.__hash__()


class AssignmentRecord:
    def __init__(self, node_id: int, fitness_gain: float, last_update = None):
        self.node_id = node_id
        self.fitness_gain = fitness_gain
        self.last_update = last_update



T = TypeVar('T')

class EnsembleMember(Identifiable, Generic[T]):
    def __init__(self, knowledge: T, component_uuid: UUID, node_uuid: UUID):
        super().__init__(component_uuid)
        self.knowledge, self.node_uuid, self.component_uuid = knowledge, node_uuid, component_uuid



class EnsembleInstance:

    def __init__(self, definition: EnsembleDefinition, coordinator: Component):
        self.definition = definition
        self.coordinator = coordinator

        self.__members: dict[UUID, EnsembleMember] = dict()

    # def id(self):
    #     return hash(map(lambda x: x.id, self.memberKnowledge))

    def is_member(self, component_uuid: UUID):
        return component_uuid in self.__members

    def get_member(self, component_uuid: UUID):
        return self.__members[component_uuid]

    def members_uuids(self):
        return list(self.__members.keys())

    def add(self, knowledge: BaseKnowledge, component_uuid:UUID, **metadata):
        if component_uuid in self.__members:
            raise Exception(f'trying to add a member({component_uuid}) already in the ensemble')
        
        member = EnsembleMember(knowledge=knowledge, component_uuid=component_uuid, **metadata)
    
        # TODO: Filter out outdated knowledge
        # self.memberKnowledge = list(filter(lambda x: x.uuid != knowledge.uuid, self.memberKnowledge))
        self.__members[component_uuid]=member

    def fitness(self):
        return self.fitness_of(None)

    def fitness_of(self, candidate):
        try:
            return self.definition.fitness(self.coordinator.knowledge, candidate)
        except (TypeError, AttributeError) as e:
            print(e)
            return 0

    def membership_of(self, member_knowledge: BaseKnowledge):
        try:
            if not isinstance(member_knowledge, self.definition.member):
                return False
            else:
                return self.definition.membership(self.coordinator.knowledge, member_knowledge)
        except (TypeError, IndexError) as e:
            print(e)
            return False

    def membership(self):
        is_active = False
        for _, member in self.__members.items():
            if self.membership_of(member.knowledge):
                is_active = True
            else:
                # TODO
                print('should unsubscribe {mk} from {self}')
        return is_active

    def knowledge_exchange(self):
        patches = []
        coordinator = self.coordinator

        for _, member in self.__members.items():
            coord, member_mappings =  self.definition.knowledge_exchange(coordinator.knowledge, member)
            patches.append( (member.node_uuid, member.component_uuid, member_mappings))
        return patches

    def add_impact(self, knowledge):
        if not self.membership_of(knowledge): # cordinator and new one
            return  float('-inf')
        else:
            new_fitness = self.fitness_of(knowledge)
            old_fitness = self.fitness()
            return new_fitness - old_fitness

    def remove_impact(self, knowledge):
        new_members = filter(lambda x: x.id != knowledge.id, self.memberKnowledge)
        return self.definition.fitness(new_members) - self.fitness()

    def replace_impact(self, added_knowledge, removed_knowledge):
        return self.add_impact(added_knowledge) + self.remove_impact(removed_knowledge)

    def __str__(self):
        return self.__class__.__name__ + " of " + str(self.definition) + " from node " + str(self.coordinator.node.id)

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
        for component in self.node.components:
            component.knowledge.assignment = AssignmentRecord(None, 0)

        scheduler.set_periodic_timer(self.react, period_ms=1000)
        self.initial_instances()

    def get_coordinator(self, definition):
        for component in self.node.components:
            if isinstance(component.knowledge, definition.coordinator):
                return component
        return None


    def initial_instances(self):
        """ create instances for roles that are coordinators in definitions the node knows """
        for component in self.node.components:
            for definition in self.definitions:
                if isinstance(component.knowledge, definition.coordinator):
                    instance = EnsembleInstance(definition, component)
                    self.assign(component, self.node.id, 0)
                    self.instances.append(instance)

    def react(self, time_ms):
        #print("Reactor invoked, sending demands and assignments")

        for _, demand in self.demands.items():
            packet = DemandPacket(time_ms, demand.component_uuid, self.node.id, demand.fitness_difference)
            self.node.networkDevice.broadcast(packet)

        # TODO: Maintain ensembles check timestamps

        self.run_ensembles(time_ms)

        # for instance in self.instances:
        #     print("### Node " + str(self.node.id) + " ensemble instance " + str(instance) + " with components: " )

    def run_ensembles(self, time_ms: int):
        # advertise existing ensembles? 
        # TODO suspend ensemble advertisement
        #
        for instance in self.instances:
            if instance.membership():
                print("### Active instance: " + str(instance))
                member_mappings = instance.knowledge_exchange()
                for (node_id, component_uuid, patch) in member_mappings:
                    packet = PatchPacket(component_uuid, patch, time_ms)
                    self.node.networkDevice.send(node_id, packet)

    def receive(self, packet: Packet, time_ms):
        packet.receive_timestamp = time_ms
        if packet.type == PacketType.PATCH and isinstance(packet, PatchPacket):
            self.process_patch(packet)

        elif packet.type == PacketType.KNOWLEDGE and isinstance(packet, KnowledgePacket):
            self.process_knowledge(packet)

        elif packet.type == PacketType.DEMAND and isinstance(packet, DemandPacket):
            self.process_demand(packet)
        else:
            print(f'no identified {packet}')


    def process_patch(self, patch_packet: PatchPacket):
        uuid = patch_packet.component_uuid
        target_component= self.node.get_component(uuid)
        if not target_component:
            raise Exception('wrong patch')

        target_component.knowledge.assignment.last_update = patch_packet.timestamp_ms
        if patch_packet.patch:
            Mapping.apply_all(patch_packet.patch, target_component.knowledge)

    def process_knowledge(self, knowledge_packet: KnowledgePacket):
#		print("Reactor processing knowledge packet")
        # print(f'{self.node.id} recieved a package of type {knowledge_packet.knowledge.__class__}')
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
                component = self.node.get_component(member.id)
                if component is not None:
                    return True
        return False
    
    def merge_knwoledge_from_ensemble(self, knowledge_packet: KnowledgePacket):
        for member in knowledge_packet.members:
            component = self.node.get_component(member.id)
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
                # print("Demanding to upgrade ensemble instance, add impact: " + str(impact))
                demand = DemandRecord(knowledge_packet.component_uuid, impact, instance)
                proposals.append(demand)
    
        # Build new ensemble instance if possible
        for definition in self.definitions:
            coordinator =  self.get_coordinator(definition)
            if coordinator is None:
                continue
            instance = EnsembleInstance(definition, coordinator)
            impact = instance.add_impact(knowledge_packet.knowledge)
            if self.evaluate_assignment(
                    knowledge_packet.knowledge.assignment.fitness_gain,
                    knowledge_packet.knowledge.assignment.node_id,
                    impact,
                    self.node.id):
                print(f'N{self.node.id} demanding new {str(instance)} from pkg from {knowledge_packet.component_uuid}, add impact: ' + str(impact))
                demand = DemandRecord(knowledge_packet.component_uuid, impact, definition)
                proposals.append(demand)


        # Create demand for existing local ensemble instance
        for instance in filter(lambda x: x.is_member(knowledge_packet.component_uuid), self.instances):
            demand = DemandRecord(knowledge_packet.id, knowledge_packet.knowledge.assignment.fitness_gain, instance)
            proposals.append(demand)

        # Pick best demand
        demand = None
        for proposal in proposals:
            if demand is None or proposal.fitness_difference > demand.fitness_difference:
                demand = proposal

        # Set best demand
        if knowledge_packet.component_uuid in self.demands:
            del self.demands[knowledge_packet.component_uuid]
        if demand is not None:
            self.demands[knowledge_packet.component_uuid] = demand

    def process_demand(self, demand: DemandPacket):
        """ Process external demands to assign reactor managed components """
        # print("Reactor processing demand packet")
        comp = self.node.get_component(demand.component_uuid)
        if not comp:
            return
        assignment = comp.knowledge.assignment

        # Assign free component
        if assignment.node_id is None:
            self.assign(comp, demand.node_id, demand.fitness_difference)
            return

        # Re-assign component
        if self.evaluate_assignment(assignment.fitness_gain, assignment.node_id, demand.fitness_difference, demand.node_id):
            self.assign(comp, demand.node_id, demand.fitness_difference)
            return

    def assign(self, component: Component, node_id: int, fitness_difference: float):
        """ Assign a component of this node to another node """
        # TODO: One more vote for keeping components in a dictionary
        print(f'assigning {component.uuid} to {node_id}')
        component.knowledge.assignment = AssignmentRecord(node_id, fitness_difference)				

    def process_assignment(self, knowledge_packet: KnowledgePacket):
        """ Assign/Update a component of another node to a ensemble in this node """
        component_uuid = knowledge_packet.component_uuid
        knowledge = knowledge_packet.knowledge
        node_uuid = knowledge_packet.from_node_id

        # Already in ensemble, update
        for instance in self.instances:
            if instance.is_member(component_uuid):
                # updates member knowledge
                mk = instance.get_member(component_uuid)
                mk.knowledge = knowledge_packet.knowledge
                # TODO: Record assignment timestamps
                return
        # TODO: Moves between ensembles on the same node

        # We received assignment for non existent demand
        if knowledge_packet.component_uuid not in self.demands:
            return

        # Process according to demand
        demand = self.demands[knowledge_packet.component_uuid]
        if isinstance(demand.target_ensemble, EnsembleDefinition):
            print("Reactor: Node " + str(self.node.id) + " creating new " + str(demand.target_ensemble) + " with component " + str(knowledge_packet.component_uuid))
            instance = EnsembleInstance(demand.target_ensemble)
            knowledge = knowledge_packet.knowledge
            setattr(knowledge, 'node_id', knowledge_packet.from_node_id)
            instance.add(knowledge)
            self.instances.append(instance)

        elif isinstance(demand.target_ensemble, EnsembleInstance):
            print("Reactor: Node " + str(self.node.id) + " Adding to ensemble " + str(demand.target_ensemble) + " component " + str(component_uuid))
            demand.target_ensemble.add(knowledge, component_uuid, node_uuid = node_uuid)
        else:
            raise Exception("demand.target_ensemble should contain definition or instance", demand.target_ensemble)


def get_knowledge_about(reactor: EnsembleReactor, member:Component):
    return map(lambda i:i.get_member(member.uuid).knowledge, reactor.instances)


def has_member(reactor: EnsembleReactor, member:Component):
    return any(get_knowledge_about(reactor, member))
