from deeco.core import Node
from deeco.sim import Sim
from deeco.position import Position
from deeco.plugins.identity_replicas import IdentityReplicas
from deeco.plugins.simplenetwork import SimpleNetwork
from deeco.plugins.walker import Walker
from deeco.plugins.knowledgepublisher import KnowledgePublisher
from deeco.plugins.ensemblereactor import EnsembleReactor

from deeco.plugins.snapshoter import Snapshoter

from .robot import Robot
from .robotgroup import RobotGroup


print("Running simulation")


def test_sim():
    sim = Sim()
    # Add snapshoter plugin
    Snapshoter(sim, period_ms=100)

    # Add identity replicas plugin (provides replicas using deep copies of original knowledge)
    IdentityReplicas(sim)

    # Add simple network device
    SimpleNetwork(sim, range_m=3, delay_ms_mu=20, delay_ms_sigma=5)

    for i in range(0, 5):
        position = Position(2 * i, 3 * i)

        node = Node(sim)
        Walker(node, position)
        KnowledgePublisher(node)
        EnsembleReactor(node, [RobotGroup()])

        robot = Robot(node)

        node.add_component(robot)

    sim.run(1000)



