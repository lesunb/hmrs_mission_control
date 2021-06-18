
from mission_control.mission.ihtn import TaskStatus, transverse_ihtn_apply_for_task
from typing import Generator, Dict, List, Sequence

from mission_control.mission.ihtn import Assignment, ElementaryTask, Task
from mission_control.mission.planning import distribute, flat_plan
from .integration import MissionHandler, MissionUnnexpectedError
from ..core import MissionContext, MissionStatus, Worker, LocalMission, Role
from ..estimate.estimate import EstimationManager, Bid

def coalitionFormationError(e, mission_context):
    message = f'Unexpected error forming coalition for {mission_context}'
    return MissionUnnexpectedError(e, message)



class CoalitionFormationProcess:
    """ Service of creating coalitions. It receives an ihtn with tasks 
    assigned to roles an return a selection of robots to execute the plan """

    def __init__(self, estimate_manager: EstimationManager):
        self.individual_plans = []
        self.estimate_manager: EstimationManager = estimate_manager
        

    def run(self, mission_context: MissionContext, workers: List[Worker], mission_handler: MissionHandler):
        #try:
        self.do_run(mission_context, workers, mission_handler)
        # except Exception as e:
        #     mission_handler.handle_unnexpected_error(coalitionFormationError(e, mission_context))

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
        plan_rank_map = {}
        for local_mission in self.get_pending_assignments(mission_context):
            mission_context.occurances.append(f'evaluating local mission for {local_mission.role}')
            task_list = self.flat_plan(local_mission.plan)
            bids = []
            candidates = self.get_compatible_workers(task_list, workers)
            for worker in candidates:
                mission_context.occurances.append(f'evaluating robot {worker.uuid}')
                bid = self.estimate(worker, task_list)
                is_viable = self.check_viable(bid, mission_context)
                mission_context.occurances.append(f'evaluating robot {worker.uuid}: bid is viable:{is_viable}')
                if is_viable:
                    bids.append(bid)
                else:
                    mission_context.occurances.append(f'inviable reason: {bid.estimate.reason}')
                    pass # TODO log
            if not bids: # empty list of viable bids
                mission_context.occurances.append(f'no viable assignment for {local_mission.role}')
                return False
            bids = self.rank_bids(bids)
            plan_rank_map[local_mission] = bids
            local_mission.bids = bids

        selected_bids =  self.select_bids(plan_rank_map)
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
            if not required_skills.difference(worker.skills):
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
