import os

import jsonpickle as json

from deeco.runnable import SimPlugin


class Snapshoter(SimPlugin):
	def __init__(self, sim, period_ms: int = 1000, snapshot_dir: str = "logs"):
		super().__init__(sim)
		self.period_ms = period_ms

		self.snapshot_dir = snapshot_dir

		if snapshot_dir is not None:
			try:
				os.mkdir(self.snapshot_dir)
			except FileExistsError as e:
				pass

	def run(self, scheduler):
		# Schedule snapshot execution
		self.sim.scheduler.set_periodic_timer(self.snapshot_system, period_ms=self.period_ms)

	def snapshot_system(self, time_ms: int):
		# Snapshot the system
		if self.snapshot_dir is not None:
			log = open(self.snapshot_dir + os.sep + str(time_ms) + ".json", "w")
			dump = json.encode({"time_ms": time_ms, "nodes": self.sim.nodes}, unpicklable=False)
			log.write(dump)
			log.close()
