import pytest

from enum import Enum
from mission_control.mission.ihtn import Method, MethodOrdering, Task, ElementaryTask, AbstractTask


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

# Defined as Enum so we can reference methods and tasks, and we can have references
# to names that we later on set on them with set_name()
class lab_samples_ihtn(Enum):
    # elementary tasks
    navto_room3 = ElementaryTask(TaskType.NAV_TO, destination=POI.room3, assign_to=[Roles.r1])
    approach_nurse = ElementaryTask(TaskType.APPROACH_PERSON, target=Roles.nurse, assign_to=[Roles.r1])
    authenticate_nurse = ElementaryTask(TaskType.AUTHENTICATE_PERSON, target=Roles.nurse, assign_to=[Roles.r1])
    open_drawer = ElementaryTask(TaskType.OPEN_DRAWER, assign_to=[Roles.r1])
    deposit = ElementaryTask(TaskType.DEPOSIT, assign_to = [Roles.nurse])
    close_drawer = ElementaryTask(TaskType.CLOSE_DRAWER, assign_to=[Roles.r1])
    navto_pharmacy = ElementaryTask(TaskType.NAV_TO, assign_to=[Roles.r1])
    approach_arm = ElementaryTask(TaskType.APPROACH_ROBOT, target=Roles.lab_arm, assign_to=[Roles.r1])
    open_drawer_lab = ElementaryTask(TaskType.OPEN_DRAWER, assign_to=[Roles.r1])
    pick_up_sample  = ElementaryTask(TaskType.PICK_UP, target=Roles.r1, assign_to=[Roles.lab_arm])
    close_drawer_lab = ElementaryTask(TaskType.CLOSE_DRAWER, assign_to=[Roles.r1])


    # methods and abstract tasks
    m_deposit = Method(subtasks = [open_drawer, deposit, close_drawer])
    deposit_sample_on_delivery_bot = AbstractTask(methods=[m_deposit])
    m_retrieve = Method(subtasks = [approach_nurse, authenticate_nurse, deposit_sample_on_delivery_bot])
    retrive_sample = AbstractTask(methods=[m_retrieve])
    m_unload = Method(subtasks=[open_drawer_lab, pick_up_sample, close_drawer_lab])
    unload_sample = AbstractTask(methods=[m_unload])
    m_mission = Method(subtasks=[navto_room3, retrive_sample, navto_pharmacy, approach_arm, unload_sample])

    # root task
    pickup_sample = AbstractTask(methods=[m_mission])

for enum_item in lab_samples_ihtn:
    setattr(enum_item.value, 'name', enum_item.name)


@pytest.fixture
def ihtn_pickup_sample():
    return lab_samples_ihtn.pickup_sample.value

@pytest.fixture
def ihtn_unload_sample():
    return lab_samples_ihtn.unload_sample.value

@pytest.fixture
def ihtn_navto_room3():
    return lab_samples_ihtn.navto_room3.value

@pytest.fixture
def ihtn_deposit():
    return lab_samples_ihtn.deposit.value

