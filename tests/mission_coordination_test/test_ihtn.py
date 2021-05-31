from resources.world_lab_samples import *

from mission_control.mission.planning import distribute, count_elementary_tasks, flat_plan, check_tasks_names
from mission_control.mission.execution import eliminate_left_task

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
    assert check_tasks_names(flat_plan(distribution), ['close_drawer_lab', 'open_drawer_lab', 'send_message', 'wait_message'])

def test_distribute(ihtn_pickup_sample):
    distribution = distribute(ihtn_pickup_sample, r1)
    assert count_elementary_tasks(distribution) == 9


def test_eliminate_left_task_some_tasks():
    global_plan, lab_samples_ihtn =  pickup_ihtn(poi.ic_room_3.value)
    res_plan = global_plan.clone()
    initial_count = count_elementary_tasks(res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.navto_room.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.approach_nurse.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.authenticate_nurse.value, res_plan)

    assert  (initial_count - count_elementary_tasks(res_plan)) == 3
        

def test_eliminate_left_task_all_tasks():
    global_plan, lab_samples_ihtn =  pickup_ihtn(poi.ic_room_3.value)
    initial_count = count_elementary_tasks(global_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.navto_room.value, global_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.approach_nurse.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.authenticate_nurse.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.open_drawer_nurse.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.deposit.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.close_drawer_nurse.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.navto_lab.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.approach_arm.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.open_drawer_lab.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.pick_up_sample.value, res_plan)
    assert  (initial_count - count_elementary_tasks(res_plan)) == 10
    res_plan = eliminate_left_task(lab_samples_ihtn.close_drawer_lab.value, res_plan)
    assert res_plan is None
    

        
