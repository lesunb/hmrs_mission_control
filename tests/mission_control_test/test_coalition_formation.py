
from .collector_world import *

from mission_control.managers.coalition_formation import CoalitionFormationManager

def test_create_mission_context(cf_manager: CoalitionFormationManager, ihtn_collect):
    m_context = cf_manager.create_mission_context(ihtn_collect)
    assert m_context is not None

def test_create_task_context(cf_manager: CoalitionFormationManager, ihtn_collect):
    individual_plans = cf_manager.individualize_plans(ihtn_collect)
    for individual_plan in individual_plans:
        assert individual_plan is not None


def test_flat_plan(cf_manager: CoalitionFormationManager, ihtn_collect):
    obtained_task = cf_manager.flat_plan(ihtn_collect)
    diff =  set(obtained_task) ^ set([ithn_collection_parts.navto_room3.value, ithn_collection_parts.pick_up_object.value])
    assert not diff


def test_get_compatible_units(cf_manager: CoalitionFormationManager, ihtn_collect, collection_robots_a_and_b):
    task_list = cf_manager.flat_plan(ihtn_collect)
    comp_units = list(cf_manager.get_compatible_units(task_list))
    # robot_a and robot_b have the skills, robot_c does not
    diff =  set(comp_units) ^ set(collection_robots_a_and_b)
    assert not diff


