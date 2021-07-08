from __init__ import *
from evaluation.experiment_gen_base.exec_sim import SimExec

from resources.world_lab_samples import cf_process, get_position_of_poi
from resources.world_lab_samples_trial import *

def test_exec_sim():
    # run in deeco env
    ########
    sim_exec = SimExec(cf_process)
    fetch_sample_trial.requests[0].task.attributes['max_time'] = 5*60

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

