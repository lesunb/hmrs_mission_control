from deeco.runnable import NodePlugin


class Replicas(NodePlugin):
	def __init__(self, node):
		super().__init__(node)

		self.storage = []

		# Provide access to this plugin
		node.replicas = self

	def store(self, knowledge):
		self.storage.append(knowledge)

	def get(self, role_bases):
		return self.storage
