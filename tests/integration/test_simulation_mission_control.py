from deeco.core import Node
from deeco.sim import Sim
from deeco.position import Position
from deeco.plugins.identity_replicas import IdentityReplicas
from deeco.plugins.simplenetwork import SimpleNetwork
from deeco.plugins.walker import Walker
from deeco.plugins.knowledgepublisher import KnowledgePublisher
from deeco.plugins.ensemblereactor import EnsembleReactor

from deeco.plugins.snapshoter import Snapshoter

from mission_control.deeco_integration.robot import Robot
from mission_control.deeco_integration.coordinator import Coordinator
from mission_control.deeco_integration.mission_ensemble import MissionEnsemble
from mission_control.deeco_integration.plugins.workload import WorkloadLoader
from mission_control.deeco_integration.hande_request_service import HandleRequestServer
from mission_control.deeco_integration.request import Request



print("Running simulation")

from ..world_collector import *

def test_sim(cf_manager, ihtn_collect):
    sim = Sim()
    # Add snapshoter plugin
    Snapshoter(sim, period_ms=100)

    # Add identity replicas plugin (provides replicas using deep copies of original knowledge)
    IdentityReplicas(sim)

    # Add simple network device
    SimpleNetwork(sim, range_m=3000, delay_ms_mu=20, delay_ms_sigma=5)

    # create coordinator
    coord_node = Node(sim)
    position = Position(0, 0)
    Walker(coord_node, position) # TODO remove
    KnowledgePublisher(coord_node)
    EnsembleReactor(coord_node, [MissionEnsemble()])
    coord = Coordinator(coord_node, required_skills = ['secure_transport'] )
    coord_node.add_component(coord)
    HandleRequestServer(coord_node, cf_manager)

    # get workload
    client = Node(sim)
    Walker(client, Position(0, 0)) # TODO remove
    WorkloadLoader(client, coord_node, [ { 'timestamp': 3000, 'content': ihtn_collect}])

    # create an inventory 


    # Add X nodes hosting one component each
    for i in range(0, 5):
        position = Position(2 * i, 3 * i)

        node = Node(sim)
        Walker(node, position)
        KnowledgePublisher(node)
        EnsembleReactor(node, [MissionEnsemble()])

        robot = Robot(node, provided_skills = ['secure_transport'])
        node.add_component(robot)

    # Run the simulation
    sim.run(3100)

    # check success / timespan

    # check failure



