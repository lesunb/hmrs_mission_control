

from mission_control.core import LocalMission, MissionState
from mission_control.processes.supervision import SupervisionProcess
from mission_control.mission.ihtn import Assignment, TaskFailure, TaskStatus, TaskState

from ..world_collector import *

def test_non_recoverable_failures_in_mission(collection_mission, collection_ihtn, collector_mission_repair_register):
    mission: MissionContext = collection_mission['mission']
    # failure for which there is NO REPAIR in the collector_mission_repair_register
    task_state = TaskFailure(task=collection_ihtn.pick_up_object.value, failure_type='battery_low')

    last_mission_state: MissionState = None
    
    class MySupervisionProcess(SupervisionProcess):
        def get_last_state_updates(self, local_mission: LocalMission) -> List[TaskState]:
            return [task_state]
        
        def report_mission_status(self, mission_context: MissionContext, mission_state: MissionState):
            nonlocal last_mission_state
            last_mission_state = mission_state

    my_sp = MySupervisionProcess(mission_handle = None, repair_planner_register=collector_mission_repair_register)

    my_sp.do_run(mission)
    assert mission.local_missions[0].is_status(TaskStatus.FAILED)
    

def test_recoverable_by_reasignment_failures_in_mission(collection_mission, collection_ihtn, collector_mission_repair_register):
    mission: MissionContext = collection_mission['mission']
    
    # failure for wich THERE IS REPAIR in the collector_mission_repair_register
    task_state = TaskFailure(task=collection_ihtn.navto_room3.value, failure_type='battery_low')

    last_mission_state: MissionState = None
    
    class MySupervisionProcess(SupervisionProcess):
        def get_last_state_updates(self, local_mission: LocalMission) -> List[TaskState]:
            return [task_state]
        
        def report_mission_status(self, mission_context: MissionContext, mission_state: MissionState):
            nonlocal last_mission_state
            last_mission_state = mission_state

    my_sp = MySupervisionProcess(mission_handle = None, repair_planner_register=collector_mission_repair_register)

    my_sp.do_run(mission)
    assert mission.local_missions[0].is_status(TaskStatus.IN_PROGRESS)
    assert mission.local_missions[0].assignment_status is LocalMission.AssignmentStatus.NOT_ASSIGNED
    

# def test_can_repair_plan(collection_mission, collection_ihtn):
#     pass
    
# def test_waiting_repair():
#     pass

# def test_mission_repaired():
#     pass

# def test_reasign():
#     pass

# def test_can_not_repair_plan(collection_mission):
#     mission: MissionContext = collection_mission['mission']

    