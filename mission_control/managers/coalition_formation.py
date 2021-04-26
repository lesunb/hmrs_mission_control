
from mission_control.mission.ihtn import ElementaryTask, Task
from mission_control.mission.planning import distribute, flat_plan
from ..core import MissionContext, Worker

class CoalitionFormationManager:
    """ Service of creating coalitions. It receives an ihtn with tasks 
    assigned to roles an return a selection of robots to execute the plan """

    def __init__(self, units = [Worker]):
        self.individual_plans = []
        self.units = units

    def create_mission_context():
        pass

    def create_coalition(self, global_mission) -> MissionContext:
        m_context = self.create_mission_context(global_mission)
        individual_plans = self.individualize_plans(global_mission)
        plan_rank_map = map()
        for individual_plan in individual_plans:
            task_list = self.flat_plan(individual_plan)
            viable_bids = []
            candidates = self.get_compatible_units(task_list)
            for unit in candidates:
                bid = self.estimate(unit, task_list)
                is_viable = self.check_viable(bid)
                if is_resource_viable:
                    viable_bids.append(bid)
                else:
                    pass # TODO log
            ranked_bids = self.rank_bids(bid)
            plan_rank_map.put(individual_plan, ranked_bids)
        
        m_context.bids = plan_rank_map
        coalition_formation_result =  self.select_bids(m_context)
        m_context.coalition_formation_result = coalition_formation_result
        return m_context

    def adapt_coalition():
        pass

    @staticmethod
    def create_mission_context(global_mission: Task) -> MissionContext:
        return MissionContext()
    
    @staticmethod
    def individualize_plans(global_mission: Task) -> Task:
        for role in global_mission.assign_to:
            yield distribute(global_mission, role)
        return        
    
    @staticmethod
    def flat_plan(task) -> [ ElementaryTask ]:
        return flat_plan(task)

    def get_compatible_units(self, task_list: [ElementaryTask]):
        """  get the units that have the required skills for executing all tasks in 'task_list' """
        required_skills = set([ task.type for task in task_list ])

        for unit in self.units:
            if not required_skills.difference(unit.skills):
                yield unit
        return
        
    def estimate(self, unit, task_list: [ElementaryTask]): 
        pass

    @staticmethod
    def check_viable(bid):
        pass

    @staticmethod
    def rank_bids(bids):
        pass

    @staticmethod
    def select_bids(mission_context):
        pass