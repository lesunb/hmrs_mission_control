
from typing import Dict, Generator, List, Sequence

from utils.logger import ContextualLogger, Logger

from ..data_model import (Assignment, ElementaryTask, LocalMission,
                          MissionContext, MissionStatus, Role, Task, Worker,
                          flat_plan, transverse_ihtn_apply_for_task)
from ..estimating import Bid, EstimatingManager
from .integration import MissionHandler, MissionUnnexpectedError
from .planning import distribute


def coalitionFormationError(e, mission_context):
    message = f'Unexpected error forming coalition for {mission_context}'
    return MissionUnnexpectedError(e, message)

class CoalitionFormationProcess:
    """ Service of creating coalitions. It receives an ihtn with tasks 
    assigned to roles an return a selection of robots to execute the plan """

    def __init__(self, estimate_manager: EstimatingManager, cl: ContextualLogger):
        self.individual_plans = []
        self.estimate_manager: EstimatingManager = estimate_manager
        self.cl = cl
        self.l: Logger = cl.get_logger('cf_process')
        

    def run(self, mission_context: MissionContext, workers: List[Worker], mission_handler: MissionHandler):
        #try:
        self.do_run(mission_context, workers, mission_handler)
        # except Exception as e:
        #   if policy == try handle unnexected error
        #     mission_handler.handle_unnexpected_error(coalitionFormationError(e, mission_context))
        #   else:
        #     raise e
    def do_run(self, mission_context: MissionContext, workers: List[Worker], mission_handler: MissionHandler):
        if mission_context.status == MissionStatus.NEW:
            mission_context.local_missions = list(self.initialize_local_missions(mission_context))
            mission_context.status = MissionStatus.IN_PROGRESS
            mission_handler.start_mission(mission_context)

        is_success = self.create_coalition(mission_context, workers)
        if is_success:
            mission_handler.update_assigments(mission_context)
        else:
            # its all or northing - or assign all pending tasks or none
            mission_handler.no_coalition_available(mission_context)

    def create_coalition(self, mission_context: MissionContext, workers: List[Worker]) -> bool:
        self.l = self.cl.get_logger(f'cf_request_{mission_context.request_id}')
        plan_rank_map = {}
        for local_mission in self.get_pending_assignments(mission_context):
            mission_context.occurances.append(f'evaluating local mission for {local_mission.role}')
            task_list = self.flat_plan(local_mission.plan)
            self.l.log(task_list, entity='local_mission')
            bids = []
            candidates = self.get_compatible_workers(task_list, workers)
            for worker in candidates:
                mission_context.occurances.append(f'evaluating robot {worker.uuid}')
                bid = self.estimate(worker, task_list)
                is_viable = self.check_viable(bid, mission_context)
                mission_context.occurances.append(f'evaluating robot {worker.uuid}: bid is viable:{is_viable}')
                self.l.log(bid, entity='bid')
                if is_viable:
                    bids.append(bid)
                else:
                    mission_context.occurances.append(f'inviable reason: {bid.estimate.reason}')
                    pass # TODO log
            if not bids: # empty list of viable bids
                mission_context.occurances.append(f'no viable assignment for {local_mission.role}')
                return False
            rank = self.rank_bids(bids)
            self.l.log(rank, entity='rank')
            plan_rank_map[local_mission] = rank
            local_mission.bids = rank

        selected_bids =  self.select_bids(plan_rank_map)
        self.l.log_each_in_map(selected_bids, entity='selected_bid')
        self.set_assignment_from_selected_bids(mission_context, selected_bids)
        return True

    @staticmethod    
    def get_pending_assignments(mission_context: MissionContext) -> Sequence[LocalMission]:
        return filter(lambda lm: lm.assignment_status == LocalMission.AssignmentStatus.NOT_ASSIGNED, 
                        mission_context.local_missions)

    @staticmethod
    def initialize_local_missions(mission_context: MissionContext) -> Generator[LocalMission, None, None]:
        for role in mission_context.global_plan.assign_to:
            local_mission = distribute(mission_context.global_plan, role)
            lm = LocalMission(local_plan=local_mission, role=role, global_mission = mission_context)
            if role.type == Role.Type.NOT_MANAGED:
                lm.assignment_status =  LocalMission.AssignmentStatus.NOT_MANAGED
            yield lm
        return

    @staticmethod
    def flat_plan(task) -> List[ ElementaryTask ]:
        return flat_plan(task)

    def get_compatible_workers(self, task_list: List[ElementaryTask], workers: List[Worker]):
        """  get the workers that have the required skills for executing all tasks in 'task_list' """
        required_skills = set([ task.type for task in task_list if isinstance(task, ElementaryTask)])
    
        for worker in workers:
            missing_skills = required_skills.difference(worker.skills)
            if missing_skills:
                self.l.log(worker, missing_skills=missing_skills, entity='incompatible_workers')
            else:
                yield worker
        return

    def estimate(self, worker, task_list: List[ElementaryTask]) -> Bid: 
        return self.estimate_manager.estimation(worker, task_list)

    def check_viable(self, bid: Bid, mission_context: MissionContext) -> bool:
        if bid.estimate.is_inviable:
            return False
        res, estimate = self.estimate_manager.check_viable(bid, mission_context)
        
        if not res:
            bid.estimate = estimate
        return res

    @staticmethod
    def rank_bids(bids: List[Bid]) -> List[Bid]:
        return sorted(bids, key=lambda bid: bid.estimate.time, reverse=False)

    @staticmethod
    def select_bids(plan_rank_map: Dict):
        selected_bids = {}
        for local_mission, bid_rank in plan_rank_map.items():
            #TODO estimate the wait time and verify resources
            selected_bids[local_mission] = bid_rank[0]
        return selected_bids
    
    def set_assignment_from_selected_bids(self, mission_context: MissionContext, selected_bids: Dict[LocalMission, Bid]):
        for local_mission, bid in selected_bids.items():
            local_mission.worker = bid.worker
            local_mission.plan.assignment.estimate = selected_bids[local_mission].estimate
            local_mission.assignment_status = LocalMission.AssignmentStatus.ASSIGNED
            # set assignment on global plan
            global_plan = mission_context.global_plan

            winning_bid_tasks = list(map(lambda p: p.task, bid.partials))
            partials_map = {}
            for partial in bid.partials:
                partials_map[partial.task] = Assignment(partial.estimate, partial.plan)
            
            def set_assignment(ihtn_task: Task, task: Task):
                ihtn_task.assignment = partials_map[task]

            transverse_ihtn_apply_for_task(global_plan, winning_bid_tasks, set_assignment)
            transverse_ihtn_apply_for_task(local_mission.plan, winning_bid_tasks, set_assignment)
