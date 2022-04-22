from mission_control.coordination.planning import check_tasks_names, distribute
from mission_control.data_model import count_elementary_tasks, flat_plan
from resources.world_lab_samples import *


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
    expected = [r1, lab_arm, nurse]
    diff =  set(obtained) ^ set(expected)
    assert not diff

def test_distribute_single_not_assigned_task(ihtn_deposit):
    distribution = distribute(ihtn_deposit, r1)
    assert distribution is None

def test_distribute_single_assigned_task(ihtn_navto_room3):
    distribution = distribute(ihtn_navto_room3, r1)
    assert eq(distribution, ihtn_navto_room3, 'name', 'destination')


def test_sync_between_two_agents(ihtn_unload_sample):
    global_plan = ihtn_unload_sample.clone()
    distribution = distribute(global_plan, r1)
    assert count_elementary_tasks(distribution) == 2
    plan = flat_plan(distribution)
    assert check_tasks_names(plan, [
        'open_drawer_lab', 'notify_lab_arm_of_open_drawer_lab_completed',
        'wait_lab_arm_to_complete_pick_up_sample', 'close_drawer_lab'])

def test_distribute(ihtn_pickup_sample):
    distribution = distribute(ihtn_pickup_sample, r1)
    assert count_elementary_tasks(distribution) == 9
    

