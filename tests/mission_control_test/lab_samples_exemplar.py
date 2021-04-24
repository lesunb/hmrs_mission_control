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

class POI:
    room3 = 0

class Roles:
    nurse = 0
    lab_arm = 1
    r1 = 2

# concrete tasks
class ct:
    navto_room3 = ConcreteTask(TaskType.NAV_TO, destination=POI.room3, assign_to=Roles.r1)
    approach_nurse = ConcreteTask(TaskType.APPROACH_PERSON, target=Roles.nurse, assign_to=Roles.r1)
    authenticate_nurse = ConcreteTask(TaskType.AUTHENTICATE_PERSON, target=Roles.nurse, assign_to=Roles.r1)
    open_drawer = ConcreteTask(TaskType.OPEN_DRAWER, assign_to=Roles.r1)
    deposit = ConcreteTask(TaskType.DEPOSIT, assign_to = Roles.nurse)
    close_drawer = ConcreteTask(TaskType.CLOSE_DRAWER, assign_to=Roles.r1)
    navto_pharmacy = ConcreteTask(TaskType.NAV_TO, assign_to=Roles.r1)
    approach_arm = ConcreteTask(TaskType.APPROACH_ROBOT, target=Roles.lab_arm, assign_to=Roles.r1)
    open_drawer = ConcreteTask(TaskType.OPEN_DRAWER, assign_to=Roles.r1)
    pick_up_sample  = ConcreteTask(TaskType.PICK_UP, target=Roles.r1, assign_to=Roles.lab_arm)
    close_drawer = ConcreteTask(TaskType.CLOSE_DRAWER, assign_to=Roles.r1)


# methods and abstract tasks
m_deposit = Method(tasks = [ct.open_drawer, ct.deposit, ct.close_drawer])
deposit_sample_on_delivery_bot = AbstractTask(methods=[m_deposit])
m_retrieve = Method(tasks = [ct.approach_nurse, ct.authenticate_nurse, deposit_sample_on_delivery_bot])
retrive_sample = AbstractTask(methods=[m_retrieve])
m_unload = Method(tasks=[ct.open_drawer, ct.pick_up_sample, ct.close_drawer])
unload_sample = AbstractTask(methods=[m_unload])
m_mission = Method(tasks=[ct.navto_room3, retrive_sample, ct.navto_pharmacy, ct.approach_arm, unload_sample])

pickup_sample = AbstractTask(methods=[m_mission])

@pytest.fixture
def ihtn_pickup_sample():
    return pickup_sample