from mission_control.mission.ihtn import ElementaryTask

from .core import Estimate, TaskContext, SkillDescriptor, Bid


class EstimateManager:
    def __init__(self):
        self.skill_descriptors: map[str, SkillDescriptor] = {}
        # TODO init environment descriptors
        # TODO init skill descriptors
        pass

    def estimate(self, unit, task_list: [ElementaryTask]) -> Bid: 
        task_context_gen = self.create_context_gen(task_list)
        estimates = []
        for task_context in task_context_gen:
            estimates.append(self.estimate_task_in_context(task_context))
        
        total_cost = self.aggregate_estimates(estimates)
        return Bid(unit, cost=total_cost, partials=estimates)

    def estimate_task_in_context(self, task_context) -> Estimate :
        # look for a skill descriptor
        sd = self.get_skill_descriptor(task_context.type)
        sd.estimate(task_context)

    @staticmethod
    def create_context_gen(unit, task_list):
        task_context = TaskContext(unit=unit)
        task_context.start()

        for task in task_list:
            new_task_context = task_context.unwind(task)
            yield new_task_context
            task_context = new_task_context
        return
            
    def get_skill_descriptor(self, task_type) -> SkillDescriptor:
        sd = self.skill_descriptors[task_type]
        return sd

    def set_skill_descriptor(self, sd, task_type):
        self.skill_descriptors[task_type] = sd