

from ..world_collector import *

from mission_control.data_model.ihtn import Task
from mission_control.data_model.restrictions import MissionContext, MissionStatus

def test_coalition_formation_process(cf_process: CoalitionFormationProcess, ihtn_collect: Task, collection_robots):
    mission_context = MissionContext(request_id=0, global_plan = ihtn_collect)
    cf_process.do_run(mission_context, collection_robots, MissionHandlerMock())
    expected_robot = collection_robots[1] # robot B that is the fastest that have the skills
    assert mission_context.local_missions[0].worker == expected_robot
    assert mission_context.status == MissionStatus.IN_PROGRESS
    
