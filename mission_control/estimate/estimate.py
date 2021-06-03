import traceback

from typing import Callable, List, Tuple, Any
from mission_control.mission.ihtn import ElementaryTask, Task

from .core import SkillDescriptor, TaskContext, create_context_gen, SkillDescriptorRegister
from ..core import BatteryTimeConstantDischarge, Worker, Estimate, InviableEstimate


class Partial:
    def __init__(self, task: Task, estimate:Estimate, plan: object):
        self.task, self.estimate, self.plan = task, estimate, plan

class Bid:
    def __init__(self, worker: Worker, estimate: Estimate, partials: List[Partial]= None):
        self.worker = worker
        self.estimate = estimate
        self.partials = partials

class TimeEstimator:
    def __init__(self, skill_descriptors: SkillDescriptorRegister):
        self.skill_descriptors = skill_descriptors
    
    def estimation(self, task_context: TaskContext, estimate:Estimate, next, inviable, **plan) -> Tuple[Estimate, Any]:
        # look for a skill descriptor
        sd = self.skill_descriptors.get(task_context.task.type)
        if sd is None:
            # TODO log error
            return InviableEstimate(reason=f'no skill descriptor to estimate {task_context.task.type}'), None
        res = sd.estimate(task_context)
        if isinstance(res, Tuple):
            task_estimate, task_plan = res
            if task_plan:
                plan.update(task_plan)
        else:
            task_estimate = res
        next(task_estimate, **plan)

class EnergyEstimatorConstantDischarge:
    def estimation(self, task_context: TaskContext, estimate:Estimate, next:Callable, invalid:Callable) -> Tuple[Estimate, Any]:
        energy_model = task_context.worker.get_resource(BatteryTimeConstantDischarge)
        if isinstance(energy_model, BatteryTimeConstantDischarge):
            estimate.energy = estimate.time * energy_model.discharge_rate
        
        next(estimate)

class Estimator:
    def estimation(self, task_context: TaskContext, estimate:Estimate, next:Callable, invalid:Callable, **plans ) -> Tuple[Estimate, Any]:
        pass

class EstimationChain:
    def __init__(self, estimators: List[Estimator]):
        self.estimators = list(estimators)
    
    def estimate(self, task_context) -> Tuple[Estimate, Any]:
        result_estimate = None
        result_plan = None
        
        def inviable(reason: str):
            nonlocal result_estimate, result_plan

            estimate = InviableEstimate(reason)
            estimate.is_inviable = True
            result_estimate = estimate
            result_plan = None
            return
        
        def next(curr_estimate: Estimate, **plans):
            nonlocal result_estimate, result_plan
            if plans:
                result_plan = plans
            if not self.estimators:
                result_estimate = curr_estimate
                return 
            estimator = self.estimators.pop(0)
            #try:
            estimator.estimation(task_context, curr_estimate, next, inviable)
            #except Exception as e:
            #    inviable(f'exception in estimating with {estimator.__class__}: {traceback.format_exc()} ')

        next(Estimate())
        return result_estimate, result_plan


class EstimationManager:
    def __init__(self, estimate_chain: List[Estimator]):
        self.estimate_chain = estimate_chain
        
        

    def estimation(self, worker: Worker, task_list: List[ElementaryTask]) -> Bid: 
        task_context_gen = create_context_gen(worker, task_list)
        partials = []
        for task_context in task_context_gen:
            task_estimate, task_plan = self.estimation_in_task_context(task_context)
            if task_estimate.is_inviable:
                return Bid(worker, cost=task_estimate) # inf cost
            partials.append(Partial(task=task_context.task, estimate=task_estimate, plan=task_plan))
    
        aggregated = self.aggregate_estimates(partials)
        return Bid(worker, estimate=aggregated, partials=partials)
    
    def estimation_in_task_context(self, task_context) -> Tuple[Estimate, Any]:
        return EstimationChain(self.estimate_chain).estimate(task_context)

    def get_skill_descriptor(self, task_type) -> SkillDescriptor:
        sd = self.skill_descriptors[task_type]
        return sd

    def set_skill_descriptor(self, sd, task_type):
        self.skill_descriptors[task_type] = sd

    def aggregate_estimates(self, partials: List[Partial]) -> Estimate:
        total_time = 0
        total_energy = 0
        for partial in partials:
            estimate = partial.estimate
            total_time += estimate.time
            total_energy += estimate.energy
        return Estimate(time=total_time, energy=total_energy)