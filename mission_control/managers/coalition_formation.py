
from typing import Generator, Dict
from typing import List

from mission_control.mission.ihtn import ElementaryTask, Task
from mission_control.mission.planning import distribute, flat_plan
from ..core import MissionContext, Worker, Bid
from ..estimate.estimate import EstimateManager

class CoalitionFormationManager:
    """ Service of creating coalitions. It receives an ihtn with tasks 
    assigned to roles an return a selection of robots to execute the plan """

    def __init__(self, workers: List[Worker], estimate_manager: EstimateManager):
        self.individual_plans = []
        self.workers = workers
        self.estimate_manager: EstimateManager = estimate_manager

    def create_mission_context():
        pass

    def create_coalition(self, global_mission) -> MissionContext:
        individual_plans = self.individualize_plans(global_mission)
        plan_rank_map = {}
        for individual_plan in individual_plans:
            task_list = self.flat_plan(individual_plan)
            viable_bids = []
            candidates = self.get_compatible_workers(task_list)
            for worker in candidates:
                bid = self.estimate(worker, task_list)
                is_viable = self.check_viable(bid)
                if is_viable:
                    viable_bids.append(bid)
                else:
                    pass # TODO log
            ranked_bids = self.rank_bids(viable_bids)
            plan_rank_map[individual_plan] = ranked_bids

        selected_bids =  self.select_bids(plan_rank_map)
        m_context: MissionContext = self.create_mission_context(global_mission)
        m_context.plans_and_ranked_bids = plan_rank_map
        m_context.selected_bids = selected_bids
        return m_context

    def adapt_coalition():
        pass

    @staticmethod
    def create_mission_context(global_mission: Task) -> MissionContext:
        return MissionContext(global_mission)
    
    @staticmethod
    def individualize_plans(global_mission: Task) -> Generator[Task, None, None]:
        for role in global_mission.assign_to:
            yield distribute(global_mission, role)
        return        
    
    @staticmethod
    def flat_plan(task) -> [ ElementaryTask ]:
        return flat_plan(task)

    def get_compatible_workers(self, task_list: [ElementaryTask]):
        """  get the workers that have the required skills for executing all tasks in 'task_list' """
        required_skills = set([ task.type for task in task_list ])

        for worker in self.workers:
            if not required_skills.difference(worker.skills):
                yield worker
        return
        
    def estimate(self, worker, task_list: [ElementaryTask]) -> Bid: 
        return self.estimate_manager.estimate(worker, task_list)

    @staticmethod
    def check_viable(bid: Bid) -> bool:
        if bid.estimate.is_impossible_to_estimate:
            return False
        # TODO check worker resources / battery
        else:
            return True
    @staticmethod
    def rank_bids(bids: [Bid]) -> [Bid]:
        return sorted(bids, key=lambda bid: bid.estimate.time, reverse=False)

    @staticmethod
    def select_bids(plan_rank_map: Dict):
        selected_bids = {}
        for task, bid_rank in plan_rank_map.items():
            #TODO estimate the wait time and verify resources
            selected_bids[task] = bid_rank[0]
        return selected_bids