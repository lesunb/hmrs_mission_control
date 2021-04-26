import pytest

from enum import Enum
from mission_control.mission.ihtn import Method, MethodOrdering, Task, ElementaryTask, AbstractTask

from mission_control.managers.coalition_formation import CoalitionFormationManager
from mission_control.core import Worker

class TaskType(Enum):
    NAV_TO = 'navigation'
    PICK_UP = 'pick_up'

class POI(Enum):
    room3 = 0

class Roles(Enum):
    r1 = 'r1'

class collection_units(Enum):
    robot_a = Worker(skills=[TaskType.NAV_TO, TaskType.PICK_UP])
    robot_b = Worker(skills=[TaskType.NAV_TO, TaskType.PICK_UP])
    robot_c = Worker(skills=[TaskType.NAV_TO])

for enum_item in collection_units:
    setattr(enum_item.value, 'name', enum_item.name)

# Defined as Enum so we can reference methods and tasks, and we can have references
# to names that we later on set on them with set_name()
class ithn_collection_parts(Enum):
    # elementary tasks
    navto_room3 = ElementaryTask(TaskType.NAV_TO, destination=POI.room3, assign_to=[Roles.r1])
    pick_up_object  = ElementaryTask(TaskType.PICK_UP, target=Roles.r1, assign_to=[Roles.r1])
    m_collect = Method(subtasks=[navto_room3, pick_up_object])

    # root task
    collect = AbstractTask(methods=[m_collect])

for enum_item in ithn_collection_parts:
    setattr(enum_item.value, 'name', enum_item.name)


@pytest.fixture
def ihtn_collect():
    return ithn_collection_parts.collect.value

@pytest.fixture
def cf_manager():
    units = [ unit.value for unit in collection_units ]
    _cf_manager = CoalitionFormationManager(units = units)
    return _cf_manager


@pytest.fixture
def r1():
    return Roles.r1

@pytest.fixture
def collection_robots():
    units = [ unit.value for unit in collection_units ]
    return units

@pytest.fixture
def collection_robots_a_and_b():
    units = [ unit.value for unit in [collection_units.robot_a, collection_units.robot_b ]]
    return units
