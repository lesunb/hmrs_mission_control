import json
from typing import List

from mission_control.utils import LogFormatterManager
from mission_control.data_model.restrictions import LocalMission, Worker
from mission_control.estimating.estimating import Bid, Partial

from .to_executor import mc_task_to_exeuctor


def pipe(*funcs):
    def pipe_call(content, **kvalues):
        value = funcs[0](content, **kvalues) # first func
        for func in funcs[1:]: # others in the pipe
            value = func(value)
        return value

    return pipe_call

class CoalitionFormationLogger:
    
    def register(lfm: LogFormatterManager):
        lfm.register_formatter('incompatible_workers', pipe(CoalitionFormationLogger.incompatible_workers_to_log, json.dumps))
        lfm.register_formatter('bid', pipe(CoalitionFormationLogger.bid_to_log, json.dumps))
        lfm.register_formatter('rank', CoalitionFormationLogger.rank_to_log)
        lfm.register_formatter('selected_bid', pipe(CoalitionFormationLogger.selected_bid_to_log, json.dumps))
        lfm.register_formatter('local_mission', CoalitionFormationLogger.local_mission_to_log)

    def bid_to_log(bid: Bid):
        log_entry  = {
            'worker': bid.worker.name,
            'is_viable': not bid.estimate.is_inviable,
            'time': bid.estimate.time,
            'remaining_battery': bid.remaining_battery,
            'energy': bid.estimate.energy
        }
        return log_entry

    def rank_to_log(bids: List[Bid]):
        rank_to_log = list(map( lambda b: b.worker.name, bids))
        return rank_to_log
    
    def partials_to_log(partials: List[Partial]):
        def log_partial(partial: Partial):
            return {
                'skill': partial.task.type,
                'label': partial.task.name,
                'time': partial.estimate.time,
                'energy': partial.estimate.energy
            }
        return list(map(log_partial, partials))
        
    def incompatible_workers_to_log(worker: Worker, missing_skills):
        return { 'worker': worker.name, 'missing_skills': list(missing_skills)}

    def selected_bid_to_log(selected_bid: Bid, key=None):
        log_entry = CoalitionFormationLogger.bid_to_log(selected_bid)
        plan = CoalitionFormationLogger.partials_to_log(selected_bid.partials)
        log_entry['plan'] = plan
        return log_entry

    def local_mission_to_log(local_mission: LocalMission):
        return list(map(mc_task_to_exeuctor, local_mission))
