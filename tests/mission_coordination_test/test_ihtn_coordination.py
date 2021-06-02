from mission_control.mission.coordination import update_mission
from mission_control.mission.ihtn import TaskState, TaskStatus
from resources.world_lab_samples import *

def test_mark_elementary_as_concluded():
    pickup_sample, lab_samples_ihtn =  pickup_ihtn(poi.ic_room_3.value)
    
    task_state = TaskState(task=lab_samples_ihtn.navto_room.value, status=TaskStatus.SUCCESS_END)
    update_mission(pickup_sample, task_state)
    assert pickup_sample.selected_method.subtasks[0].state.is_status(TaskStatus.SUCCESS_END)


def test_mark_all_subtasks_as_concluded():
    pickup_sample, lab_samples_ihtn =  pickup_ihtn(poi.ic_room_3.value)
    
    tasks = [
        lab_samples_ihtn.open_drawer_nurse.value,
        lab_samples_ihtn.deposit.value,
        lab_samples_ihtn.close_drawer_nurse.value
    ]
    task_status_list = map(lambda t:TaskState(status=TaskStatus.SUCCESS_END, task=t), tasks)
    for ts in task_status_list:
        update_mission(pickup_sample, ts)
    
    # abstract parent task should be SUCCESS_END
    assert pickup_sample.selected_method.subtasks[1].state.is_status(TaskStatus.SUCCESS_END)

