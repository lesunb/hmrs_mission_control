from abc import abstractmethod


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


class NodePlugin(Runnable):
	def __init__(self, node):
		self.node = node
		node.add_plugin(self)


class SimPlugin(Runnable):
	def __init__(self, sim):
		super().__init__()
		self.sim = sim
		sim.add_plugin(self)

	def attach_to(self, node):
		pass
