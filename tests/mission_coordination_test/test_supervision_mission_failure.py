

from mission_control.core import LocalMission
from mission_control.processes.supervision import SupervisionProcess
from mission_control.mission.coordination import update_mission
from mission_control.mission.ihtn import Task, TaskStatus, TaskState

from ..world_collector import *

def test_mark_local_mission_as_having_failures(collection_mission, collection_ihtn):
    mission: MissionContext = collection_mission['mission']
    
    # mark first task as concluded
    task_state = TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.FAILURE)

    class MySupervisionProcess(SupervisionProcess):
        def get_pending_updates(self, local_mission: LocalMission) -> List[TaskState]:
            return [task_state]
    
    my_sp = MySupervisionProcess(None)

    my_sp.run(mission)
    assert mission.local_missions[0].is_status(TaskStatus.FAILURE)
    

def test_can_repair_plan(collection_mission, collection_ihtn):
    mission: MissionContext = collection_mission['mission']
    
    # mark first task as concluded
    task_state = TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.FAILURE)

    class MySupervisionProcess(SupervisionProcess):
        def get_pending_updates(self, local_mission: LocalMission) -> List[TaskState]:
            return [task_state]
    
    my_sp = MySupervisionProcess(None)

    my_sp.run(mission)
    my_sp.run(mission)
    assert mission.local_missions[0].is_status(TaskStatus.FAILURE)
    

def test_waiting_repair():
    pass

def test_mission_repaired():
    pass

def test_reasign():
    pass

# def test_can_not_repair_plan(collection_mission):
#     mission: MissionContext = collection_mission['mission']

    