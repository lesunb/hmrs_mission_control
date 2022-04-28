import copy
from abc import abstractmethod
from typing import Any, Tuple

from ..data_model import ElementaryTask, Estimate, Worker



class TaskContext:
    def __init__(self, worker: Worker):
        self.worker = worker
        self.task: ElementaryTask = None
        self.factors = None
        self.origin = None
        self.prev_ctx: TaskContext = None
        
    def start(self):
        self.origin = self.worker.location

    def unwind(self, next_task: ElementaryTask):
        next_task_ctx = copy.copy(self)
        next_task_ctx.task = next_task
        next_task_ctx.prev_ctx = self
        # curr destination is the next task origin
        if self.get('destination') is not None:
            next_task_ctx.origin = self.get('destination')

        return next_task_ctx
    
    def get(self, prop):
        """ 
        Get prop from task, ctx, and recursivly form previous tasks/ctxs
            Note taht Props that were not not override in newer ctxs are considered current.
         """
        # look into the ctx
        task_prop = getattr(self.task, prop, None)
        ctx_prop = getattr(self, prop, None)
        value = task_prop if task_prop is not None else ctx_prop

        if value is not None:
            return value
        elif self.prev_ctx is not None:
            return self.prev_ctx.get(prop)
        else:
            return None


class SkillDescriptor:
    name = None
    required_capabilities = None

    @abstractmethod
    def estimate(self, task_context: TaskContext) -> Tuple[Estimate, Any]:
        """
        Realize estimate. Returns an Estimate and optionally a plan to be 
        used by an equivalent skill implementation
        """
        pass

class EnvironmentDescriptor:
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def get(self, parametes):
        pass

class SkillDescriptorRegister:
    def __init__(self, *task_type_skill_desc_pairs):
        self.descs = {pair[0]: pair[1] for pair in task_type_skill_desc_pairs}
    
    def register(self, task_type, descriptor: SkillDescriptor):
        self.descs[task_type] = descriptor

    def get(self, type) -> SkillDescriptor:
        return self.descs[type]
        


