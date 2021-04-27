

from .collector_world import *

from mission_control.estimate.estimate import EstimateManager
from mission_control.core import POI, Worker
from mission_control.mission.ihtn import ElementaryTask

sr_poi = POI('storage_room')
room1_poi = POI('room1')
room3_poi = POI('room3')
task1 = ElementaryTask(type='navigate', destination=room3_poi)
task2 = ElementaryTask(type='navigate', destination=room1_poi)
task3 = ElementaryTask(type='simple_action')
task4 = ElementaryTask(type='navigate', destination=room3_poi)
task_list = [task1, task2, task3, task4]

unit = Worker(position = sr_poi)

# def test_get_compatible_units(cf_manager: CoalitionFormationManager, ihtn_collect, collection_robots_a_and_b):
#     robot_a = collection_robots_a_and_b[0]
#     # mock a path between robot_a and room3 with distance 100
#     # robot_a avg_speed

#     bid  = cf_manager.estimate(robot_a, task_list)

em = EstimateManager()

def test_create_task_context():
    task_context_gen = em.create_context_gen(unit, task_list)
    estimates = []
    task_ctxs = list(task_context_gen)
    last_ctx = task_ctxs[3]
    assert last_ctx.get('origin') == room1_poi

def test_estimate_navigation_task_in_context():
    assert False


def test_estimate():
    assert False


def test_estimate_no_route():
    assert False
