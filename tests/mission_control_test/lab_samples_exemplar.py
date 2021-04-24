import pytest

from enum import Enum
from mission_control.mission.ihtn import Method, MethodOrdering, Task, ConcreteTask, AbstractTask


class TaskType(Enum):
    NAV_TO = 'navigation'
    APPROACH_PERSON = 'approach_person'
    AUTHENTICATE_PERSON = 'authenticate_person'
    OPEN_DRAWER = 'open_drawer'
    CLOSE_DRAWER = 'close_drawer'
    APPROACH_ROBOT = 'approach_robot'
    PICK_UP = 'pick_up'
    DEPOSIT = 'deposit'

class POI(Enum):
    room3 = 0

class Roles(Enum):
    nurse =  'nurse'
    lab_arm = 'lab_arm'
    r1 = 'r1'

# concrete tasks
class ct(Enum):
    navto_room3 = ConcreteTask(TaskType.NAV_TO, destination=POI.room3, assign_to=Roles.r1)
    approach_nurse = ConcreteTask(TaskType.APPROACH_PERSON, target=Roles.nurse, assign_to=Roles.r1)
    authenticate_nurse = ConcreteTask(TaskType.AUTHENTICATE_PERSON, target=Roles.nurse, assign_to=Roles.r1)
    open_drawer = ConcreteTask(TaskType.OPEN_DRAWER, assign_to=Roles.r1)
    deposit = ConcreteTask(TaskType.DEPOSIT, assign_to = Roles.nurse)
    close_drawer = ConcreteTask(TaskType.CLOSE_DRAWER, assign_to=Roles.r1)
    navto_pharmacy = ConcreteTask(TaskType.NAV_TO, assign_to=Roles.r1)
    approach_arm = ConcreteTask(TaskType.APPROACH_ROBOT, target=Roles.lab_arm, assign_to=Roles.r1)
    open_drawer_lab = ConcreteTask(TaskType.OPEN_DRAWER, assign_to=Roles.r1)
    pick_up_sample  = ConcreteTask(TaskType.PICK_UP, target=Roles.r1, assign_to=Roles.lab_arm)
    close_drawer_lab = ConcreteTask(TaskType.CLOSE_DRAWER, assign_to=Roles.r1)


    # methods and abstract tasks
    m_deposit = Method(tasks = [open_drawer, deposit, close_drawer])
    deposit_sample_on_delivery_bot = AbstractTask(methods=[m_deposit])
    m_retrieve = Method(tasks = [approach_nurse, authenticate_nurse, deposit_sample_on_delivery_bot])
    retrive_sample = AbstractTask(methods=[m_retrieve])
    m_unload = Method(tasks=[open_drawer_lab, pick_up_sample, close_drawer_lab])
    unload_sample = AbstractTask(methods=[m_unload])
    m_mission = Method(tasks=[navto_room3, retrive_sample, navto_pharmacy, approach_arm, unload_sample])

    pickup_sample = AbstractTask(methods=[m_mission])

def set_name(enum_item):
    setattr(enum_item.value, 'name', enum_item.name)

for item in ct:
    set_name(item)

@pytest.fixture
def ihtn_pickup_sample():
    return ct.pickup_sample.value