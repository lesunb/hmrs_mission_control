
from ..sequencing import SkillLibrary

class TaskExecutor:
    def __init__(self, skill_library: SkillLibrary):
        self.local_plan = None
        self.skill_library = skill_library
    
    def run(self):
        while True:
            for result in self.exec_next_task():
                self.handle_task_status_update(result)
                yield
            self.handle_task_result(result)
    
    def exec_next_task(self):
        """ should be constantly in a run loop while the robot is active """
        task = self.next_task()
        if not task:
            return 'empty plan'
        
        skill_impl = self.skill_library.get_skill(task)
        skill_impl.load(task)

        while True:
            task_status = self.run(skill_impl)
            if self.has_task_ended(task_status):
                return task_status
            else:
                yield task_status

    def run(self, skill_impl):
        return skill_impl.tick()

    def handle_task_result(self, task_result):
        pass

    def handle_task_status_update(self, task_result):
        pass

    def next_task(self):
        pass

    def sleep():
        pass

    def update_local_plan(self):
        pass

    def init_skill_library(self):
        pass

    def has_task_ended(self, task_status):
        pass

