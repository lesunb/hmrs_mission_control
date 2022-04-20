
from mission_control.data_model.core import LocalMission, MissionState
from mission_control.data_model.ihtn import TaskState, TaskStatus
from mission_control.data_model.core import MissionContext
from mission_control.coordinator.supervision import SupervisionProcess

from ..world_collector import *

def test_local_mission_end_success_concluded(collection_mission, collection_ihtn):
    mission: MissionContext = collection_mission['mission']

    task_states = [TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.COMPLETED_WITH_SUC)]

    class MySupervisionProcess(SupervisionProcess):
        def get_last_state_updates(self, local_mission: LocalMission) -> List[TaskState]:
            return task_states
    
    my_sp = MySupervisionProcess(mission_handle = None, repair_planner_register=None)
    my_sp.do_run(mission)
    assert not mission.local_missions[0].is_status(TaskStatus.COMPLETED_WITH_SUC)

    task_states = [TaskState(task=collection_ihtn.pick_up_object.value, status=TaskStatus.COMPLETED_WITH_SUC)]
    my_sp.do_run(mission)
    
    assert mission.local_missions[0].is_status(TaskStatus.COMPLETED_WITH_SUC)


def test_global_mission_end_success_concluded(collection_mission, collection_ihtn):
    mission: MissionContext = collection_mission['mission']

    task_states = [TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.COMPLETED_WITH_SUC)]

    last_mission_state: MissionState = None

    class MySupervisionProcess(SupervisionProcess):
        def get_last_state_updates(self, local_mission: LocalMission) -> List[TaskState]:
            return task_states
        
        def report_mission_status(self, mission_context: MissionContext, mission_state: MissionState):
            nonlocal last_mission_state
            last_mission_state = mission_state

    my_sp = MySupervisionProcess(mission_handle = None, repair_planner_register=None)

    task_states = [TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.IN_PROGRESS)]
    my_sp.do_run(mission)
    assert mission.local_missions[0].worker # worker assigned
    assert pytest.approx(last_mission_state.remaining_time) == 11.87248
    
    task_states = [TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.COMPLETED_WITH_SUC)]
    my_sp.do_run(mission)
    assert pytest.approx(last_mission_state.remaining_time) == 10

    task_states = [TaskState(task=collection_ihtn.pick_up_object.value, status=TaskStatus.COMPLETED_WITH_SUC)]
    my_sp.do_run(mission)
    
    assert mission.local_missions[0].is_status(TaskStatus.COMPLETED_WITH_SUC)
    assert mission.global_plan.state.is_status(TaskStatus.COMPLETED_WITH_SUC)
    assert not mission.local_missions[0].worker # worker is now free
    assert last_mission_state.remaining_time == 0

# TODO
# def test_mission_cancelled():  
#     pass