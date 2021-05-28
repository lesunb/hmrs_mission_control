from typing import Final

from ..estimate.core import SkillDescriptor
from ..core import Estimate


def generic_skill_descriptor_constant_cost_factory(name, time_constant_cost):
    
    class GenericSkillDescriptor(SkillDescriptor):
        def __init__(self):
            self.time_constant_cost = time_constant_cost
            self.name = name
        
        def estimate(self, task_context):
            return Estimate(time = time_constant_cost, task=task_context.task)

    return GenericSkillDescriptor()