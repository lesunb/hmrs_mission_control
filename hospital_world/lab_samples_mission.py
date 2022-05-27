from copy import deepcopy
import pytest
from enum import Enum

from mission_control.data_model import Method, ElementaryTask, AbstractTask
from mission_control.data_model import Role

from hospital_world.bindings import poi, task_type

nurse =  Role('nurse', type=Role.Type.NOT_MANAGED)
lab_arm = Role('lab_arm', type=Role.Type.NOT_MANAGED)
r1 = Role('r1')

def pickup_ihtn(pickup_location):
    class lab_samples_ihtn(Enum):
        # elementary tasks
        navto_room = ElementaryTask(task_type.NAV_TO, destination=pickup_location, assign_to=[r1])
        approach_nurse = ElementaryTask(task_type.APPROACH_PERSON, target=nurse, assign_to=[r1])
        authenticate_nurse = ElementaryTask(task_type.AUTHENTICATE_PERSON, target=nurse, assign_to=[r1])
        open_drawer_for_nurse = ElementaryTask(task_type.OPERATE_DRAWER, action='open', assign_to=[r1])
        deposit = ElementaryTask(task_type.DEPOSIT, assign_to = [nurse])
        close_drawer_nurse = ElementaryTask(task_type.OPERATE_DRAWER, action='close', assign_to=[r1])
        navto_lab = ElementaryTask(task_type.NAV_TO, destination=poi.laboratory.value, assign_to=[r1])
        approach_arm = ElementaryTask(task_type.APPROACH_ROBOT, target=lab_arm, assign_to=[r1])
        open_drawer_lab = ElementaryTask(task_type.OPERATE_DRAWER, action='open', assign_to=[r1])
        pick_up_sample  = ElementaryTask(task_type.PICK_UP, target=r1, assign_to=[lab_arm])
        close_drawer_lab = ElementaryTask(task_type.OPERATE_DRAWER, action='close', assign_to=[r1])

        # methods and abstract tasks
        m_deposit = Method(subtasks = [open_drawer_for_nurse, deposit, close_drawer_nurse])
        deposit_sample_on_delivery_bot = AbstractTask(methods=[m_deposit])
        m_retrieve = Method(subtasks = [approach_nurse, authenticate_nurse, deposit_sample_on_delivery_bot])
        retrive_sample = AbstractTask(methods=[m_retrieve])
        m_unload = Method(subtasks=[open_drawer_lab, pick_up_sample, close_drawer_lab])
        unload_sample = AbstractTask(methods=[m_unload])
        m_mission = Method(subtasks=[navto_room, retrive_sample, navto_lab, approach_arm, unload_sample])

        # root task
        pickup_sample = AbstractTask(methods=[m_mission])
        
    for enum_item in lab_samples_ihtn:
        setattr(enum_item.value, 'name', enum_item.name)

    return (lab_samples_ihtn.pickup_sample.value.clone(), deepcopy(lab_samples_ihtn))


# pickup_sample, lab_samples_ihtn =  pickup_ihtn(poi.ic_room_3.value)

@pytest.fixture
def ihtn_pickup_sample():
    pickup_sample, _ =  pickup_ihtn(poi.ic_room_3.value)
    return pickup_sample

@pytest.fixture
def ihtn_unload_sample():
    _, lab_samples_ihtn =  pickup_ihtn(poi.ic_room_3.value)
    return lab_samples_ihtn.unload_sample.value.clone()

@pytest.fixture
def ihtn_navto_room3():
    _, lab_samples_ihtn =  pickup_ihtn(poi.ic_room_3.value)
    return lab_samples_ihtn.navto_room.value

@pytest.fixture
def ihtn_deposit():
    _, lab_samples_ihtn =  pickup_ihtn(poi.ic_room_3.value)
    return lab_samples_ihtn.deposit.value
