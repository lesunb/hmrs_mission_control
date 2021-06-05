from abc import abstractmethod
from deeco.core import Runnable


class SimPlugin(Runnable):
	def __init__(self, sim):
		super().__init__()
		self.sim = sim
		sim.add_plugin(self)

	def attach_to(self, node):
		pass
