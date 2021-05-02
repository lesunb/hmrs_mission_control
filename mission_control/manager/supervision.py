

from ..core import MissionContext
from .integration import MissionHandler, MissionUnnexpectedError

def createError(acitve_mission, assigned_workers, updates):
    self.message = f'Unexpected error updating {acitve_mission} with {updates}'
    return MissionUnnexpectedError(e, message)

class SupervisionProcess:
    def __init__(self, mission_handle: MissionHandler):
        self.m_handler:MissionHandler = mission_handle

    def run(active_mission: MissionContext, assigned_workers: [Worker], updates):
        try:
            self.do_run(active_mission, assigned_workers, updates)
        except e:
            self.m_handler.handle_unnexpected_error(createError(e, active_mission, updates))

    def do_run(active_mission: MissionContext, assigned_workers: [Worker], updates):
        (robot_statuses, mission_status) = self.update_mission()
                    
        if mission_status.is_complete_with_success or mission_status.is_permanent:
            self.finish_mission(active_mission)

        for robot_status in status.robot_statuses:
            if robot_status.is_completed_with_success:
                self.assignment_complete(robot_status.robot)
            elif robot_status.is_fatal_failure:
                self.handle_permanent_failure(robot_status)
            elif mission_status.is_fatal_failure and robot_status.is_ok \
                                                 and robot_status.task_can_be_canceled:
                self.assignment_cancel(robot_status.robot)

        self.report_progress(active_mission)

    def update_mission(self, updates):
        # do update
        violations = self.check_restrictions()

    def handle_reasignable_failure(self, robot_status):
        request = Request(self.active_mission)
        self.queue_request(request)

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

           


            
