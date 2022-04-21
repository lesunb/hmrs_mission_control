
from abc import abstractmethod
from enum import Enum

from ..data_model import Task

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
