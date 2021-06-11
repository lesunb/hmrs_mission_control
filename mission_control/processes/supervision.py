

import functools
import operator
from mission_control.mission.ihtn import Assignment, Task, TaskState, TaskStatus, ihtn_aggregate, transverse_ihtn
from mission_control.mission.coordination import update_mission

from typing import List

from ..core import Estimate, MissionContext, MissionStatus, Worker
from .integration import MissionHandler, MissionUnnexpectedError

def createError(e, acitve_mission, updates):
    message = f'Unexpected error updating {acitve_mission} with {updates}'
    return MissionUnnexpectedError(e, message)

class SupervisionProcess:
    def __init__(self, mission_handle: MissionHandler):
        self.m_handler:MissionHandler = mission_handle

    def run(self, active_mission: MissionContext, assigned_workers: List[Worker], updates):
        try:
            self.do_run(active_mission, assigned_workers, updates)
        except Exception as e:
            self.m_handler.handle_unnexpected_error(createError(e, active_mission, updates))

    def do_run(self, mission_context: MissionContext, assigned_workers: List[Worker], updates):
        mission_status = self.update_mission()
        
    
        # handle mission status
        if mission_status.is_ok:
            if robot_status.is_completed_with_success:
                self.assignment_complete(robot_status.robot)
            
            self.report(mission_status)

        else:
            repair(mission_context)
        
        robot_status = self.get_robot_status()
        # 
        for robot_status in robot_statuses:
            
            if robot_status.is_completed_with_success:
                self.assignment_complete(robot_status.robot)
            elif robot_status.is_fatal_failure:
                self.handle_permanent_failure(robot_status)
            elif mission_status.is_fatal_failure and robot_status.is_ok \
                                                 and robot_status.task_can_be_canceled:
                self.assignment_cancel(robot_status.robot)

        if mission_status.is_complete_with_success or mission_status.is_permanent:
            self.finish_mission(active_mission)

        self.report_progress(active_mission)

    def evaluate_mission_status(mission_context: MissionContext) -> MissionStatus:
        def get_remaining_time(task: Task):
            if task.state.is_status(TaskStatus.SUCCESS_END):
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

    def get_updated_mission_status(self, mission_context: MissionContext) -> MissionStatus:
        task_states = self.get_task_states()
        for task_state in task_states:
            update_mission(mission_context.global_plan, task_state)

        evaluate_mission_status(mission_context)

        # do update
        violations = self.check_restrictions()

    def repair(self, mission_context: MissionContext):
        pass

    def assignment_complete(self, robot):
        self.update_assigment(ScheduleUpdate(worker=robot, status='avaiable') )

    def assignment_cancel(self, robot):
        self.update_assigment(ScheduleUpdate(worker=robot, status='avaiable') )

    def handle_permanent_failure(self, robot_status):
        self.report_to_operator(robot=robot_status.robot, content=robot_status.failure)
        self.update_assigment(ScheduleUpdate(worker=robot, status='unavailable') )


    def update_progress_and_check_mission_restriction(self, task_status_update):
        self.update_mission(task_status_update)
        checks = self.check_mission_restrictions()

        if has_failure(checks):
            self.handle_failure(checks.failures)
        else:
            self.update_progress(checks)
    
    def update_worker_status_and_check_resources(self, worker_status):
        self.update_worker_status(uworker_status)
        check = self.check_worker_restrictions()
        
        if has_failure(checks):
            self.try_handle_failure(checks.failure)
        else:
            self.update_progress(checks)

    def get_progress():
        pass




    def try_handle_failure(self, failure):
        should_reasign = self.is_fatal(failure) or self.better_reasign(failure)
        can_be_reasigned = self.can_be_reasigned(failure)

        soluction = None
        if should_reasign and can_be_reasigned:
            soluction = self.reasign(failure)
        
        if not soluction:
            self.notify_not_recoverable_failure(failure, soluction)

           


            
