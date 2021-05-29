import json
from __init__ import *
from random import Random

from mission_control.core import Request
from evaluation.framework.exec_sim import SimExec
from evaluation.framework.trial import Trial
from evaluation.framework.trial import total_combinations, draw_without_repetition, draw_with_repetition

from resources.world_lab_samples import task_type, all_skills, near_ic_pc_rooms, cf_process, pickup_ihtn, get_position_of_poi


def gen_requests(times, locations, rand):
    selected_locations = draw_without_repetition(locations, len(times), rand)
    for time, location in zip(times, selected_locations):
        task, ihtn = pickup_ihtn(location)
        yield location, Request(task=task, timestamp=time)
    return

def main():
    random = Random()
    random.seed(42)
    number_of_robots = 5
    
    # times in which a new request will appear in the trial
    request_times = [ 2000 ] # single request

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
        draw_without_repetition(near_ic_pc_rooms, number_of_robots, random),
        draw_without_repetition(near_ic_pc_rooms, number_of_robots, random),
        draw_without_repetition(near_ic_pc_rooms, number_of_robots, random)
    ]

    # three selections of starting battery level for each robot
    # starting from 10 to 90
    battery_levels = [
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random),
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random),
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots, random),
    ]

    battery_consumption_rates = [
        draw_without_repetition([x * 0.0001 for x in range(10, 30)], number_of_robots, random),
        draw_without_repetition([x * 0.0001 for x in range(10, 30)], number_of_robots, random),
        draw_without_repetition([x * 0.0001 for x in range(10, 30)], number_of_robots, random),
    ]

    # constant for all robots
    avg_speed = [[0.8, 0.8, 0.8, 0.8, 0.8]]
    
    
    # Design - total combination of robot factors
    ######

    robots_factors_combinatios = total_combinations({
        'skills': skills,
        'location': locations,
        'battery_level': battery_levels,
        'battery_consumption_rate': battery_consumption_rates,
        'avg_speed': avg_speed
    })

    # set of requests    
    trial_id = 0
    trials = []
    requests = None
    for trial_robots_factors in robots_factors_combinatios:
        trial_robots = []
        for robot_id in range(0, number_of_robots):
            #each robot
            robot_facotrs = { 'id': robot_id }
            for key, values_set in trial_robots_factors.items():
                # each factor
                robot_facotrs[key] = values_set[robot_id]
            
            trial_robots.append(robot_facotrs)

        
        locations_without_robot = list(set(near_ic_pc_rooms) - set(trial_robots_factors['location']))
        # generate the a request for each time
        requests = []
        requests_locations = []
        for location, request in gen_requests(request_times, locations_without_robot, random):
            requests.append(request)
            requests_locations.append(location)

        trial = Trial(id=trial_id, robots=trial_robots, requests=requests)
        trials.append(trial)
        trial_id += 1
    
    trials_dicts = []

    # batch exec for trials
    for trial in trials:
        # run in deeco env
        ########
        sim_exec = get_sim_exec()
        final_state = sim_exec.run(trial)
        # inspect end state
        print(final_state)
        
        # prep exec sim
        ####### 
        for robot in trial.robots:
            robot['position'] = get_position_of_poi(robot['location'])
            robot['location'] = robot['location'].label
            robot['skills'].sort()
        print(robot)

        trial.nurses = []
        for req_location in requests_locations:
            trial.nurses.append({ 'position': get_position_of_poi(req_location), 'location': req_location.label})
        print(trial.nurses)

        # delete non dict
        delattr(trial, 'requests')
        trials_dicts.append(trial.__dict__)
    
    # dump trials
    with open('experiment_trials.json', 'w') as outfile:
        json.dump(trials_dicts, outfile, indent=4, sort_keys=True)
    

def get_sim_exec():
    return SimExec(cf_process)



if __name__ == '__main__':
    main()
