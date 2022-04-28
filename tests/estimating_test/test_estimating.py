from mission_control.common_descriptors.navigation_sd import Move
from mission_control.estimating import EstimatingManager, create_context_gen
from mission_control.data_model import ElementaryTask
from mission_control.data_model.restrictions import worker_factory

from ..world_collector import *

task1 = ElementaryTask(type=task_type.NAV_TO.value, destination=poi.room3.value)
task2 = ElementaryTask(type=task_type.NAV_TO.value, destination=poi.room1.value)
task3 = ElementaryTask(type=task_type.NAV_TO.value, destination=poi.room3.value)

task_list = [task1, task2, task3]


worker1 = robots[1]

worker_factory(location = poi.sr.value, 
        capabilities=[
            Move(avg_speed = 15, u='m/s'),
            # power_source_battery( 
            #     { capacity:1000, u:'Ah'},
            #     { charge:900, u:'Ah'}, ),
        ],
        skills=[task_type.NAV_TO.value],
        # models=[
        #     c('constant_power_consumption', rate=300, u='Ah'),
        # ]
        )

task_context_gen = create_context_gen(worker1, task_list)
task_ctxs = list(task_context_gen)
last_ctx = task_ctxs[2]



def test_estimate_navigation_task_in_context(estimate_manager: EstimatingManager):
    estimate = estimate_manager.estimation_in_task_context(last_ctx)
    assert estimate is not None


def test_estimate(estimate_manager: EstimatingManager):
    bid = estimate_manager.estimation(worker1, task_list)
    assert bid.estimate.time > 5 and bid.estimate.time < 6