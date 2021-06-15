
from mission_control.core import LocalMission
from mission_control.mission.ihtn import TaskState, TaskStatus
from mission_control.core import MissionContext
from mission_control.processes.supervision import SupervisionProcess

from ..world_collector import *

def test_local_mission_end_success_concluded(collection_mission, collection_ihtn):
    mission: MissionContext = collection_mission['mission']

    task_states = [TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.SUCCESS_ENDED)]

    class MySupervisionProcess(SupervisionProcess):
        def get_pending_updates(self, local_mission: LocalMission) -> List[TaskState]:
            return task_states
    
    my_sp = MySupervisionProcess(None)
    my_sp.run(mission)
    assert not mission.local_missions[0].is_status(TaskStatus.SUCCESS_ENDED)

    task_states = [TaskState(task=collection_ihtn.pick_up_object.value, status=TaskStatus.SUCCESS_ENDED)]
    my_sp.run(mission)
    
    assert mission.local_missions[0].is_status(TaskStatus.SUCCESS_ENDED)


def test_global_mission_end_success_concluded(collection_mission, collection_ihtn):
    mission: MissionContext = collection_mission['mission']

    task_states = [TaskState(task=collection_ihtn.navto_room3.value, status=TaskStatus.SUCCESS_ENDED)]

    class MySupervisionProcess(SupervisionProcess):
        def get_pending_updates(self, local_mission: LocalMission) -> List[TaskState]:
            return task_states
    
    my_sp = MySupervisionProcess(None)
    my_sp.run(mission)


    task_states = [TaskState(task=collection_ihtn.pick_up_object.value, status=TaskStatus.SUCCESS_ENDED)]
    my_sp.run(mission)
    
    assert mission.global_plan.state.is_status(TaskStatus.SUCCESS_ENDED)
    assert mission.local_missions[0].is_status(TaskStatus.SUCCESS_ENDED)

def test_mission_cancelled():
    
    pass