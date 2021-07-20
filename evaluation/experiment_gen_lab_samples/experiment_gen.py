
import json
from pathlib import Path

from typing import List
from __init__ import *
from random import Random
from datetime import datetime

from mission_control.core import Request
from evaluation.experiment_gen_base.exec_sim import SimExec
from evaluation.experiment_gen_base.trial import Trial
from evaluation.experiment_gen_base.trial_design import draw_without_repetition, draw_with_repetition, total_combinations


from resources.world_lab_samples import task_type, all_skills, poi, routes_ed, near_ic_pc_rooms, cf_process, pickup_ihtn, get_position_of_poi

from evaluation.experiment_gen_lab_samples.baseline_plan import append_baseline_trial

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
    random = Random()
    random.seed(44)
    number_of_robots = 5
    number_of_nurses = 1
    
    # times in which a new request will appear in the trial
    request_times = [ 4000 ] # single request

    # selected levels
    #################

    # robot can have or not a secure drawer
    skills_levels = [
        all_skills, # all skills
        list(set(all_skills) - set([task_type.OPERATE_DRAWER])) # all skills but operate drawer
    ]
    
    # three random selections for each robot
    skills = [
        draw_with_repetition(skills_levels, number_of_robots, random),
        draw_with_repetition(skills_levels, number_of_robots, random),
        draw_with_repetition(skills_levels, number_of_robots, random)
    ]

    # three selections of positions for each robot
    locations = [ 
        draw_without_repetition(near_ic_pc_rooms, number_of_robots + number_of_nurses, random),
        draw_without_repetition(near_ic_pc_rooms, number_of_robots + number_of_nurses, random),
        draw_without_repetition(near_ic_pc_rooms, number_of_robots + number_of_nurses, random)
    ]

    # three selections of starting battery level for each robot
    # starting from 10 to 90
    battery_charges = [
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random),
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random),
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random),
    ]

    battery_discharge_rates = [
        draw_without_repetition([x * 0.00001 for x in range(10, 20)], number_of_robots, random),
        draw_without_repetition([x * 0.00001 for x in range(10, 20)], number_of_robots, random),
        draw_without_repetition([x * 0.00001 for x in range(10, 20)], number_of_robots, random),
    ]

    # constant for all robots
    avg_speed = [[0.15, 0.15, 0.15, 0.15, 0.15]]
    
    
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
    trials: List[Trial] = []
    requests = None
    baseline_trials = []
    trial_id = 1
    for trial_design in trial_designs:
        set_of_robot_factors = []
        code = trial_design.code
        factors = trial_design.factors_map

        for robot_id in range(0, number_of_robots):
            #each robot
            robot_facotrs = { 'id': robot_id }
            for factor_key, values_set in trial_design.items():
                # each factor
                robot_facotrs[factor_key] = values_set[robot_id]
            
            set_of_robot_factors.append(robot_facotrs)
        
        # trailing positions are the position of nurses
        nurse_locations = trial_design['location'][number_of_robots: number_of_robots + number_of_nurses]

        # generate a request for each time
        requests = []
        nurses = []
        nurses_locations = []

        # append approach trial
        for location, request in gen_requests(request_times, nurse_locations):
            requests.append(request)
            nurses.append({ 'position': get_position_of_poi(location), 'location': location.label})
            nurses_locations.append(location)
        planned_code = code + 'p' # at 'p', for _p_lanned variant
        trial = Trial(id=trial_id, code=planned_code, factors=factors,
            robots=set_of_robot_factors, 
            nurses= nurses,
            requests=requests)
        
        trials.append(trial)
        # append baseline trial
        baseline_code = code + 'b'
        append_baseline_trial(baseline_trials, id=trial_id, code=baseline_code, factors=factors, robots=set_of_robot_factors, 
            nurses_locations=nurses_locations, nurses=nurses, routes_ed=routes_ed, random=random)
        
        trial_id = trial_id + 1

    exp_id = exp_gen_id()
    with open(f'tmp/design_{exp_id}.json', 'w') as outfile:
        json.dump(code_map, outfile, indent=4, sort_keys=True)

    # dump baseline trials
    with open(f'tmp/experiment_baseline_trials_{exp_id}.json', 'w') as outfile:
        json.dump(baseline_trials, outfile, indent=4, sort_keys=True)

    # batch exec for trials
    planned_trials = []
    no_plan_trials = []
    for trial in trials:
        # run in deeco env
        ########
        sim_exec = get_sim_exec()
        final_state = sim_exec.run(trial, limit_ms=10000)
        # inspect end state
        print(final_state['missions'][0].occurances)
        # prep exec sim
        ####### 

        for robot in trial.robots:
            robot['position'] = get_position_of_poi(robot['location'])
            robot['location'] = robot['location'].label
            robot['skills'].sort()

        # delete non dict
        delattr(trial, 'requests')

        if any(final_state['local_plans']):
            planned_trials.append(trial.__dict__)
        else:
            no_plan_trials.append(trial.__dict__)
    
    # dump trials
    with open(f'tmp/experiment_no_plan_trials_{exp_id}.json', 'w') as outfile:
        json.dump(no_plan_trials, outfile, indent=4, sort_keys=True)



    trials = []
    trials.extend(planned_trials)
    trials.extend(baseline_trials)
    trials.sort(key=trial_key_to_sort)
    # finally, write the experiment gen to the final folder
    new_experiment_path = f'new_experiments/experiment_{exp_id}_run_1/step1_experiment_generation'
    path = Path(new_experiment_path)
    path.mkdir(parents=True, exist_ok=True)

    with open(f'{new_experiment_path}/design.json', 'w') as outfile:
        json.dump(code_map, outfile, indent=4, sort_keys=True)

    with open(f'{new_experiment_path}/trials.json', 'w') as outfile:
        json.dump(trials, outfile, indent=4, sort_keys=True)


def get_sim_exec():
    return SimExec(cf_process)



if __name__ == '__main__':
    main()
