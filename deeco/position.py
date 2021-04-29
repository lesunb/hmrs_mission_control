import math


class Position:
	EQ_THRESHOLD = 0.000001

	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def __str__(self):
		return str.format("[{0:f}, {1:f}]", self.x, self.y)

	def __eq__(self, other):
		return self.dist_to(other) < Position.EQ_THRESHOLD

	def __sub__(self, other):
		return Position(self.x - other.x, self.y - other.y)

	def __truediv__(self, scalar: float):
		"""Position(x1/x2, y1/y2)"""
		return Position(self.x / scalar, self.y / scalar)

	def __mul__(self, other):
		return Position(self.x * other, self.y * other)

	def __add__(self, other):
		return Position(self.x + other.x, self.y + other.y)

	def dist_to(self, other):
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

	@staticmethod
	def average(*other):
		x = 0
		y = 0

		for position in other:
			x += position.x
			y += position.y

		return Position(x / len(other), y / len(other))

	def length(self):
		return math.sqrt(self.x**2 + self.y**2)
