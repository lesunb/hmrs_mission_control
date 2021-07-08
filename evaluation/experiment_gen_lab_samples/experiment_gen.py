
import json
from typing import List
from __init__ import *
from random import Random

from mission_control.core import Request
from evaluation.experiment_gen_base.exec_sim import SimExec
from evaluation.experiment_gen_base.trial import Trial
from evaluation.experiment_gen_base.trial_design import total_combinations, draw_without_repetition, draw_with_repetition

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

def main():
    random = Random()
    random.seed(42)
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

    factors_combinatios = total_combinations({
        'skills': skills,
        'location': locations,
        'battery_charge': battery_charges,
        'battery_discharge_rate': battery_discharge_rates,
        'avg_speed': avg_speed
    })

    # set of requests    
    trial_id = 0
    trials = []
    requests = None
    baseline_trials = []
    for trial_robots_factors in factors_combinatios:
        set_of_robot_factors = []
        for robot_id in range(0, number_of_robots):
            #each robot
            robot_facotrs = { 'id': robot_id }
            for key, values_set in trial_robots_factors.items():
                # each factor
                robot_facotrs[key] = values_set[robot_id]
            
            set_of_robot_factors.append(robot_facotrs)
        
        # trailing positions are the position of nurses
        nurse_locations = trial_robots_factors['location'][number_of_robots: number_of_robots + number_of_nurses]

        # generate a request for each time
        requests = []
        nurses = []
        nurses_locations = []
        for location, request in gen_requests(request_times, nurse_locations):
            requests.append(request)
            nurses.append({ 'position': get_position_of_poi(location), 'location': location.label})
            nurses_locations.append(location)

        trial = Trial(id=trial_id, robots=set_of_robot_factors, requests=requests)
            
        trial.nurses = nurses
        trials.append(trial)
        append_baseline_trial(baseline_trials, id=trial_id, robots=set_of_robot_factors, 
            nurses_locations=nurses_locations, nurses=nurses, routes_ed=routes_ed, random=random)
        
        trial_id += 1
    
        planned_trials = []
        no_plan_trials = []


    # dump baseline trials
    with open('experiment_baseline_trials.json', 'w') as outfile:
        json.dump(baseline_trials, outfile, indent=4, sort_keys=True)

    # batch exec for trials
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
    with open('experiment_planned_trials.json', 'w') as outfile:
        json.dump(planned_trials, outfile, indent=4, sort_keys=True)

    if no_plan_trials:
        with open('experiment_no_plan_trials.json', 'w') as outfile:
            json.dump(no_plan_trials, outfile, indent=4, sort_keys=True)




def get_sim_exec():
    return SimExec(cf_process)



if __name__ == '__main__':
    main()
