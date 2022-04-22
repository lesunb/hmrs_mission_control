
from ..data_model import Task
from .component_model_interfaces import SkillImplementation, TickStatus


class ActiveSkillController:
    """ 
    Active Skill Subsystem
    """
    def __init__(self):
        self.active_skill = None

    def load(self, skill: SkillImplementation, task: Task):
        """
        Load a new skill
        """
        self.active_skill = skill
        skill.load(task)

    def is_idle(self):
        """  
        Is idle if there is no active skill
        """
        return self.active_skill is None

    def tick(self) -> TickStatus:
        """
        Tick the active skill
        """
        tick_result = self.active_skill.tick()
        if tick_result.status == TickStatus.Type.COMPLETED_WITH_SUC:
            self.active_skill.complete()
            self.active_skill = None

        return tick_result
