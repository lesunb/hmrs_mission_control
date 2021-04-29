import pytest

from lagom import Container
from typing import List

from enum import Enum

from mission_control.core import Worker, worker_factory, POI
from mission_control.estimate.core import SkillDescriptorRegister
from mission_control.estimate.estimate import EstimateManager
from mission_control.managers.coalition_formation import CoalitionFormationManager
from mission_control.mission.ihtn import Method, MethodOrdering, Task, ElementaryTask, AbstractTask

from mission_control.estimate.commons.routes_ed import RoutesEnvironmentDescriptor, Map
from mission_control.estimate.commons.navigation_sd import NavigationSkillDescriptor, Move
from mission_control.estimate.commons.generic_constant_cost_sd import generic_skill_descriptor_constant_cost_factory

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

class roles(Enum):
    r1 = 'r1'

class robot(Enum):
    a = worker_factory(position = poi.sr, 
        capabilities=[
            Move(avg_speed = 10, u='m/s')
        ],
        skills=[task_type.NAV_TO, task_type.PICK_UP])
    b = worker_factory(position = poi.room1, 
        capabilities=[
            Move(avg_speed = 15, u='m/s')
        ],
        skills=[task_type.NAV_TO, task_type.PICK_UP])
    c = worker_factory(position = poi.room1, 
        capabilities=[
            Move(avg_speed = 20, u='m/s')
        ],
        skills=[task_type.NAV_TO])

for enum_item in robot:
    setattr(enum_item.value, 'name', enum_item.name)
robots = [ unit.value for unit in robot ]

# Defined as Enum so we can reference methods and tasks, and we can have references
# to names that we later on set on them with set_name()
class collection_ihtn(Enum):
    # elementary tasks
    navto_room3 = ElementaryTask(task_type.NAV_TO, destination=poi.room3, assign_to=[roles.r1])
    pick_up_object  = ElementaryTask(task_type.PICK_UP, target=roles.r1, assign_to=[roles.r1])
    m_collect = Method(subtasks=[navto_room3, pick_up_object])

    # root task
    collect = AbstractTask(methods=[m_collect])

for enum_item in collection_ihtn:
    setattr(enum_item.value, 'name', enum_item.name)


@pytest.fixture
def ihtn_collect():
    return collection_ihtn.collect.value

@pytest.fixture
def r1():
    return Roles.r1

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
container[Map] = Map(pois =[], segments=[])
routes_ed = container[RoutesEnvironmentDescriptor]

# skill desc
nav_sd = container[NavigationSkillDescriptor]
pick_up_sd = generic_skill_descriptor_constant_cost_factory('pick_up', 10)

# skill desc container singleton
sd_register = SkillDescriptorRegister( (task_type.NAV_TO, nav_sd), (task_type.PICK_UP, pick_up_sd))
container[SkillDescriptorRegister] = sd_register


# estimate manager
container[List[Worker]] = robots
em:EstimateManager = container[EstimateManager]
cfm: CoalitionFormationManager = container[CoalitionFormationManager]
######
# Robots
########

@pytest.fixture
def cf_manager():
    return cfm

