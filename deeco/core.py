from abc import abstractmethod
from copy import deepcopy

from deeco.runnable import *
from deeco.packets import KnowledgePacket

class Node(Runnable):
    counter = 0

    @staticmethod
    def __gen_id():
        identifier = Node.counter
        Node.counter += 1
        return identifier

    def __init__(self, runtime: Runtime):
        runtime.add_node(self)

        self.runtime = runtime
        self.id = self.__gen_id()

        self.plugins = []
        self.components = []

        # Deploy system plugins on node
        for plugin in runtime.plugins:
            plugin.attach_to(self)

    def __getstate__(self):
        return {"id": self.id, "components": self.components}

    def add_component(self, component):
        self.components.append(component)

    def get_components(self):
        return self.components

    def get_component_ids(self):
        return map(lambda x: x.id, self.components)

    def get_component_by_id(self, id: int):
        for component in self.components:
            if component.id == id:
                return component

        return None

    def add_plugin(self, plugin: NodePlugin):
        self.plugins.append(plugin)

    def run(self, scheduler):
        # schedule plugins
        for plugin in self.plugins:
            plugin.run(scheduler)

        # schedule component (processes)
        for component in self.components:
            for entry in type(component).__dict__.values():
                if hasattr(entry, "is_process"):
                    method = process_factory(component, entry, self)
                    scheduler.set_periodic_timer(method, entry.period_ms)


class Role:
    pass

class Group(Role):
    def __init__(self):
        super().__init__()
        self.members = []

class Identifiable(Role):
    def __init__(self):
        super().__init__()
        self.node_id = None
        self.id = None


class TimeStamped(Role):
    def __init__(self):
        super().__init__()
        self.time = None


class BaseKnowledge(Identifiable, TimeStamped):
    def __init__(self):
        super().__init__()

class Metadata:
    def __init__(self):
        self.coordinatedBy = None
        self.coordinating = None


def process(period_ms: int):
    def process_with_period(method):
        method.is_process = True
        method.period_ms = period_ms
        return method

    return process_with_period


def process_factory(component, entry, node: Node):
    return lambda time_ms: entry(component, node)


class Component:
    counter = 0

    class Knowledge:
        pass

    @staticmethod
    def gen_id():
        identifier = Component.counter
        Component.counter += 1
        return identifier

    def __init__(self, node: Node):
        self.id = self.gen_id()

        self.time = None
        self.knowledge = self.Knowledge()
        self.knowledge.id = self.id
        self.metadata = Metadata()


class EnsembleDefinition:
    class Knowledge:
        pass
    
    def __init__(self, coordinator: Role, member: Role):
        self.coordinator = coordinator
        self.member = member

    @abstractmethod
    def fitness(self, candidate, *members):
        pass

    @abstractmethod
    def membership(self, *knowledge):
        pass

    @abstractmethod
    def knowledge_exchange(self, *knowledge):
        pass

    def instantiate(self, coordinator):
        return EnsembleInstance(self, coordinator)


class EnsembleInstance:
    def __init__(self, definition: EnsembleDefinition, coordinator: Component):
        self.definition = definition
        self.memberKnowledge = []
        self.coordinator = coordinator

    def id(self):
        return hash(map(lambda x: x.id, self.memberKnowledge))

    def contains(self, component_id: int):
        return component_id in map(lambda x: x.id, self.memberKnowledge)

    def add(self, knowledge: BaseKnowledge):
        # TODO: Filter out outdated knowledge
        self.memberKnowledge = list(filter(lambda x: x.id != knowledge.id, self.memberKnowledge))
        self.memberKnowledge.append(knowledge)

    def fitness(self):
        return self.fitness_of(None, *self.memberKnowledge)

    def fitness_of(self, candidate, *members_knowledge):
        try:
            return self.definition.fitness(self.coordinator.knowledge, candidate, *members_knowledge)
        except (TypeError, AttributeError) as e:
            print(e)
            return 0

    def membership_of(self, member_knowledge):
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
        for mk in self.memberKnowledge:
            if self.membership_of(mk):
                is_active = True
            else:
                print('should unsubscribe {mk} from {self}')
        return is_active

    def knowledge_exchange(self):
        patches = []
        coordinator = self.coordinator

        for member in self.memberKnowledge:
            coord, member_mappings =  self.definition.knowledge_exchange(coordinator.knowledge, member)
            patches.append( (member.node_id, member.id, member_mappings))
        return patches

    def add_impact(self, knowledge):
        if not self.membership_of(knowledge): # cordinator and new one
            return  float('-inf')
        else:
            new_fitness = self.fitness_of(knowledge, self.memberKnowledge)
            old_fitness = self.fitness()
            return new_fitness - old_fitness

    def remove_impact(self, knowledge):
        new_members = filter(lambda x: x.id != knowledge.id, self.memberKnowledge)
        return self.definition.fitness(new_members) - self.fitness()

    def replace_impact(self, added_knowledge, removed_knowledge):
        return self.add_impact(added_knowledge) + self.remove_impact(removed_knowledge)

    def __str__(self):
        return self.__class__.__name__ + " of " + str(self.definition) + " with id " + str(self.id())