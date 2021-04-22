
from typing import List

from ensembles.core import Ensemble
from ensembles.exchange import member_to_coordinator, coordinator_to_member

from ensembles.field import Field


def has_intersection_skills_membership_function_facotry(mission_skills):
    def membership_function(coordinator, robot):
        if robot.skills is None:
            return False
        else:
            inters = mission_skills.intersection(robot.skills)
            return True if inters.len > 0 else False

def ensemble_factory(id = 'mission_control', membership = None):
    ensemble = Ensemble(
        id = id,
        coordinator_role = 'Mission_Coordinator',
        member_role = 'Robot',
        membership = membership,
        knowledge_exchange = [
            member_to_coordinator(
                from_member = [],
                to_coordinator = [],
                eval  = lambda args : True
            ),
            coordinator_to_member(
                from_coordinator = [],
                to_member = [],
                eval  = lambda args : True
            )
        ],
    )
    return ensemble

