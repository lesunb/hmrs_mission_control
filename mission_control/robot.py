from typing import List

from ensembles.core import Component, Role, Knowledge, process

from ensembles.field import Field

class LocalMissionManager(Role):
    def __init__():
        self.status = Field(None)
        self.mission_queue = []
        self.current_mission = None
        self.current_task = Field(None)
        self.current_task_status = None

        self.current_task.bind_to(sequencing_task)
        # on_change

    def bind(self):
        pass

    def get_update_status_process(self, status):

        def update_status():
            pass

        return update_status

    def select_mission(self):
        pass

    def sequence_mission(self):
        ''' on change mission queue '''
        pass

    def sequencing_task(self, current_task_status):
        ''' on current_task end '''
        
        next_task = self.get_next(self.current_mission, current_task_status)
        if next_task != current_task_status:
            current_task_status.value = next_task


def sequencing(mission_queue, current_mission, current_task):
    return current_task


def robot_factory(id, position):
    robot = Component(
        id = id,
        features = [ LocalMissionManager ],
        knowledge = Knowledge(
            id = id,
            position = position
        ), 
        processes = [
            # process(
            #     'sequencing',
            #     func(
            #         inp = ['mission_queue'],
            #         inout = 'current_task',
            #         eval  = sequencing
            #     ),
            #     scheduling = Periodic(100)
            # )
        ],
    )
    return robot


