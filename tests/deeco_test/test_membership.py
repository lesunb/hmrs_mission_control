from deeco.core import Node, Component
from deeco.sim import Sim
from deeco.position import Position
from deeco.plugins.identity_replicas import IdentityReplicas
from deeco.plugins.simplenetwork import SimpleNetwork
from deeco.plugins.walker import Walker
from deeco.plugins.knowledgepublisher import KnowledgePublisher
from deeco.plugins.ensemblereactor import EnsembleReactor

from deeco.plugins.snapshoter import Snapshoter

from .robot import Robot, Rover
from .robotgroup import RobotGroup


print("Running simulation")


def test_multiple_nodes():
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
        EnsembleReactor(node, [RobotGroup(coordinator=Rover, member=Rover)])

        robot = Robot(node)

        node.add_component(robot)

    sim.run(1000)


def get_knowledge_about(reactor: EnsembleReactor, member:Component):
    for instance in reactor.instances:
        for mk in instance.memberKnowledge:
            if mk.id is member.id:
                return mk
    return None

def has_member(reactor: EnsembleReactor, member:Component):
    return get_knowledge_about(reactor, member) is not None



def test_join_ensemble_and_update_ensemble_knowledge():
    sim = Sim()

    # Add simple network device
    SimpleNetwork(sim, range_m=3, delay_ms_mu=20, delay_ms_sigma=5)

    position0 = Position(0.5, 0.5)
    node0 = Node(sim)
    Walker(node0, position0, speed_m_s=0.001/3.6)
    KnowledgePublisher(node0, publishing_period_ms=100) # same frequency that the walker
    er0 = EnsembleReactor(node0, [RobotGroup(coordinator=Rover, member=Rover)])
    robot0 = Robot(node0)
    node0.add_component(robot0)

    position1 = Position(0.4, 0.6)
    node1 = Node(sim)
    Walker(node1, position1, speed_m_s=0.001/3.6)
    KnowledgePublisher(node1)
    er1 = EnsembleReactor(node1, [RobotGroup(coordinator=Rover, member=Rover)])
    robot1 = Robot(node1)
    node1.add_component(robot1)

    sim.run(20000)
    assert has_member(er0, robot1)

    # check if er2 has an updated knowledge about robo
    dist = get_knowledge_about(er0, robot1).position.dist_to(node1.positionProvider.get())
    # assert that ensemble knowledge is at most two walker step behind
    assert dist < 2*0.001/3.6


