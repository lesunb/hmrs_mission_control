
import json
from pathlib import Path

from typing import List
from __init__ import *
from random import Random
from datetime import datetime

from utils.logger import LogDir
from utils.to_string import obj_to_string

from mission_control.core import Request
from evaluation.experiment_gen_base.exec_sim import SimExec
from evaluation.experiment_gen_base.scenario import Scenario
from evaluation.experiment_gen_base.trial_design import draw_without_repetition, draw_from_distribution, selection, total_combinations
from mission_control.core import POI, Role

from verification import verify_trials
#from resources.world_lab_samples import task_type, carry_robot_skills, routes_ed, near_ic_pc_rooms, pickup_ihtn, get_position_of_poi, container
from resources.world_food_logistics import task_type, carry_robot_skills, routes_ed, near_ic_pc_rooms, pickup_ihtn, get_position_of_poi, container
from resources.ithn_from_json import ihtn_from_json

from evaluation.experiment_gen_lab_samples.baseline_plan import append_baseline_trial
from collections import namedtuple


# def randomly_gen_requests(times, locations, rand):
#     selected_locations = draw_without_repetition(locations, len(times), rand)
#     for time, location in zip(times, selected_locations):
#         task, _ = pickup_ihtn(location)
#         yield location, Request(task=task, timestamp=time)
#     return

def gen_requests(times, locations):
    for time, location in zip(times, locations):
        task, _ = pickup_ihtn(location)
        yield location, Request(task=task, timestamp=time)
    return

def gen_requests2(times, locations):
    print(times)
    print(locations)
    for time, location in zip(times, locations):
        task = ihtn_from_json("ihtn_flp.json")
        print(task)
        yield location, Request(task=task, timestamp=time)
    return

def simp_factors_map(map):
    return map


def exp_gen_id():
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    print("Current Time =", current_time)
    return current_time

def trial_key_to_sort(trial):
    id_str = '{:02d}'.format(trial['id'])
    return f'{id_str}_{trial["code"]}'

def main():
    exp_id = exp_gen_id()
    new_experiment_path = f'mutrose/flp/experiment_{exp_id}'
    path = Path(new_experiment_path + '/tmp')
    path.mkdir(parents=True, exist_ok=True)
    LogDir.default_path = new_experiment_path + '/logs'


    random = Random()
    random.seed(42)
    number_of_robots = 2
    number_of_patients = 1
    
    # times in which a new request will appear in the trial
    request_times = [ 4000 ] # single request

    # selected levels
    #################

    # robot can have or not a secure drawer
    skills_levels = [
        carry_robot_skills, # all skills
        list(set(carry_robot_skills)) # all skills but operate drawer
    ]

    # constant for all robots
    avg_speed = [[0.15]*number_of_robots]

    # three selections of starting battery level for each robot
    # starting from 10 to 90
    battery_charges = [
        draw_from_distribution('betavariate', alpha=2, beta=2, number_of_draws=number_of_robots, rand=random),
        draw_from_distribution('betavariate', alpha=2, beta=2, number_of_draws=number_of_robots, rand=random),
        draw_from_distribution('betavariate', alpha=2, beta=2, number_of_draws=number_of_robots, rand=random),
    ]

    battery_discharge_rates = [
        draw_without_repetition([x * 0.00002 for x in range(10, 40)], number_of_robots, random),
        draw_without_repetition([x * 0.00002 for x in range(10, 40)], number_of_robots, random),
        draw_without_repetition([x * 0.00002 for x in range(10, 40)], number_of_robots, random),
    ]
        
    # three random selections for each robot
    skills = [
        [ selection(carry_robot_skills, 0.94, random) for x in range(0, number_of_robots) ],
        [ selection(carry_robot_skills, 0.94, random) for x in range(0, number_of_robots) ],
        [ selection(carry_robot_skills, 0.94, random) for x in range(0, number_of_robots) ],
    ]

    # three selections of positions for each robot
    locations = [ 
        [POI("PC Room 5"), POI("PC Room 2"), POI("PC Room 4")],
        [POI("PC Room 3"), POI("PC Room 2"), POI("PC Room 4")],
        [POI("PC Room 1"), POI("PC Room 2"), POI("PC Room 4")],
    ]

    # Design - total combination of robot factors
    ######

    factors_levels_list = [
        ('avg_speed', avg_speed),
        ('battery_charge', battery_charges),
        ('battery_discharge_rate', battery_discharge_rates),
        ('skills', skills),
        ('location', locations)
    ]

    trial_designs, code_map = total_combinations(factors_levels_list)

    # set of requests
    scenarios: List[Scenario] = []
    requests = None
    baseline_trials = []
    scenario_id = 1
    for trial_design in trial_designs:
        set_of_robot_factors = []
        code = trial_design.code
        factors = trial_design.factors_map

        for robot_index in range(0, number_of_robots):
            #each robot
            robot_facotrs = { 'id': (robot_index + 1), 'name': f'r{(robot_index + 1)}'}
            for factor_key, values_set in trial_design.items():
                # each factor
                robot_facotrs[factor_key] = values_set[robot_index]
            
            set_of_robot_factors.append(robot_facotrs)
        
        # trailing positions are the position of patients
        patient_locations = trial_design['location'][number_of_robots: number_of_robots + number_of_patients]

        # generate a request for each time
        requests = []
        patients = []
        patients_locations = []
        for location, request in gen_requests2(request_times, patient_locations):
            requests.append(request)
            patients.append({ 'position': get_position_of_poi(location), 'location': location.label})
            patients_locations.append(location)

        ##
        # append baseline trial
        ##
        baseline_code = code + 'b'
        append_baseline_trial(baseline_trials, id=scenario_id, code=baseline_code, factors=factors, robots=set_of_robot_factors, 
            nurses_locations=patients_locations, nurses=patients, routes_ed=routes_ed, random=random)
        

        ##
        # append approach trial
        ##
        planned_code = code + 'p' # at 'p', for _p_lanned variant
        scenario = Scenario(id=scenario_id, code=planned_code, factors=factors,
            robots=set_of_robot_factors, 
            nurses= patients,
            requests=requests)
        
        scenarios.append(scenario)
        scenario_id += 1

    dump_scenarios(scenarios, f'{new_experiment_path}/scenarios.json')

    with open(f'{new_experiment_path}/factors_code.json', 'w') as outfile:
        json.dump(code_map, outfile, indent=4, sort_keys=True)



    # dump baseline trials
    with open(f'{new_experiment_path}/tmp/experiment_baseline_trials_{exp_id}.json', 'w') as outfile:
        json.dump(baseline_trials, outfile, indent=4, sort_keys=True)

    # batch exec for planned scenarios
    planned_trials = []
    no_plan_trials = []
    for scenario in scenarios:
        # run in deeco env
        sim_exec = get_sim_exec()
        final_state = sim_exec.run(scenario, limit_ms=10000)
        # inspect end state
        print(final_state['missions'][0].occurances)
        for robot in scenario.robots:
            robot['position'] = get_position_of_poi(robot['location'])
            robot['location'] = robot['location'].label
            robot['skills'].sort()

        # delete non dict before writing to json
        delattr(scenario, 'requests')

        if any(final_state['local_plans']):
            planned_trials.append(scenario.__dict__)
        else:
            no_plan_trials.append(scenario.__dict__)
    
    # dump no planned trials for debug (ideally it is empty)
    if no_plan_trials:
        with open(f'{new_experiment_path}/no_plan_trials.json', 'w') as outfile:
            json.dump(no_plan_trials, outfile, indent=4, sort_keys=True)

    trials = []
    trials.extend(planned_trials)
    trials.extend(baseline_trials)
    trials.sort(key=trial_key_to_sort)
    # finally, write the experiment gen to the final folder

    with open(f'{new_experiment_path}/design.json', 'w') as outfile:
        json.dump(code_map, outfile, indent=4, sort_keys=True)

    with open(f'{new_experiment_path}/trials.json', 'w') as outfile:
        json.dump(trials, outfile, indent=4, sort_keys=True)

    '''verification_of_plans = verify_trials(trial_designs, scenarios)
    with open(f'{new_experiment_path}/verification.json', 'w') as outfile:
        json.dump(verification_of_plans, outfile, indent=4, sort_keys=True)'''

def get_sim_exec():
    return SimExec(container)


def repack(objiter, repacking_tupels):
    new = {}
    for key, value in objiter:
        _, fnc = next(filter(lambda item: item[0] == key, repacking_tupels), (None, None))
        new[key] = fnc(value) if fnc else value
    return new

def dump_scenarios(scenarios, path):
    noop = lambda x: x
    
    def repack_robots(robot):
        return repack(robot.items(),
            [('location', lambda location: location.label )])

    def scenrio_to_dump(scenario: Scenario):
        return repack(scenario.__dict__.items(),[ 
            ('patient', lambda patients: list(map( lambda patient: patient.location))),
            ('requests', 
                lambda requests: list(map( 
                        lambda request: { 
                            'timestamp': request.timestamp, 
                            'task': request.task.name }, requests            ) 
            )),
            ('robots', lambda robots: list(map(repack_robots, robots )))
        ])

    sceratios_to_dump = list(map(scenrio_to_dump, scenarios))
    with open(path, 'w') as outfile:
        json.dump(sceratios_to_dump, outfile, indent=4, sort_keys=True)




if __name__ == '__main__':
    main()
