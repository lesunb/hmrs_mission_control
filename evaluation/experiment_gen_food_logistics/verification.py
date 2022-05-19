from functools import reduce

from evaluation.experiment_gen_base import scenario
from lagom.container import Container

from mission_control.common_descriptors.routes_ed import RoutesEnvironmentDescriptor
#from resources.world_lab_samples import poi, approach_person_time, authenticate_person_time, operate_drawer_time, send_message_time, wait_message_time
from collections import namedtuple
from resources.world_lab_samples import *

robot_eval = namedtuple("robot_eval", "id has_missing_skills has_enough_battery estimated_time estimated_battery_discharge")
    
def evaluate_robot_pickup_samples(container:Container, nurse_location, avg_speed, battery_charge, 
    battery_discharge_rate, skills, location, id):
    routes_ed = container[RoutesEnvironmentDescriptor]

    missing_skills  = set(  # required
                        ['approach_person', 'approach_robot', 'authenticate_person', 
                        'navigation', 'operate_drawer']
                        ) - set(skills) # own skills
    has_missing_skills = True if missing_skills else False

    partials = [ # sum all
            (routes_ed.get(location, nurse_location).get_distance() / avg_speed ), # navto_room
            approach_person_time, #approach_nurse
            authenticate_person_time, #authenticate_nurse 
            operate_drawer_time, #open_drawer_for_nurse 
            send_message_time, wait_message_time, #deposit 
            operate_drawer_time, #close_drawer_nurse 
            (routes_ed.get(nurse_location, poi.laboratory.value).get_distance() / avg_speed ), #navto_lab 
            approach_person_time, #approach_arm 
            operate_drawer_time, #open_drawer_lab 
            send_message_time, wait_message_time, #pick_up_sample 
            operate_drawer_time, #close_drawer_lab
    ]
    estimated_time = reduce(lambda a, b: a + b, partials)
    
    estimated_battery_discharge = estimated_time * battery_discharge_rate
    has_enough_battery = (battery_charge - estimated_battery_discharge) > 0.05
    
    return robot_eval(id, has_missing_skills, has_enough_battery, estimated_time, estimated_battery_discharge)

def evaluate_scenario(avg_speed, battery_charge, battery_discharge_rate, skills, 
                     location):
    num_of_robots = len(avg_speed)
    nurse_location = location[-1] # last one
    robot_evals = [None] * num_of_robots
    for index in range(0, num_of_robots):
        robot_evals[index] = evaluate_robot_pickup_samples(
            container, nurse_location, avg_speed[index], battery_charge[index], 
            battery_discharge_rate[index], skills[index], location[index],
            id=(index +1)
        )
    print(robot_evals)

    # rank evals
    rank = sorted(robot_evals, key=lower_ttc_policy, reverse=True)
    return robot_evals, rank
    
def verify_trials(design, scenarios_with_plan):
    verification = {}
    for design, planned in zip(design, scenarios_with_plan):
        code = design.code
        expected_evaluation, rank = evaluate_scenario(**design)
        planned_assigned = get_assigned(planned)
        verification[code] = \
            rank[0].id == planned_assigned['id']
    return verification

def get_assigned(scenarios_with_plan):
    return next(filter(lambda r: r['local_plan'],  scenarios_with_plan.robots))

def lower_ttc_policy(r: robot_eval):
    if r.has_missing_skills:
        return -1
    elif not r.has_enough_battery:
        return 0
    else:
        return 1/r.estimated_time

