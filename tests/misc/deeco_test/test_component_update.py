from deeco.core import Node, Component
from deeco.sim import Sim
from deeco.position import Position
from deeco.plugins.simplenetwork import SimpleRangeLimitedNetwork
from deeco.plugins.walker import Walker
from deeco.plugins.knowledgepublisher import KnowledgePublisher
from deeco.plugins.ensemblereactor import EnsembleReactor, has_member

from deeco.plugins.snapshoter import Snapshoter

from .leader_follower import Leader, Follower, LeaderFollowingGroup

print("Running simulation")


def test_join_ensemble_and_update_knowledge():
    sim = Sim()

    # Add simple network device
    SimpleRangeLimitedNetwork(sim, range_m=3, delay_ms_mu=20, delay_ms_sigma=5)

    node0 = Node(sim)
    Walker(node0, Position(0.5, 0.5), speed_m_s=0.001/3.6)
    KnowledgePublisher(node0, publishing_period_ms=100) # same frequency that the walker
    er0 = EnsembleReactor(node0, [LeaderFollowingGroup()])
    robot0 = Leader(node0)
    node0.add_component(robot0)


    node1 = Node(sim)
    Walker(node1, Position(0.4, 0.6), speed_m_s=0.1/3.6)
    KnowledgePublisher(node1)
    er1 = EnsembleReactor(node1, [LeaderFollowingGroup()])
    robot1 = Follower(node1)
    node1.add_component(robot1)

    sim.run(10000)
    assert has_member(er0, robot1)

    # check if er2 has an updated knowledge about robo
    dist = node0.positionProvider.get().dist_to(node1.positionProvider.get())
    # assert that ensemble knowledge is at most one walker step behind
    assert dist < 0.01/3.6


