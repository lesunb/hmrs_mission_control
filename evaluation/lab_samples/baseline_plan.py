
from copy import deepcopy
from resources.world_lab_samples import get_position_of_poi, poi
from evaluation.framework.trial import draw_with_repetition
from typing import List


def append_baseline_trial(baseline_trials: List, id, robots, nurses_locations, nurses, routes_ed, random):
    # create baseline
    _robots = deepcopy(robots)

    # randomly select the robot
    selected = draw_with_repetition(_robots, 1, random)
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

    baseline_trials.append({'id': id, 'robots': _robots, 'nurses': nurses })
    
def get_baseline_plan(origin, nurse_location, lab, routes_ed):
    waypoints_to_nurse = routes_ed.get(origin, nurse_location).get_all_waypoints()
    waypoints_to_lab = routes_ed.get(nurse_location, lab).get_all_waypoints()
    return [
            [
                "navigation",
                [ 
                    nurse_location.label,
                    waypoints_to_nurse
                ]
            ],
            [
                "approach_person",
                [
                    "nurse"
                ]
            ],
            [
                "authenticate_person",
                [
                    "nurse"
                ]
            ],
            [
                "operate_drawer",
                [
                    "open"
                ]
            ],
            [
                "send_message",
                [
                    "nurse"
                ]
            ],
            [
                "wait_message",
                [
                    "r1"
                ]
            ],
            [
                "operate_drawer",
                [
                    "close"
                ]
            ],
            [
                "navigation",
                [
                    lab.label,
                    waypoints_to_lab
                ]
            ],
            [
                "approach_robot",
                [
                    "lab_arm"
                ]
            ],
            [
                "operate_drawer",
                [
                    "open"
                ]
            ],
            [
                "send_message",
                [
                    "lab_arm"
                ]
            ],
            [
                "wait_message",
                [
                    "r1"
                ]
            ],
            [
                "operate_drawer",
                [
                    "close"
                ]
            ]
        ]

