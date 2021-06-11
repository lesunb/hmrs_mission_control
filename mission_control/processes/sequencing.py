from abc import abstractmethod
from copy import Error
from enum import Enum
from mission_control.mission.ihtn import AbstractTask, ElementaryTask
from ..core import Task
from mission_control.mission.planning import flat_plan
from mission_control.mission.execution import eliminate_left_task, get_first_task

class TickStatus:
    class Type(Enum):
        FATAL_FAILURE = 0
        IN_PROGRESS = 1
        SUCCESS_END = 2
    
    def __init__(self, status: Type, task: Task):
        self.status, self.task = status, task
    

class SkillImplementation:
    
    def __init__(self):
        self.is_loaded = False
        self.task = None

    @abstractmethod
    def on_load(self):
        """ 
        On start
        """
        pass
    
    @abstractmethod
    def on_complete(self):
        pass

    @abstractmethod
    def on_tick(self) -> TickStatus:
        pass
    
    def load(self, task: Task):
        self.on_load(task)
        self.is_loaded = True

    def tick(self) -> TickStatus:
        if not self.is_loaded:
            return #TODO return state loading
        return self.on_tick()

    def complete(self):
        self.on_complete()

class SkillLibrary:
    def __init__(self):
        self.skills_map = {}

    def query(self, task: ElementaryTask) -> SkillImplementation:
        ref = self.skills_map[task.type]
        if ref is None:
            raise Exception(f'no skill implementation for <{task.type}> found on library' )
        return ref()

    def add(self, task_type, skill_impl: SkillImplementation):
        self.skills_map[task_type] = skill_impl


class ActiveSkillController:
    """ 
    Active Skill Subsystem
    """
    def __init__(self):
        self.active_skill = None

    def load(self, skill: SkillImplementation, task: Task):
        """
        Load a new skill
        """
        self.active_skill = skill
        skill.load(task)

    def is_idle(self):
        """  
        Is idle if there is no active skill
        """
        return self.active_skill is None

    def tick(self) -> TickStatus:
        """
        Tick the active skill
        """
        tick_result = self.active_skill.tick()
        if tick_result.status == TickStatus.Type.SUCCESS_END:
            self.active_skill.complete()
            self.active_skill = None

        return tick_result

class LocalMissionController:
    class Status(Enum):
        NO_PLAN = 0
        IN_PROGRESS = 1
        CONCLUDED_WIH_SUCCESS = 2
        FATAL_FAILURE = 3

    def __init__(self, local_plan: Task):
        self.initial_plan = local_plan
        self.curr_plan = local_plan
        self._curr_task: Task = None
        self.concluded_curr_plan_tasks = 0
        if local_plan is not None:
            self.status = LocalMissionController.Status.IN_PROGRESS
        else:
            self.status = LocalMissionController.Status.NO_PLAN

    def has_no_plan(self):
        return self.curr_plan is None

    def update(self, tick_status: TickStatus) -> TickStatus:
        """
        Update curr plan with tick status
        """
        if tick_status.status is TickStatus.Type.SUCCESS_END: # task ended
            self.curr_plan = eliminate_left_task(tick_status.task, self.curr_plan)
            self._curr_task: Task = None
            self.concluded_curr_plan_tasks += 1
            if self.curr_plan is None:
                self.status = LocalMissionController.Status.CONCLUDED_WIH_SUCCESS
        #TODO task in progress

        #TODO failure

        #TODO send status

    def next_task(self):
        if self._curr_task is None:
            curr_task = self.get_next_task()
            self._curr_task = curr_task
            return curr_task
        else:
            raise Exception(f'trying to get a next task in a plan, while there is a task in progress {self._curr_task}')

    def get_next_task(self):
        return get_first_task(self.curr_plan)



    def get_task_status(self):
        pass


class TaskStatus:
    def set_value(self, value):
        pass

class SequencingProcess:
    def __init__(self, skill_library: SkillLibrary):
        self.skill_library = skill_library

    
    def run(self, local_mission: LocalMissionController, active_skill_ctrl: ActiveSkillController, task_status: TaskStatus):
        if local_mission.has_no_plan():
            # nothing to do
            return
        
        if active_skill_ctrl.is_idle():
            # load new task
            next_task = local_mission.next_task()
            skill_impl = self.skill_library.query(next_task)
            active_skill_ctrl.load(skill_impl, next_task)
            
        tick_status = active_skill_ctrl.tick()
        local_mission.update(tick_status)
        task_status.set_value(local_mission.get_task_status())


