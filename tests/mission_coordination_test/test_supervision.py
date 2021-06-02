
from mission_control.mission.ihtn import Task, TaskStatus, TaskState
from mission_control.mission.coordination import update_mission
from ..world_collector import *

from mission_control.processes.supervision import SupervisionProcess


def test_estimate_time_remaining_on_init(collection_mission):
    mission = collection_mission['mission']
    
    mission_status = SupervisionProcess.evaluate_mission_status(mission)
    
    assert pytest.approx(11.87248) == mission_status.time_remaining


def test_estimate_time_remaining_with_task_concluded(collection_mission):
    mission = collection_mission['mission']
    
    # mark first task as concluded
    task_status = TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.SUCCESS_END)
    update_mission(mission.global_plan, task_status)
    
    mission_status = SupervisionProcess.evaluate_mission_status(mission)

    assert pytest.approx(10) == mission_status.time_remaining

def test_estimate_time_remaining_with_task_in_progress(collection_mission):
    mission = collection_mission['mission']
    
    # mark first task as concluded
    task_status = TaskState(task=collection_ihtn.navto_room3.value, 
                             status=TaskStatus.IN_PROGRESS, progress=0.5)
    update_mission(mission.global_plan, task_status)
    
    mission_status = SupervisionProcess.evaluate_mission_status(mission)

    assert pytest.approx(10.93624) == mission_status.time_remaining


# def test_check_battery():
#     mission, robot = collection_mission['mission'], collection_mission['robot']
    
#     mission_status = SupervisionProcess.evaluate_mission_status(mission)
#     assert mission_status.time_remaining == 1000