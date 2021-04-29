
from ..world_collector import *

from mission_control.managers.coalition_formation import CoalitionFormationManager
from mission_control.core import Bid, Estimate, ImpossibleToEstimate, MissionContext

def test_create_mission_context(cf_manager: CoalitionFormationManager, ihtn_collect):
    m_context = cf_manager.create_mission_context(ihtn_collect)
    assert m_context is not None

def test_create_task_context(cf_manager: CoalitionFormationManager, ihtn_collect):
    individual_plans = cf_manager.individualize_plans(ihtn_collect)
    for individual_plan in individual_plans:
        assert individual_plan is not None


nav_to_room3 = collection_ihtn.navto_room3.value
pick_up_object = collection_ihtn.pick_up_object.value

def test_flat_plan(cf_manager: CoalitionFormationManager, ihtn_collect):
    obtained_task = cf_manager.flat_plan(ihtn_collect)
    diff =  set(obtained_task) ^ set([nav_to_room3, pick_up_object])
    assert not diff


def test_get_compatible_workers(cf_manager: CoalitionFormationManager, ihtn_collect, collection_robots_a_and_b):
    task_list = cf_manager.flat_plan(ihtn_collect)
    comp_workers = list(cf_manager.get_compatible_workers(task_list))
    # robot_a and robot_b have the skills, robot_c does not
    diff =  set(comp_workers) ^ set(collection_robots_a_and_b)
    assert not diff

def test_check_viable(cf_manager: CoalitionFormationManager, collection_robots):
    worker = collection_robots[0]
    bid = Bid(worker = worker, estimate = Estimate(time = 3, energy = 5))
    assert cf_manager.check_viable(bid) == True


def test_check_not_viable(cf_manager: CoalitionFormationManager, collection_robots):
    worker = collection_robots[0]
    bid = Bid(worker = worker, estimate = ImpossibleToEstimate(reason='no route'))
    assert cf_manager.check_viable(bid) == False


def test_sort_and_select_bids(cf_manager: CoalitionFormationManager, collection_robots):
    worker = collection_robots[0]
    bid1 = Bid(worker = worker, estimate = Estimate(time = 3, energy = 5))

    worker = collection_robots[1]
    bid2 = Bid(worker = worker, estimate = Estimate(time = 2, energy = 5))

    worker = collection_robots[1]
    bid3 = Bid(worker = worker, estimate = Estimate(time = 2.5, energy = 5))
    sorted_bids = cf_manager.rank_bids([bid1, bid2, bid3])
    assert sorted_bids[0] == bid2
    assert sorted_bids[1] == bid3
    assert sorted_bids[2] == bid1

    task = ElementaryTask('noop')
    sorted_bids
    plan_rank_map = {}
    plan_rank_map[task] = sorted_bids
    result = cf_manager.select_bids(plan_rank_map)
    assert result[task] == sorted_bids[0]




