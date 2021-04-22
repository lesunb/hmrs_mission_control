
from typing import List

from ensembles.core import Component, Role, Knowledge, process

from ensembles.field import Field
        

class GlobalMissionManager(Role):
    def __init__():
        self.mission_contexts = map()

class MissionContext:
    def __init__(self, request):
        self.id = 0
        self.request = request
        self.mision_status = 'NOT_STARTED'
        self.missions_local_plans = map()

class CoalitionFormationManager:
    ''' Responsible for new missions '''
    pass

class SupervisionManager:
    ''' Manages Existing Missions '''
    def __init__():
        pass


def coordinator_factory(id = 'Mission_Coordinator', environment_descriptors = None, skill_descriptors = None):
    # create new mission 

    coordinator = Component(
        id = id,
        features = [ SupervisionManager, CoalitionFormationManager],
        knowledge = Knowledge(
        ),
        processes = [
            # process(
            #     'coalision_formation',
            #     func(
            #         inp = ['request_queue'],
            #         inout = 'current_mission',
            #         inout = 'current_task',
            #         eval  = sequencing
            #     )
            #     scheduling = Periodic(100)
            # )
        ],
    )
    return coordinator