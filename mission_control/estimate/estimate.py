from typing import List, Tuple
from mission_control.mission.ihtn import ElementaryTask, Task

from .core import SkillDescriptor, TaskContext, create_context_gen, SkillDescriptorRegister
from ..core import Worker, Estimate, ImpossibleToEstimate


class Partial:
    def __init__(self, task: Task, estimate:Estimate, plan: object):
        self.task, self.estimate, self.plan = task, estimate, plan

class Bid:
    def __init__(self, worker: Worker, estimate: Estimate, partials: List[Partial]= None):
        self.worker = worker
        self.estimate = estimate
        self.partials = partials

class EstimateManager:
    def __init__(self, skill_descriptors: SkillDescriptorRegister):
        self.skill_descriptors = skill_descriptors

    def estimate(self, worker: Worker, task_list: List[ElementaryTask]) -> Bid: 
        task_context_gen = create_context_gen(worker, task_list)
        partials = []
        for task_context in task_context_gen:
            task_estimate, task_plan = self.estimate_task_in_context(task_context)
            if task_estimate.is_impossible_to_estimate:
                return Bid(worker, cost=task_estimate) # inf cost
            partials.append(Partial(task=task_context.task, estimate=task_estimate, plan=task_plan))
        
        aggregated = self.aggregate_estimates(partials)
        return Bid(worker, estimate=aggregated, partials=partials)

    def estimate_task_in_context(self, task_context: TaskContext) -> Estimate :
        # look for a skill descriptor
        sd = self.skill_descriptors.get(task_context.task.type)
        if sd is None:
            # TODO log error
            return ImpossibleToEstimate(reason=f'no skill descriptor to estimate {task_context.task.type}')
        estimate, plan = sd.estimate(task_context)
        return estimate, plan

            
    def get_skill_descriptor(self, task_type) -> SkillDescriptor:
        sd = self.skill_descriptors[task_type]
        return sd

    def set_skill_descriptor(self, sd, task_type):
        self.skill_descriptors[task_type] = sd

    def aggregate_estimates(self, partials: List[Partial]) -> Estimate:
        total_time = 0
        total_energy = 0
        for partial in partials:
            estimate = partial.estimate
            total_time += estimate.time
            total_energy += estimate.energy
        return Estimate(time=total_time, energy=total_energy)