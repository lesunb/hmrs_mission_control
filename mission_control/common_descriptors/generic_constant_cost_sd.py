from typing import Final

from ..coordinator.estimating.core import SkillDescriptor
from ..data_model.core import Estimate


def generic_skill_descriptor_constant_cost_factory(name, time_constant_cost):
    
    class GenericSkillDescriptor(SkillDescriptor):
        def __init__(self):
            self.time_constant_cost = time_constant_cost
            self.name = name
        
        def estimate(self, _):
            return Estimate(time = time_constant_cost), None

    return GenericSkillDescriptor()