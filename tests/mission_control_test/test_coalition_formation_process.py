

from ..world_collector import *

from mission_control.mission.ihtn import Task

def test_coalition_formation_process(cf_manager: CoalitionFormationManager, ihtn_collect: Task, collection_robots):
    result = cf_manager.create_coalition(ihtn_collect)
    expected_robot = collection_robots[1] # robot B that is the fastest that have the skills
    for individual_plan, selected_bid in result.selected_bids.items():
        # TODO change the result for a map role -> (plan, result) to make it easier to reference
        # for to take the only individual plan
        assert selected_bid.worker == expected_robot
    
    
