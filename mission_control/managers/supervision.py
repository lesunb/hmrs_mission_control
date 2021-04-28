

class TaskStatusUpdate:
    pass


class Supervision:
    def __init__(self, mission_context):
        pass

    def update_mission(self, task_status_update):
        pass

    def check_mission_restrictions():
        pass

    def check_worker_restrictions():
        pass

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

           


            
