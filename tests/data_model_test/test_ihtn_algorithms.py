
from mission_control.data_model import eliminate_left_task, count_elementary_tasks
from hospital_world.lab_samples_mission import pickup_ihtn, poi

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
    res_plan = eliminate_left_task(lab_samples_ihtn.open_drawer_for_nurse.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.deposit.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.close_drawer_nurse.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.navto_lab.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.approach_arm.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.open_drawer_lab.value, res_plan)
    res_plan = eliminate_left_task(lab_samples_ihtn.pick_up_sample.value, res_plan)
    assert  (initial_count - count_elementary_tasks(res_plan)) == 10
    res_plan = eliminate_left_task(lab_samples_ihtn.close_drawer_lab.value, res_plan)
    assert res_plan is None