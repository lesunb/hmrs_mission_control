from deeco.core import Node
from deeco.sim import Sim
from deeco.position import Position
from deeco.plugins.identity_replicas import IdentityReplicas
from deeco.plugins.simplenetwork import SimpleNetwork
from deeco.plugins.walker import Walker
from deeco.plugins.knowledgepublisher import KnowledgePublisher
from deeco.plugins.ensemblereactor import EnsembleReactor

from robot import Robot
from robotgroup import RobotGroup
from deeco.plugins.snapshoter import Snapshoter

print("Running simulation")

sim = Sim()

# Add snapshoter plugin
Snapshoter(sim, period_ms=100)

# Add identity replicas plugin (provides replicas using deep copies of original knowledge)
IdentityReplicas(sim)

# Add simple network device
SimpleNetwork(sim, range_m=3, delay_ms_mu=20, delay_ms_sigma=5)

# Add X nodes hosting one component each
for i in range(0, 5):
	position = Position(2 * i, 3 * i)

	node = Node(sim)
	Walker(node, position)
	KnowledgePublisher(node)
	EnsembleReactor(node, [RobotGroup()])

	robot = Robot(node)

	node.add_component(robot)

# Run the simulation
sim.run(60000)
