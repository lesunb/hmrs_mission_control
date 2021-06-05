from deeco.runnable import SimPlugin
from deeco.core import Runnable, Runtime
import types
from queue import PriorityQueue

class Timer:
	pass


class Scheduler:
	def run(self):
		pass

	def schedule_timer(self, timer: Timer):
		pass

	def get_time_ms(self):
		pass

	def set_timer(self, method: types.MethodType, time_ms: int):
		self.schedule_timer(Timer(self, method, time_ms))

	def set_periodic_timer(self, method: types.MethodType, period_ms: int, time_ms: int = 0):
		self.schedule_timer(PeriodicTimer(self, method, period_ms, time_ms))


class SimScheduler(Scheduler):
	def __init__(self):
		self.events = PriorityQueue()
		self.time_ms = None

	def run(self, limit_ms: int):
		self.time_ms = 0
		while not self.events.empty() and self.time_ms < limit_ms:
			event: Timer = self.events.get()
			self.time_ms = event.time_ms
			event.run(self.time_ms)

	def schedule_timer(self, timer: Timer):
		self.events.put(timer)

	def get_time_ms(self):
		return self.time_ms


class Timer:
	def default_method(self, time_ms):
		print("No method set for " + str(type(self)) + " at " + str(time_ms))

	def __init__(self, scheduler: Scheduler, method: types.MethodType, time_ms):
		self.scheduler = scheduler
		self.time_ms = time_ms
		self.method = method

	def __lt__(self, other):
		return self.time_ms < other.time_ms

	def run(self, time_ms: int):
		self.method(time_ms)


class PeriodicTimer(Timer):
	def __init__(self, scheduler: Scheduler, method: types.MethodType, period_ms: int, time_ms: int):
		super().__init__(scheduler, method, time_ms)
		self.period_ms = period_ms

	def run(self, time_ms: int):
		super().run(time_ms)
		self.time_ms += self.period_ms
		self.scheduler.schedule_timer(self)


class Sim(Runtime):
	def __init__(self):
		self.scheduler = SimScheduler()

		self.nodes = []
		self.plugins = []

	def add_plugin(self, plugin: SimPlugin):
		self.plugins.append(plugin)

	def add_node(self, node: Runnable):
		self.nodes.append(node)

	def run(self, limit_ms: int):
		# Schedule system plugins
		for plugin in self.plugins:
			plugin.run(self.scheduler)

		# Schedule nodes
		for node in self.nodes:
			node.run(self.scheduler)

		self.scheduler.run(limit_ms)

		print("All done")
