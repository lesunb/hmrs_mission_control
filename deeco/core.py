from abc import abstractmethod

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


class Identifiable(Role):
	def __init__(self):
		super().__init__()
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

	@abstractmethod
	def fitness(self, *knowledge):
		pass

	@abstractmethod
	def membership(self, *knowledge):
		pass

	@abstractmethod
	def knowledge(self, *knowledge):
		pass

	def instantiate(self):
		return EnsembleInstance(self)


class EnsembleInstance:
	def __init__(self, definition: EnsembleDefinition):
		self.definition = definition
		self.memberKnowledge = []

	def id(self):
		return hash(map(lambda x: x.id, self.memberKnowledge))

	def contains(self, component_id: int):
		return component_id in map(lambda x: x.id, self.memberKnowledge)

	def add(self, knowledge: BaseKnowledge):
		# TODO: Filter out outdated knowledge
		self.memberKnowledge = list(filter(lambda x: x.id != knowledge.id, self.memberKnowledge))
		self.memberKnowledge.append(knowledge)

	def fitness(self):
		return self.fitness_of(self.memberKnowledge)

	def fitness_of(self, member_knowledge):
		try:
			return self.definition.fitness(*member_knowledge)
		except (TypeError, AttributeError):
			return 0

	def membership_of(self, member_knowledge):
		try:
			return self.definition.membership(*member_knowledge)
		except TypeError:
			return False

	def membership(self):
		return self.membership_of(self.memberKnowledge)

	def knowledge(self):
		return self.definition.knowledge(*self.memberKnowledge)

	def add_impact(self, knowledge):
		new_members = self.memberKnowledge + [knowledge]
		new_fitness = self.fitness_of(new_members)
		old_fitness = self.fitness()
		return new_fitness - old_fitness

	def remove_impact(self, knowledge):
		new_members = filter(lambda x: x.id != knowledge.id, self.memberKnowledge)
		return self.definition.fitness(new_members) - self.fitness()

	def replace_impact(self, added_knowledge, removed_knowledge):
		return self.add_impact(added_knowledge) + self.remove_impact(removed_knowledge)

	def __str__(self):
		return self.__class__.__name__ + " of " + str(self.definition) + " with id " + str(self.id())