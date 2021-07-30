
from copy import deepcopy
from evaluation.experiment_gen_base.trial_design import draw_without_repetition
from resources.world_lab_samples import get_position_of_poi, poi
from typing import List




def append_baseline_trial(baseline_trials: List, id, code, factors, robots, nurses_locations, nurses, routes_ed, random):
    # create baseline
    _robots = deepcopy(robots)

    # randomly select the robot
    selected = draw_without_repetition(_robots, 1, random)
    selected_robot = selected[0]

    # set empty plan
    for robot in _robots:
        robot['local_plan'] = None

    # generate a plan for the selected robot 
    nurse_location = nurses_locations[0]
    local_plan = get_baseline_plan(origin = selected_robot['location'], nurse_location=nurse_location, 
                lab=poi.laboratory.value, routes_ed= routes_ed)
    selected_robot['local_plan'] = local_plan

    # prepare for json
    for robot in _robots:
        robot['position'] = get_position_of_poi(robot['location'])
        robot['location'] = robot['location'].label
        robot['skills'].sort()

    baseline_trials.append({'id': id, 'code': code, 'factors': factors, 'robots': _robots, 'nurses': nurses })
    
def get_baseline_plan(origin, nurse_location, lab, routes_ed):
    waypoints_to_nurse = routes_ed.get(origin, nurse_location).get_all_waypoints()
    waypoints_to_lab = routes_ed.get(nurse_location, lab).get_all_waypoints()
    return [
            [
                "navigation",
                [ 
                    nurse_location.label,
                    waypoints_to_nurse
                ],
                "navto_room"
            ],
            [
                "approach_person",
                [
                    "nurse"
                ],
                "approach_nurse"
            ],
            [
                "authenticate_person",
                [
                    "nurse"
                ],
                "authenticate_nurse"
            ],
            [
                "operate_drawer",
                [
                    "open"
                ],
                "open_drawer_for_nurse"
            ],
            [
                "send_message",
                [
                    "nurse"
                ],
                "notify_nurse_of_open_drawer_for_nurse_completed"
            ],
            [
                "wait_message",
                [
                    "nurse"
                ],
                "wait_nurse_to_complete_deposit"
            ],
            [
                "operate_drawer",
                [
                    "close"
                ],
                "close_drawer_nurse"
            ],
            [
                "navigation",
                [
                    lab.label,
                    waypoints_to_lab
                ],
                "navto_lab"
            ],
            [
                "approach_robot",
                [
                    "lab_arm"
                ],
                "approach_arm"
            ],
            [
                "operate_drawer",
                [
                    "open"
                ],
                "open_drawer_lab"
            ],
            [
                "send_message",
                [
                    "lab_arm"
                ],
                "notify_lab_arm_of_open_drawer_lab_completed"
            ],
            [
                "wait_message",
                [
                    "lab_arm"
                ],
                "wait_lab_arm_to_complete_pick_up_sample"
            ],
            [
                "operate_drawer",
                [
                    "close"
                ],
                "close_drawer_lab"
            ]
        ]

