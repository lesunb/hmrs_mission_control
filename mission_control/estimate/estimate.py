from typing import List
from mission_control.mission.ihtn import ElementaryTask

from .core import SkillDescriptor, create_context_gen, SkillDescriptorRegister
from ..core import Worker, Estimate, ImpossibleToEstimate

class Bid:
    def __init__(self, worker: Worker, estimate: Estimate, partials: List[Estimate]= None):
        self.worker = worker
        self.estimate = estimate
        self.partials = partials

class EstimateManager:
    def __init__(self, skill_descriptors: SkillDescriptorRegister):
        self.skill_descriptors = skill_descriptors

    def estimate(self, worker: Worker, task_list: List[ElementaryTask]) -> Bid: 
        task_context_gen = create_context_gen(worker, task_list)
        estimates = []
        for task_context in task_context_gen:
            partial = self.estimate_task_in_context(task_context)
            estimates.append(partial)
            if partial.is_impossible_to_estimate:
                return Bid(worker, cost=partial, partials=estimates)
        
        aggregated = self.aggregate_estimates(estimates)
        return Bid(worker, estimate=aggregated, partials=estimates)

    def estimate_task_in_context(self, task_context) -> Estimate :
        # look for a skill descriptor
        sd = self.skill_descriptors.get(task_context.task.type)
        if sd is None:
            # TODO log error
            return ImpossibleToEstimate(reason=f'no skill descriptor to estimate {task_context.task.type}')
        return sd.estimate(task_context)

            
    def get_skill_descriptor(self, task_type) -> SkillDescriptor:
        sd = self.skill_descriptors[task_type]
        return sd

    def set_skill_descriptor(self, sd, task_type):
        self.skill_descriptors[task_type] = sd

    def aggregate_estimates(self, estimates: List[Estimate]) -> Estimate:
        total_time = 0
        total_energy = 0
        for partial in estimates:
            total_time += partial.time
            total_energy += partial.energy
        return Estimate(time=total_time, energy=total_energy)