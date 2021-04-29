from typing import Final

from ..estimate.core import SkillDescriptor
from .routes_ed import RoutesEnvironmentDescriptor
from ..core import POI, Capability, Estimate, ImpossibleToEstimate


def generic_skill_descriptor_constant_cost_factory(name, time_constant_cost):
    
    class GenericSkillDescriptor(SkillDescriptor):
        def __init__(self):
            self.time_constant_cost = time_constant_cost
            self.name = name
        
        def estimate(self, task_context):
            return Estimate(time = time_constant_cost)

    return GenericSkillDescriptor()