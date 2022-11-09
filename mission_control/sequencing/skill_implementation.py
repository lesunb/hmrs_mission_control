
from abc import abstractmethod
from enum import Enum
from ..core import Task

class TickStatus:
    class Type(Enum):
        FATAL_FAILURE = 0
        IN_PROGRESS = 1
        COMPLETED_WITH_SUC = 2
    
    def __init__(self, status: Type, task: Task):
        self.status, self.task = status, task
    

class SkillImplementation:
    
    def __init__(self):
        self.is_loaded = False
        self.task = None

    @abstractmethod
    def on_load(self):
        """ 
        On start
        """
        pass
    
    @abstractmethod
    def on_complete(self):
        pass

    @abstractmethod
    def on_tick(self) -> TickStatus:
        pass
    
    def load(self, task: Task):
        self.on_load(task)
        self.is_loaded = True

    def tick(self) -> TickStatus:
        if not self.is_loaded:
            return #TODO return state loading
        return self.on_tick()

    def complete(self):
        self.on_complete()


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
