

from mission_control.coordination import SupervisionProcess
from mission_control.coordination.update_mission import \
    update_estimates_with_progress
from mission_control.data_model import TaskState, TaskStatus

from ..world_collector import *


def test_estimate_time_remaining_on_init(collection_mission):
    mission = collection_mission['mission']
    
    mission_status = SupervisionProcess.evaluate_mission_state(mission)
    
    assert pytest.approx(11.87248) == mission_status.remaining_time


def test_estimate_time_remaining_with_task_concluded(collection_mission, collection_ihtn):
    mission = collection_mission['mission']
    
    # mark first task as concluded
    task_state = TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.COMPLETED_WITH_SUC)
    update_estimates_with_progress(mission.global_plan, task_state)
    
    mission_status = SupervisionProcess.evaluate_mission_state(mission)

    assert pytest.approx(10) == mission_status.remaining_time

def test_estimate_time_remaining_with_task_in_progress(collection_mission, collection_ihtn):
    mission = collection_mission['mission']
    
    # mark first task as concluded
    task_state = TaskState(task=collection_ihtn.navto_room3.value, 
                             status=TaskStatus.IN_PROGRESS, progress=0.5)
    update_estimates_with_progress(mission.global_plan, task_state)
    
    mission_status = SupervisionProcess.evaluate_mission_state(mission)

    assert pytest.approx(10.93624) == mission_status.remaining_time


# def test_check_battery():
#     mission, robot = collection_mission['mission'], collection_mission['robot']
    
#     mission_status = SupervisionProcess.evaluate_mission_state(mission)
#     assert mission_status.remaining_time == 1000
