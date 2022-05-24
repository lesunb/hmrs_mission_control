

from lagom import Container

from deeco.core import Node
from deeco.sim import Sim
from deeco.plugins.identity_replicas import IdentityReplicas
from deeco.plugins.simplenetwork import SimpleNetwork
from deeco.plugins.knowledgepublisher import KnowledgePublisher
from deeco.plugins.ensemblereactor import EnsembleReactor


from mission_control.utils.logger import ContextualLogger
from mission_control.deeco_integration.mission_coordination_ensemble import MissionCoordinationEnsemble
from mission_control.deeco_integration.robot import Robot
from mission_control.deeco_integration.coordinator import Coordinator
from mission_control.deeco_integration.plugins.requests_queue import RequestsQueue
from mission_control.deeco_integration.mission_coordination_ensemble import MissionCoordinationEnsemble

from mission_control.utils.timer import Timer
from mission_control.deeco_integration.deeco_timer import DeecoTimer

from mission_control.data_model.restrictions import Battery
from mission_control.coordination import CoalitionFormationProcess

from resources.world_lab_samples import *
from .to_executor import prep_plan
from .scenario import Scenario

print("Running simulation")
class SimExec:
    def __init__(self, container: Container):
        self.cf_process: CoalitionFormationProcess = container[CoalitionFormationProcess]
        self.cl = container[ContextualLogger]

    @staticmethod
    def instantiate_robot_component(node, battery_charge, **initial_knowledge):
         return Robot(node=node,
            battery = Battery(
                capacity = 1,
				charge = battery_charge
                ),
            **initial_knowledge)

    def run(self, scenario: Scenario, limit_ms=5000):
        print(f'init scenario {scenario.code}')
        self.cl.start_group_context(f'{scenario.code}')
        requests = scenario.requests
        robots_initial_conf = scenario.robots
        
        cf_process = self.cf_process

        sim = Sim()

        # Add identity replicas plugin (provides replicas using deep copies of original knowledge)
        IdentityReplicas(sim)

        # Add simple network device
        SimpleNetwork(sim)
        
        # wire sim timer with container timer
        timer:DeecoTimer = container[Timer]
        timer.scheduler = sim.scheduler

        # create coordinator
        coord_node = Node(sim)        
        # node plugins
        KnowledgePublisher(coord_node)
        RequestsQueue(coord_node, requests)
        EnsembleReactor(coord_node, [ MissionCoordinationEnsemble() ])

        # mission coordinator component
        coord = Coordinator(coord_node, name='mission_coordinator', required_skills=[], cf_process=cf_process)
        coord_node.add_component(coord)

        robots, robots_nodes = [], []


        # instantiate workers
        for r in robots_initial_conf:
            
            node = Node(sim)
            robot = self.instantiate_robot_component(node, **r)
            node.add_component(robot)
            # node plugins
            KnowledgePublisher(node)
            EnsembleReactor(node, [ MissionCoordinationEnsemble() ])

            # save to report
            robots_nodes.append(node)
            robots.append(robot)

        # Run the simulation
        sim.run(limit_ms)
        self.cl.end_all_contexts()

        # get results
        local_plans = list(map(prep_plan, robots))
        
        for local_plan, robot in zip(local_plans, scenario.robots):
            robot['local_plan'] = local_plan
        
        return {
            'nodes': {
                'coord_node': coord_node,
                'robots': robots_nodes
            },
            'components': {
                'coordinator': coord.knowledge,
                'robots': list(map(lambda r : r.knowledge, robots))
            },
            'local_plans': local_plans,
            'missions': coord.knowledge.missions
        }


