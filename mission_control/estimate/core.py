from abc import abstractmethod
import math, copy

from mission_control.mission.ihtn import ElementaryTask
from mission_control.core import Worker


class TaskContext:
    def __init__(self, unit: Worker):
        self.unit = unit
        self.task = None
        self.factors = None
        self.origin = None
        self.prev_ctx: TaskContext = None
        
    def start(self):
        self.origin = self.unit.position

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


class Estimate:
    def __init__(self, tasks, time, energy, invalid=False):
        if invalid:
            self.time =  math.inf
            self.energy =  math.inf
        pass

class Bid:
    def __init__(self, unit, estimate, tasks_estimates):
        self.time_individual_tasks = None
        self.power_consumption_individual_tasks = None

    def is_power_viable(self):
        pass
    
    def get_time_indivual_tasks(self):
        pass


class EnvironmentDescriptor:
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def get(parametes):
        pass

class EnvironmentDescriptorContainer:
    def __init__(self, descriptors = []):
        self.env_descs = {}
        for env_desc in descriptors:
            env_descs[type(env_desc)] = env_desc


class SkillDescriptor:
    def __init__(self, environment_descriptors: EnvironmentDescriptorContainer):
        self.ed = environment_descriptors

    def get_env_desc(type_) -> EnvironmentDescriptor :
        ed = self.ed.get(type_)
        if ed is None:
            raise f'ev {type_} not found'
        else:
            return ed

    @abstractmethod
    def estimate(self, task_context: TaskContext) -> Estimate:
        pass

