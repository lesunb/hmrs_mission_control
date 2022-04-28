import traceback
from typing import Any, Callable, List, Tuple

from ..data_model import (BatteryTimeConstantDischarge, ElementaryTask,
                          Estimate, InviableEstimate, MissionContext, Worker)
from ..utils.contants import ConstantsProvider
from .plugin_interfaces import SkillDescriptor, SkillDescriptorRegister
from .provided_interface import (PLAN_MINIMUM_TARGET_BATTERTY_CHARGE_CONST,
                                 Bid, Estimator, Partial, TaskContext)


class TimeEstimator(Estimator):
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

    def check_viable(self, bid: Bid, mission_context: MissionContext, next, invalid):
        if not mission_context or not mission_context.global_plan:
            next()
            return
        
        max_time = mission_context.global_plan.attributes.get('max_time')
        if max_time is None or bid.estimate.time < max_time:
            next()
            return
        else:
            invalid('max time exceeded (5 min)')

class EnergyEstimatorConstantDischarge(Estimator):
    def __init__(self, constant_config_provider: ConstantsProvider):
        self.min_target_battery_chage = constant_config_provider.get(PLAN_MINIMUM_TARGET_BATTERTY_CHARGE_CONST, 0)

    def estimation(self, task_context: TaskContext, estimate:Estimate, next:Callable, invalid:Callable) -> Tuple[Estimate, Any]:
        energy_model = task_context.worker.get_resource(BatteryTimeConstantDischarge)
        if isinstance(energy_model, BatteryTimeConstantDischarge):
            estimate.energy = estimate.time * energy_model.discharge_rate
        
        next(estimate)
    
    def check_viable(self, bid: Bid, mission_context: MissionContext, next, invalid):
        energy_model: BatteryTimeConstantDischarge = bid.worker.get_resource(BatteryTimeConstantDischarge)
        remaining_battery = energy_model.battery.charge - bid.estimate.energy
        bid.remaining_battery = remaining_battery
        if remaining_battery > energy_model.minimum_useful_level and \
            remaining_battery > self.min_target_battery_chage:
            next()
        else:
            invalid('Not enough battery')
        
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
            if not self.estimators:  # chain ended
                result_estimate = curr_estimate
                return 
            estimator = self.estimators.pop(0)
            try:
                estimator.estimation(task_context, curr_estimate, next, inviable)
            except Exception as e:
               inviable(f'exception in estimating with {estimator.__class__}: {traceback.format_exc()} ')

        next(Estimate())
        return result_estimate, result_plan

class CheckViabilityChain:
    def __init__(self, estimators: List[Estimator]):
        self.estimators = list(estimators)
    
    def check_viable(self, bid: Bid, mission_context: MissionContext) -> bool:
        result = True
        result_estimate = None
        
        def inviable(reason: str):
            nonlocal result_estimate, result
            result = False

            estimate = InviableEstimate(reason)
            estimate.is_inviable = True
            result_estimate = estimate
            return
        
        def next():
            if not self.estimators: # chain ended
                return
            
            estimator = self.estimators.pop(0)
            try:
                estimator.check_viable(bid, mission_context, next, inviable)
            except Exception as e:
               inviable(f'exception in estimating with {estimator.__class__}: {traceback.format_exc()} ')

        next()
        return result, result_estimate

def create_context_gen(worker: Worker, task_list: List[ElementaryTask]):
    task_context = TaskContext(worker=worker)
    task_context.start()

    for task in task_list:
        new_task_context = task_context.unwind(task)
        yield new_task_context
        task_context = new_task_context
    return



class EstimatingManager:
    def __init__(self, estimate_chain: List[Estimator]):
        self.estimate_chain = estimate_chain
        
    def estimation(self, worker: Worker, task_list: List[ElementaryTask]) -> Bid: 
        task_context_gen = create_context_gen(worker, task_list)
        partials = []
        for task_context in task_context_gen:
            task_estimate, task_plan = self.estimation_in_task_context(task_context)
            if task_estimate.is_inviable:
                return Bid(worker, estimate=task_estimate) # inf cost
            partials.append(Partial(task=task_context.task, estimate=task_estimate, plan=task_plan))
    
        aggregated = self.aggregate_estimates(partials)
        return Bid(worker, estimate=aggregated, partials=partials)

    def check_viable(self, bid: Bid, mission_context: MissionContext):
        return CheckViabilityChain(self.estimate_chain).check_viable(bid, mission_context)
    
    def estimation_in_task_context(self, task_context) -> Tuple[Estimate, Any]:
        return EstimationChain(self.estimate_chain).estimate(task_context)

    def get_skill_descriptor(self, task_type) -> SkillDescriptor:
        return self.skill_descriptors[task_type]

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
