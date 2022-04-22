
from mission_control.data_model.restrictions import BatteryTimeConstantDischarge
from ..world_collector import *
from mission_control.coordination.core import create_context_gen

task1 = ElementaryTask(type=task_type.NAV_TO.value, destination=poi.room3.value)
task2 = ElementaryTask(type=task_type.NAV_TO.value, destination=poi.room1.value)
task3 = ElementaryTask(type=task_type.NAV_TO.value, destination=poi.room3.value)

task_list = [task1, task2, task3]

worker1 = Worker(location = poi.sr.value, 
        capabilities=[
            Move(avg_speed = 15, u='m/s')
        ],
        skills=[task_type.NAV_TO.value],
        resources=[
           BatteryTimeConstantDischarge(
                battery=Battery(capacity=1, charge=1),
                discharge_rate=0.0003,
                minimum_useful_level=0.05)
        ])

task_context_gen = create_context_gen(worker1, task_list)
task_ctxs = list(task_context_gen)
last_ctx = task_ctxs[2]



def test_estimate(estimate_manager: estimate_manager):
    bid = estimate_manager.estimation(worker1, task_list)
    assert bid.estimate.energy == pytest.approx(0.0016847348)

