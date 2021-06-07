from resources.world_lab_samples import task_type, all_skills, near_ic_pc_rooms, cf_process, pickup_ihtn, get_position_of_poi
import json
from __init__ import *
from random import Random

from mission_control.core import BatteryTimeConstantDischarge, Request
from evaluation.framework.exec_sim import SimExec
from evaluation.framework.trial import Trial

from resources.world_lab_samples_trial import *

def test_exec_sim():
    # run in deeco env
    ########
    sim_exec = SimExec(cf_process)
    final_state = sim_exec.run(fetch_sample_trial, limit_ms=10000)
    # inspect end state
    print(final_state['missions'][0].occurances)
    # prep exec sim
    ####### 

    for robot in fetch_sample_trial.robots:
        robot['position'] = get_position_of_poi(robot['location'])
        robot['location'] = robot['location'].label
        robot['skills'].sort()


    # delete non dict
    delattr(fetch_sample_trial, 'requests')

    assert any(final_state['local_plans'])

