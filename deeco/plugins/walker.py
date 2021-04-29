from deeco.runnable import NodePlugin
from deeco.position import Position
from deeco.plugins.positionprovider import PositionProvider


class Walker(NodePlugin, PositionProvider):
	DEFAULT_SPEED_M_S = 5 / 3.6
	DEFAULT_STEP_MS = 100

	def __init__(self, node, position: Position, speed_m_s=DEFAULT_SPEED_M_S):
		super().__init__(node)

		self.position = position
		self.target = position

		self.speed_m_s = speed_m_s

		node.walker = self
		node.positionProvider = self

	def get(self):
		return self.position

	def set_target(self, target: Position):
		self.target = target

	def run(self, scheduler):
		scheduler.set_periodic_timer(self.move, period_ms=self.DEFAULT_STEP_MS)

	def move(self, time_ms):
		step = self.speed_m_s / (1000 / self.DEFAULT_STEP_MS)

		if self.position.dist_to(self.target) < step:
			self.position = self.target
		else:
			vector = self.target - self.position
			vector /= vector.length()
			vector *= step
			self.position += vector
