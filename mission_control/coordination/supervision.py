

import functools
import operator
from abc import abstractmethod
from typing import Generator, List, Tuple

from ..data_model import (Assignment, ElementaryTask, Estimate, LocalMission,
                          MissionContext, MissionState, MissionStatus, Task,
                          TaskState, TaskStatus, ihtn_aggregate, is_failed,
                          is_success)
from .integration import MissionHandler, MissionUnnexpectedError
from .repair import MissionRepairPlannerRegister, MissionRepairStatus
from .update_mission import update_estimates_with_progress


def createError(e, acitve_mission, updates):
    message = f'Unexpected error updating {acitve_mission} with {updates}'
    return MissionUnnexpectedError(e, message)

def end_mission(mission_context: MissionContext, status: MissionStatus):
    mission_context.status = status

def end_local_mission(local_mission: LocalMission, end_status: TaskStatus):
    local_mission.worker = None
    local_mission.status = end_status

# global mission life cycle
def end_mission_due_failure(mission_context: MissionContext):
    end_mission(mission_context, MissionStatus.FAILED)
    for lm in mission_context.local_missions:
        end_local_mission(lm, end_status=TaskStatus.FAILED)

def end_mission_concluded_with_success(mission_context: MissionContext):
    end_mission(mission_context, MissionStatus.COMPLETED_WITH_SUCCESS)
    for lm in  mission_context.local_missions:
        assert not lm.worker # check worker is not assigned

def only_elem_task_updates(task_states: List[TaskState]):
    return filter(lambda ts: isinstance(ts.task, ElementaryTask), task_states)


def update_local_mission_with_task_state(local_mission: LocalMission, task_state: TaskState):
    update_estimates_with_progress(local_mission.plan, task_state)
    if task_state.is_status(TaskStatus.FAILED):
        local_mission.failure = task_state


class SupervisionProcess:
    def __init__(self, mission_handle: MissionHandler, repair_planner_register: MissionRepairPlannerRegister):
        self.m_handler:MissionHandler = mission_handle
        self.repair_planner_register = repair_planner_register

    @abstractmethod
    def get_active_missions() -> List[MissionContext]:
        pass

    @abstractmethod
    def get_pending_updates(self, local_mission: LocalMission) -> List[TaskState]:
        pass

    def run(self):
        #try:
        for mission_context in self.get_active_missions():
            self.do_run(mission_context)
        #except Exception as e:
        #    self.m_handler.handle_unnexpected_error(createError(e, active_mission))
        # 

    def do_run(self, mission_context: MissionContext):
        # supervise local missions

        lm_task_progress = []
        for local_misison in mission_context.local_missions:
            task_updates = self.refresh_local_mission(local_misison)
            lm_task_progress.extend(task_updates)
        
        self.update_estimates(mission_context, lm_task_progress)
        # check mission status transitions
        # FAILED
        has_failure = any(map(lambda lm: is_failed(lm), mission_context.local_missions))
        if has_failure:
            end_mission_due_failure(mission_context)

        # CONCLUDED WITH SUCCESS
        all_success = all(map(lambda lms: is_success(lms), mission_context.local_missions))
        if all_success:
            end_mission_concluded_with_success(mission_context)
        
        mission_status = self.evaluate_mission_state(mission_context)
        self.report_mission_status(mission_context, mission_status)

    @staticmethod
    def update_estimates(mission_context: MissionContext, elem_task_updates: List[TaskState]):
        for task_state in elem_task_updates:
            update_estimates_with_progress(mission_context.global_plan, task_state)

    # local mission life cycle
    def refresh_local_mission(self, local_mission: LocalMission):
        # local mission in progress
        task_states = self.get_last_state_updates(local_mission)
        for task_state in task_states:
            update_local_mission_with_task_state(local_mission, task_state)

        #  failed
        if local_mission.is_status(TaskStatus.FAILED):
            
            # local mission repair
            repair_result, task_updates_after_repair = self.local_mission_repair(local_mission)

            if repair_result in [MissionRepairStatus.REASSIGN, MissionRepairStatus.PLAN_ADAPTED]:
                # repaired
                local_mission.set_status(TaskStatus.IN_PROGRESS)
                task_states = task_updates_after_repair
            elif repair_result == MissionRepairStatus.CANT_REPAIR:
                # failed
                local_mission.set_status(TaskStatus.FAILED)

        elif is_success(local_mission):
            end_local_mission(local_mission, TaskStatus.COMPLETED_WITH_SUC)

        return only_elem_task_updates(task_states)

    @staticmethod
    def evaluate_mission_state(mission_context: MissionContext) -> MissionState:
        def get_remaining_time(task: Task):
            if task.state.is_status(TaskStatus.COMPLETED_WITH_SUC):
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

        if mission_context.global_plan.state.is_in(
            TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED_WITH_SUC):
            ihtn_aggregate(mission_context.global_plan, sum_remaining_time)
        return MissionState(get_remaining_time(mission_context.global_plan))
    

    def get_local_mission_and_pending_updates_by_status(self, mission_context: MissionContext, *target_statuses: List[TaskStatus]) -> Generator[Tuple[LocalMission, List[TaskState]], None, None]:
        lms_in_progress = filter(lambda lm: lm.status_in(target_statuses), mission_context.local_missions)
        for lm in lms_in_progress:
            yield lm, self.get_pending_updates(lm)

    def report_mission_status(self, mission_context: MissionContext, mission_status: MissionStatus):
        print('ok')

    @abstractmethod
    def get_last_state_updates(self, local_mission: LocalMission) -> List[TaskState]:
        # TODO sort by timestamp, older first 
        return

    def local_mission_repair(self, local_mission: LocalMission):
        repair_planner = self.repair_planner_register.get(local_mission.global_mission.mission_type)
        repair_result, task_updates_after_repair = repair_planner.try_local_repair(local_mission)
        return repair_result, task_updates_after_repair

    ###################################
    # handle failure and mission repair
    ###################################

    @staticmethod
    def mark_to_reasign(local_mission: LocalMission):
        local_mission.worker = None
        local_mission.assignment_status = LocalMission.AssignmentStatus.NOT_ASSIGNED
    