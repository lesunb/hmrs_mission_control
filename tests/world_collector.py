from mission_control.processes.integration import MissionHandler
from mission_control.processes.sequencing import SkillImplementation, SkillLibrary, TickStatus
import pytest

from lagom import Container
from typing import List

from enum import Enum

from mission_control.core import MissionContext, Role, Worker, worker_factory, POI
from mission_control.estimate.core import SkillDescriptorRegister
from mission_control.estimate.estimate import EstimateManager
from mission_control.processes.coalition_formation import CoalitionFormationProcess
from mission_control.mission.ihtn import Method, ElementaryTask, AbstractTask

from mission_control.common_descriptors.routes_ed import RoutesEnvironmentDescriptor, Map, Nodes
from mission_control.common_descriptors.navigation_sd import NavigationSkillDescriptor, Move
from mission_control.common_descriptors.generic_constant_cost_sd import generic_skill_descriptor_constant_cost_factory

from mission_control.common_descriptors.routes_ed import Map

###
# Produces:
#  - a simple mission with two tasks
#  - three robots
#  - a EnstimateManager
#  - 

##
class task_type(Enum):
    NAV_TO = 'navigation'
    PICK_UP = 'pick_up'

class poi(Enum):
    sr = POI('storage_room')
    room1 = POI('room1')
    room3 = POI('room3')

def create_map() -> Map:
    map = Map()
    ic_corridor = Nodes("IC Corridor", [-37, 15])

    sr = Nodes("storage_room", [-37, 35])
    ic_room_1 = Nodes("room1", [-38, 35])
    ic_room_2 = Nodes("room2", [-34, 35])
    ic_room_3 = Nodes("room3", [-38, 23])

    ic_corridor.add_edges([sr, ic_room_1, ic_room_2, ic_room_3])
    
    sr.add_edges([ic_corridor])
    ic_room_1.add_edges([ic_corridor])
    ic_room_2.add_edges([ic_corridor])
    ic_room_3.add_edges([ic_corridor])

    map.add_nodes([ic_corridor, sr, ic_room_1, ic_room_2,
                   ic_room_3])
    return map

for enum_item in poi:
    setattr(enum_item.value, 'name', enum_item.name)

role_r1 = Role('r1')

class robot(Enum):
    a = worker_factory(location = poi.sr.value, 
        capabilities=[
            Move(avg_speed = 10, u='m/s')
        ],
        skills=[task_type.NAV_TO.value, task_type.PICK_UP.value])
    b = worker_factory(location = poi.room1.value, 
        capabilities=[
            Move(avg_speed = 15, u='m/s')
        ],
        skills=[task_type.NAV_TO.value, task_type.PICK_UP.value])
    c = worker_factory(location = poi.room1.value, 
        capabilities=[
            Move(avg_speed = 20, u='m/s')
        ],
        skills=[task_type.NAV_TO.value])

for enum_item in robot:
    setattr(enum_item.value, 'name', enum_item.name)
robots = [ unit.value for unit in robot ]

# Defined as Enum so we can reference methods and tasks, and we can have references
# to names that we later on set on them with set_name()
class collection_ihtn(Enum):
    # elementary tasks
    navto_room3 = ElementaryTask(task_type.NAV_TO.value, destination=poi.room3.value, assign_to=[role_r1])
    pick_up_object  = ElementaryTask(task_type.PICK_UP.value, target=role_r1, assign_to=[role_r1])
    m_collect = Method(subtasks=[navto_room3, pick_up_object])

    # root task
    collect = AbstractTask(methods=[m_collect])

for enum_item in collection_ihtn:
    setattr(enum_item.value, 'name', enum_item.name)


@pytest.fixture
def ihtn_collect():
    return collection_ihtn.collect.value.clone()

@pytest.fixture
def r1():
    return role_r1

@pytest.fixture
def collection_robots():
    return robots

@pytest.fixture
def collection_robots_a_and_b():
    robots = [ enum_item.value for enum_item in [robot.a, robot.b]]
    return robots


######
# Container, and processes
########

container = Container()
# env desc
container[Map] = create_map()
routes_ed = container[RoutesEnvironmentDescriptor]

# skill desc
nav_sd = container[NavigationSkillDescriptor]
pick_up_sd = generic_skill_descriptor_constant_cost_factory('pick_up', 10)

# skill desc container singleton
sd_register = SkillDescriptorRegister( (task_type.NAV_TO.value, nav_sd), (task_type.PICK_UP.value, pick_up_sd))
container[SkillDescriptorRegister] = sd_register


# estimate manager
container[List[Worker]] = robots
em:EstimateManager = container[EstimateManager]
cfp: CoalitionFormationProcess = container[CoalitionFormationProcess]
######
# Robots
########

@pytest.fixture
def cf_process():
    return cfp

@pytest.fixture
def estimate_manager():
    return em

@pytest.fixture
def routes_envdesc():
    return routes_ed


###
# Execution
###
class OneTickSkill(SkillImplementation):
    task = None
    def on_load(self, task):
        self.tick_count = 0
        self.task = task
        print(task)

    def on_tick(self):
        if self.tick_count is 0:
            self.tick_count = 1
            return TickStatus(status=TickStatus.Type.IN_PROGRESS, task=self.task)
        else:
            return TickStatus(status=TickStatus.Type.SUCCESS_END, task=self.task)

    def on_complete(self):
        print(f'task completed')

collector_skill_library = SkillLibrary()
collector_skill_library.add(task_type.NAV_TO.value, OneTickSkill)
collector_skill_library.add(task_type.PICK_UP.value, OneTickSkill)


class MissionHandlerMock(MissionHandler):
    def start_mission(*params):
        pass

@pytest.fixture
def collection_mission():
    mission_context = MissionContext(global_plan = collection_ihtn.collect.value.clone())
    cfp.do_run(mission_context, robots, MissionHandlerMock())
    robot_b = robots[1] # robot B that is the fastest that have the skills
    cmission = {"mission": mission_context, 'robot': robot_b}
    return cmission


