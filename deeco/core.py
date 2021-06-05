from __future__ import annotations

from abc import abstractmethod
from typing import Any, List

import shortuuid

class ComponentRole:
    pass

class Group(ComponentRole):
    def __init__(self):
        super().__init__()
        self.members = []

class UUID(str):
    pass

class Identifiable:

    def __init__(self, uuid = None):
        super().__init__()
        if uuid:
            self.__uuid = uuid
        else:
            self.__uuid: UUID = self.gen_new_uuid()
    
    @staticmethod
    def gen_new_uuid() -> UUID:
        return shortuuid.uuid()

    @property
    def uuid(self):
        return self.__uuid

    def isid(self, uuid: str) -> bool:
        return self.__uuid == uuid

    def same_uuid(self, other: Any):
        if isinstance(other, Identifiable):
            return other.uuid == self.uuid
        return False


class BaseKnowledge(ComponentRole):
    def __init__(self):
        self.time = None

class Component(Identifiable):
    counter = 0

    class Knowledge(BaseKnowledge):
        pass

    def __init__(self, node: Node):
        super().__init__()
        self.node = node
        self.time = None
        self.knowledge = self.Knowledge()
        self.metadata = Metadata()


class Runnable:
	def run(self, scheduler):
		pass


class Runtime:
	@abstractmethod
	def add_runnable(self, runnable: Runnable):
		pass

	@abstractmethod
	def add_plugin(self, plugin):
		pass

	@abstractmethod
	def get_scheduler(self):
		pass
	
	@abstractmethod
	def add_node(self, node):
		pass

class NodePlugin(Runnable):
	def __init__(self, node: Node):
		self.node = node
		node.add_plugin(self)

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
        self.__components: dict[UUID, Component] = {}

        # Deploy system plugins on node
        for plugin in runtime.plugins:
            plugin.attach_to(self)

    def __getstate__(self):
        return {"id": self.id, "components": self.components}

    def add_component(self, component:Component):
        self.__components[component.uuid] = component

    @property
    def components(self) -> List[Component]:
        return list(self.__components.values())

    def get_components_uuids(self):
        return list(self.__components.keys())

    def get_component(self, uuid: UUID) -> Component:
        return self.__components.get(uuid)

    def add_plugin(self, plugin: NodePlugin):
        self.plugins.append(plugin)

    def run(self, scheduler):
        # schedule plugins
        for plugin in self.plugins:
            plugin.run(scheduler)

        # schedule component (processes)
        for component in self.__components.values():
            for entry in type(component).__dict__.values():
                if hasattr(entry, "is_process"):
                    method = process_factory(component, entry, self)
                    scheduler.set_periodic_timer(method, entry.period_ms)


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


class EnsembleDefinition:
    class Knowledge:
        pass
    
    def __init__(self, coordinator: ComponentRole, member: ComponentRole):
        self.coordinator = coordinator
        self.member = member

    @abstractmethod
    def fitness(self, coordinator, candidate) -> float:
        pass

    @abstractmethod
    def membership(self, coordinator, candidate):
        pass

    @abstractmethod
    def knowledge_exchange(self, coordinator, candidate):
        pass
