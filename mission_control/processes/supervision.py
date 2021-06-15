

from abc import abstractmethod
import functools
import operator

from lagom.interfaces import T
from mission_control.mission.ihtn import Assignment, Task, TaskState, TaskStatus, ihtn_aggregate, transverse_ihtn
from mission_control.mission.coordination import update_mission

from typing import Generator, List, Tuple

from ..core import Estimate, LocalMission, MissionContext, MissionStatus, Worker
from .integration import MissionHandler, MissionUnnexpectedError

def createError(e, acitve_mission, updates):
    message = f'Unexpected error updating {acitve_mission} with {updates}'
    return MissionUnnexpectedError(e, message)

class SupervisionProcess:
    def __init__(self, mission_handle: MissionHandler):
        self.m_handler:MissionHandler = mission_handle

    def run(self, active_mission: MissionContext):
        #try:
        self.do_run(active_mission)
        #except Exception as e:
        #    self.m_handler.handle_unnexpected_error(createError(e, active_mission))


    def do_run(self, mission_context: MissionContext):
        self.update_mission_in_progress(mission_context)
        self.update_mission_with_failure(mission_context)

        mission_status = self.evaluate_mission_status(mission_context)
        self.report_mission_status(mission_context, mission_status)

    def update_mission_in_progress(self, mission_context: MissionContext):
        for local_mission, task_states in self.get_local_mission_in_progress_and_updates(mission_context):
            # local mission in progress
            has_failure = False
            for task_state in task_states:
                update_mission(local_mission.plan, task_state)
                update_mission(mission_context.global_plan, task_state)
        
            # mission end
            if local_mission.is_status(TaskStatus.SUCCESS_ENDED):
                self.end_local_mission(local_mission, TaskStatus.SUCCESS_ENDED)
                continue

            # mission cancelled
            has_local_mission_been_canceled = self.check_local_mission_cancelled(local_mission)
            if has_local_mission_been_canceled:
                self.end_local_mission(local_mission, TaskStatus.CANCELED)
                continue

            # task failure
            if local_mission.is_status(TaskStatus.FAILURE):
                self.transit_lm_to_with_failures(local_mission)
                continue

            # else the local misison is still in progress
            # continue

    def check_local_mission_cancelled(self, local_mission: LocalMission) -> bool:
        return False

    @staticmethod
    def evaluate_mission_status(mission_context: MissionContext) -> MissionStatus:
        def get_remaining_time(task: Task):
            if task.state.is_status(TaskStatus.SUCCESS_ENDED):
                return 0
            estimate: Estimate = task.assignment.estimate
            state: TaskState = task.state
            return estimate.time * \
                        (1 - state.progress)

        def set_remaining_time(task: Task, remaining_time):
            if  task.assignment is None:
                task.assignment = Assignment()
            if  task.assignment.estimate is None:
                task.assignment.estimate = Estimate()
            task.assignment.estimate.time = remaining_time

        def sum_remaining_time(abs_task: Task, subtasks: List[Task]):
            remaining_time = functools.reduce(operator.add, 
                map(lambda task: get_remaining_time(task)
                    ,subtasks))
            set_remaining_time(abs_task, remaining_time)

        ihtn_aggregate(mission_context.global_plan, sum_remaining_time)
        return MissionStatus(get_remaining_time(mission_context.global_plan))
    
    
    def end_local_mission(self, local_mission: LocalMission, end_status: TaskStatus):
        local_mission.worker = None
        local_mission.status = end_status

    def get_local_mission_in_progress_and_updates(self, mission_context: MissionContext) -> Generator[Tuple[LocalMission, List[TaskState]], None, None]:
        lms_in_progress = filter(lambda lm: lm.is_status(TaskStatus.IN_PROGRESS) or lm.is_status(TaskStatus.NOT_STARTED), mission_context.local_missions)
        for lm in lms_in_progress:
            yield lm, self.get_pending_updates(lm)


    @staticmethod
    def report_mission_status(mission_context: MissionContext, mission_status: MissionStatus):
        pass

    @abstractmethod
    def get_pending_updates(self, local_mission: LocalMission) -> List[TaskState]:
        pass

    ###################################
    # handle failure and mission repair
    ###################################

    def transit_lm_to_with_failures(self, local_mission: LocalMission):
        assert local_mission.is_status(TaskStatus.FAILURE)
        self.repair_local_missions(local_mission)

    def update_mission_with_failure(self, mission_context: MissionContext):
        for local_mission, failure in self.get_local_mission_with_failure(mission_context):
            pass

    def repair_local_missions(self, local_mission: LocalMission):
        return 


    def get_local_mission_with_failure(self, mission_context: MissionContext) -> Generator[Tuple[LocalMission, List[TaskState]], None, None]:
        lms_in_progress = filter(lambda lm: lm.is_status(TaskStatus.FAILURE), mission_context.local_missions)
        for lm in lms_in_progress:
            yield lm, self.get_pending_updates(lm)

    def try_handle_failure(self, failure):
        should_reasign = self.is_fatal(failure) or self.better_reasign(failure)
        can_be_reasigned = self.can_be_reasigned(failure)

        soluction = None
        if should_reasign and can_be_reasigned:
            soluction = self.reasign(failure)
        
        if not soluction:
            self.notify_not_recoverable_failure(failure, soluction)

           


            
