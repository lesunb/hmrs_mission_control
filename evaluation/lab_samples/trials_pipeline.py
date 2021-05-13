from __init__ import *

from mission_control.core import Request
from evaluation.framework.exec_sim import SimExec
from evaluation.framework.trial import Trial
from evaluation.framework.trial import total_combinations, draw_without_repetition, draw_with_repetition

from resources.world_lab_samples import task_type, all_skills, all_rooms, cf_process, pickup_ihtn


def gen_requests(times, locations):
    selected_locations = draw_without_repetition(locations, len(times))
    for time, location in zip(times, selected_locations):
        task, ihtn = pickup_ihtn(location)
        yield Request(task=task, timestamp=time)
    return

def main():
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
        draw_with_repetition(skills_levels, number_of_robots),
        draw_with_repetition(skills_levels, number_of_robots),
        draw_with_repetition(skills_levels, number_of_robots)
    ]

    # three selections of positions for each robot
    locations = [ 
        draw_without_repetition(all_rooms, number_of_robots),
        draw_without_repetition(all_rooms, number_of_robots),
        draw_without_repetition(all_rooms, number_of_robots)
    ]

    # three selections of starting battery level for each robot
    # starting from 10 to 90
    battery_levels = [
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots),
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots),
        draw_without_repetition([x * 0.01 for x in range(10, 90)], number_of_robots),
    ]

    battery_consumption_rates = [
        draw_without_repetition([x * 0.001 for x in range(10, 30)], number_of_robots),
        draw_without_repetition([x * 0.001 for x in range(10, 30)], number_of_robots),
        draw_without_repetition([x * 0.001 for x in range(10, 30)], number_of_robots),
    ]

    # constant for all robots
    avg_speed = [[10, 10, 10, 10, 10]]
    
    
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
    for trial_robots_factors in robots_factors_combinatios:
        trial_robots = []
        for robot_id in range(0, number_of_robots):
            #each robot
            robot_facotrs = {}
            for key, values_set in trial_robots_factors.items():
                # each factor
                robot_facotrs[key] = values_set[robot_id]
            trial_robots.append(robot_facotrs)
        
        locations_without_robot = list(set(all_rooms) - set(trial_robots_factors['location']))
        # generate the a request for each time
        requests = list(gen_requests(request_times, locations_without_robot))

        trial = Trial(id=trial_id, robots=trial_robots, requests=requests)
        trials.append(trial)
        trial_id += 1
    

    # batch exec for trials
    for trial in trials:
        # run sim
        sim_exec = get_sim_exec()
        final_state = sim_exec.run(trial)
        # inspect end state
        print(final_state)
    # dump trials

def get_sim_exec():
    return SimExec(cf_process)



if __name__ == '__main__':
    main()
