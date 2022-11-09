from .skill_library import SkillLibrary
from .local_mission import LocalMissionController, TaskStatus
from .skill_implementation import ActiveSkillController

class SequencingProcess:
    def __init__(self, skill_library: SkillLibrary):
        self.skill_library = skill_library

    
    def run(self, local_mission: LocalMissionController, active_skill_ctrl: ActiveSkillController, task_status: TaskStatus):
        if local_mission.has_no_plan():
            # nothing to do
            return
        
        if active_skill_ctrl.is_idle():
            # load new task
            next_task = local_mission.next_task()
            skill_impl = self.skill_library.query(next_task)
            active_skill_ctrl.load(skill_impl, next_task)
            
        tick_status = active_skill_ctrl.tick()
        local_mission.update(tick_status)
        task_status.set_value(local_mission.get_task_status())



class SequencingProcessV2:
    def __init__(self, skill_library: SkillLibrary):
        self.skill_library = skill_library

    
    def run(self, local_mission: LocalMissionController, active_skill_ctrl: ActiveSkillController, task_status: TaskStatus):
        if local_mission.has_no_plan():
            # nothing to do
            return
        
        if active_skill_ctrl.is_idle():
            # load new task
            next_task = local_mission.next_task()
            skill_impl = self.skill_library.query(next_task)
            active_skill_ctrl.load(skill_impl, next_task)

        # handle enqueue new task    
        tick_status, new_task = active_skill_ctrl.tick()

        local_mission.update(tick_status)
        task_status.set_value(local_mission.get_task_status())


