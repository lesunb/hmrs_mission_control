from ..world_lab_samples import *

from mission_control.mission.planning import distribute, count_elementary_tasks, flat_plan, check_tasks_names


def eq(obja, objb, *fields):
    if type(obja) == type(objb):
        for field in fields:
            if (getattr(obja, field) != getattr(objb, field)):
                return False
        return True
    else:
        return False

def test_count_elementary_tasks(ihtn_pickup_sample):
    count = count_elementary_tasks(ihtn_pickup_sample)
    assert count == 11

def test_abstract_task_assign_to(ihtn_pickup_sample):
    obtained = ihtn_pickup_sample.assign_to
    expected = [Roles.r1, Roles.lab_arm, Roles.nurse]
    diff =  set(obtained) ^ set(expected)
    assert not diff

def test_distribute_single_not_assigned_task(ihtn_deposit):
    distribution = distribute(ihtn_deposit, Roles.r1)
    assert distribution is None

def test_distribute_single_assigned_task(ihtn_navto_room3):
    distribution = distribute(ihtn_navto_room3, Roles.r1)
    assert eq(distribution, ihtn_navto_room3, 'name', 'destination')


def test_sync_between_two_agents(ihtn_unload_sample):
     distribution = distribute(ihtn_unload_sample, Roles.r1)
     assert count_elementary_tasks(distribution) == 2
     assert check_tasks_names(flat_plan(distribution), ['close_drawer_lab', 'open_drawer_lab', 'send_message', 'wait_message'])

def test_distribute(ihtn_pickup_sample):
    distribution = distribute(ihtn_pickup_sample, Roles.r1)
    assert count_elementary_tasks(distribution) == 9
