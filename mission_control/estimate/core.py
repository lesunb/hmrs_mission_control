from abc import abstractmethod
import math, copy

from mission_control.mission.ihtn import ElementaryTask
from mission_control.core import Worker


class TaskContext:
    def __init__(self, worker: Worker):
        self.worker = worker
        self.task = None
        self.factors = None
        self.origin = None
        self.prev_ctx: TaskContext = None
        
    def start(self):
        self.origin = self.worker.position

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


def create_context_gen(worker: Worker, task_list: [ElementaryTask]):
    task_context = TaskContext(worker=worker)
    task_context.start()

    for task in task_list:
        new_task_context = task_context.unwind(task)
        yield new_task_context
        task_context = new_task_context
    return

class Estimate:
    def __init__(self, task=None, time=math.inf, energy=math.inf):
        self.is_viable = True
        self.task = task
        self.time = time
        self.energy = energy

class Nonviable(Estimate):
    def __init__(self, reason:str, ):
        super(time = math.inf, energy = math.inf)
        self.reason = reason
        self.is_viable = False


            
class Bid:
    def __init__(self, worker, estimate, partials):
        self.worker = worker
        self.estimate = estimate
        self.partials = partials

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

class SkillDescriptor:
    name = None
    required_capabilities = None

    @abstractmethod
    def estimate(self, task_context: TaskContext) -> Estimate:
        pass

class SkillDescriptorRegister:
    def __init__(self, *task_type_skill_desc_pairs):
        self.descs = {}
        for pair in task_type_skill_desc_pairs:
            self.descs[pair[0]] = pair[1]
    
    def register(self, task_type, descriptor: SkillDescriptor):
        self.descs[task_type] = descriptor

    def get(self, type):
        return self.descs[type]
