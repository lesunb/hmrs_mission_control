from enum import Enum
from lagom import Container

from ..world_collector import *

from mission_control.core import POI, worker_factory
from mission_control.estimate.estimate import EstimateManager
from mission_control.estimate.core import create_context_gen, SkillDescriptorRegister
from mission_control.mission.ihtn import ElementaryTask

from mission_control.common_descriptors.routes_ed import RoutesEnvironmentDescriptor, Map
from mission_control.common_descriptors.navigation_sd import NavigationSkillDescriptor, Move

task1 = ElementaryTask(type=task_type.NAV_TO, destination=poi.room3.value)
task2 = ElementaryTask(type=task_type.NAV_TO, destination=poi.room1.value)
task3 = ElementaryTask(type=task_type.NAV_TO, destination=poi.room3.value)

task_list = [task1, task2, task3]


worker1 = robots[1]

worker_factory(location = poi.sr.value, 
        capabilities=[
            Move(avg_speed = 15, u='m/s'),
            # power_source_battery( 
            #     { capacity:1000, u:'Ah'},
            #     { charge:900, u:'Ah'}, ),
        ],
        skills=[task_type.NAV_TO],
        # models=[
        #     c('constant_power_consumption', rate=300, u='Ah'),
        # ]
        )

task_context_gen = create_context_gen(worker1, task_list)
task_ctxs = list(task_context_gen)
last_ctx = task_ctxs[2]


def test_estimate_navigation_task_in_context(estimate_manager):
    estimate = estimate_manager.estimate_task_in_context(last_ctx)
    assert estimate is not None


def test_estimate(estimate_manager):
    bid = estimate_manager.estimate(worker1, task_list)
    assert bid.estimate.time > 5 and bid.estimate.time < 6

def test_estimate_route(routes_envdesc):
    route = routes_envdesc.get(poi.room3.value, poi.room1.value)
    assert route.get_distance() > 3




# def test_estimate_no_route():
#     # TODO   
#     assert False

