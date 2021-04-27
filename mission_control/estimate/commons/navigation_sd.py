from ..core import SkillDescriptor, POI, Estimate
from .routes_ed import RoutesEnvironmentDescriptor

class NavigationSkillDescriptor(SkillDescriptor):
    def __init__(self, environment_descriptors):
        super().__init__(environment_descriptors)
        self.routes_ed: RoutesEnvironmentDescriptor = self.getED(RoutesEnvironmentDescriptor)
    
    def estimate(self, task_context, unit):
        origin: POI = task_context.get('origin')
        dest: POI = task_context.get('destination')
        
        avg_speed = unit('avg_speed')

        route = self.routes_ed.get(origin, destination)
        if not route:
            return Estimate(invalid=True)
        distance = route.get_distance()
        estimate_time = distance / avg_speed
        return Estimate(time = estimate_time)

