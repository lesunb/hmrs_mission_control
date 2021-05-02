

from ..world_collector import *

from mission_control.mission.ihtn import Task
from mission_control.core import MissionContext

def test_coalition_formation_process(cf_manager: CoalitionFormationProcess, ihtn_collect: Task, collection_robots):
    mission_context = MissionContext(global_plan = ihtn_collect)
    cf_manager.do_run(mission_context, collection_robots)
    expected_robot = collection_robots[1] # robot B that is the fastest that have the skills
    assert mission_context.local_missions[0].worker == expected_robot
    assert mission_context.status == MissionContext.Status.DISTRIBUTING_TASKS
    
