

import pytest
from mission_control.processes.supervision import SupervisionProcess
from mission_control.mission.coordination import update_mission
from mission_control.mission.ihtn import Task, TaskStatus, TaskState

from tests.world_collector import collection_ihtn
from mission_control.processes.sequencing import TaskStatus

from ..world_collector import *

def test_can_repair_plan(collection_mission):
    mission: MissionContext = collection_mission['mission']
    
    # mark first task as concluded
    task_state = TaskStatus(task=collection_ihtn.navto_room3.value, status=TaskStatus.FATAL_FAILURE)
    update_mission(mission.global_plan, task_state)
    
    mission_status = SupervisionProcess.evaluate_mission_status(mission)

    

    assert pytest.approx(10) == mission_status.time_remaining

# def test_can_not_repair_plan(collection_mission):
#     mission: MissionContext = collection_mission['mission']

    