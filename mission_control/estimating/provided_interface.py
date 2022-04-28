from typing import Any, Callable, List, Tuple

from ..data_model import Task, Estimate, Worker
from .plugin_interfaces import TaskContext

class Partial:
    def __init__(self, task: Task, estimate:Estimate, plan: object):
        self.task, self.estimate, self.plan = task, estimate, plan

class Bid:
    def __init__(self, worker: Worker, estimate: Estimate, partials: List[Partial]= None):
        self.worker = worker
        self.estimate = estimate
        self.partials = partials

class Estimator:
    def estimation(self, task_context: TaskContext, estimate: Estimate, next: Callable, invalid: Callable, **plans ) -> Tuple[Estimate, Any]:
        pass

    def check_viable(self, bid: Bid, next, invalid):
        next()


# constant names

PLAN_MINIMUM_TARGET_BATTERTY_CHARGE_CONST = 'PLAN_MINIMUM_TARGET_BATTERTY_CHARGE_CONST'

