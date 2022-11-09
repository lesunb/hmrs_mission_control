from abc import abstractmethod
from enum import Enum

from ..core import Task
from mission_control.mission.execution import eliminate_left_task, get_first_task
from skill_implementation import TickStatus

class LocalMissionController:
    class Status(Enum):
        NO_PLAN = 0
        IN_PROGRESS = 1
        CONCLUDED_WIH_SUCCESS = 2
        FATAL_FAILURE = 3

    def __init__(self, local_plan: Task):
        self.initial_plan = local_plan
        self.curr_plan = local_plan
        self._curr_task: Task = None
        self.concluded_curr_plan_tasks = 0
        if local_plan is not None:
            self.status = LocalMissionController.Status.IN_PROGRESS
        else:
            self.status = LocalMissionController.Status.NO_PLAN

    def has_no_plan(self):
        return self.curr_plan is None

    def update(self, tick_status: TickStatus) -> TickStatus:
        """
        Update curr plan with tick status
        """
        if tick_status.status is TickStatus.Type.COMPLETED_WITH_SUC: # task ended
            self.curr_plan = eliminate_left_task(tick_status.task, self.curr_plan)
            self._curr_task: Task = None
            self.concluded_curr_plan_tasks += 1
            if self.curr_plan is None:
                self.status = LocalMissionController.Status.CONCLUDED_WIH_SUCCESS
        #TODO task in progress

        #TODO failure

        #TODO send status

    def next_task(self):
        if self._curr_task is None:
            curr_task = self.get_next_task()
            self._curr_task = curr_task
            return curr_task
        else:
            raise Exception(f'trying to get a next task in a plan, while there is a task in progress {self._curr_task}')

    def get_next_task(self):
        return get_first_task(self.curr_plan)



    def get_task_status(self):
        pass


class TaskStatus:
    def set_value(self, value):
        pass

