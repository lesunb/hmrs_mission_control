from enum import Enum

from ..data_model import (ElementaryTask, LocalMission, MissionContext, Task,
                          TaskState, TaskStatus, flat_plan)


class MissionRepairStatus(Enum):
    class RepairType:
        def __init__(self, label, should_reasign=False):
            self.label, self.should_reasign = label, should_reasign

    WAITING = RepairType('PLAN_ADAPTED')
    PLAN_ADAPTED = RepairType('PLAN_ADAPTED')
    REASSIGN = RepairType('REASIGN', should_reasign=True)
    CANT_REPAIR = None


class RepairPlanner:
    def try_local_repair(self, local_mission: LocalMission) -> MissionRepairStatus:
        pass

    def try_global_repair(self, global_mission: MissionContext) -> MissionRepairStatus:
        pass

    def reset_task_states(self, plan: Task):
        to_reset = filter(lambda task: not task.state.is_in(TaskStatus.IN_PROGRESS, 
                                                            TaskStatus.NOT_ASSIGNED),
                         flat_plan(plan))
        def reset_task(task: ElementaryTask):
            return TaskState(task=task, progress=0, status=TaskStatus.IN_PROGRESS)
        return map(reset_task, to_reset)



class MissionRepairPlannerRegister:
    def __init__(self, *mission_type_planner):
        self.descs = {}
        for pair in mission_type_planner:
            self.descs[pair[0]] = pair[1]
    
    def register(self, task_type, descriptor: RepairPlanner):
        self.descs[task_type] = descriptor

    def get(self, type) -> RepairPlanner:
        return self.descs.get(type)
        
