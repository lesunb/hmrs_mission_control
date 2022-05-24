from __future__ import annotations
from collections.abc import Sequence

from abc import abstractmethod
from copy import copy
from enum import Enum
from typing import List

from ..utils.to_string import obj_to_string


class Role:
    class Type(str, Enum):
        MANAGED= 'MANAGED'
        NOT_MANAGED= 'NOT_MANAGED'

    def __init__(self, label, type = Type.MANAGED):
        self.label, self.type = label, type

class MethodOrdering(Enum):
    SEQUENTIAL= 0
    NON_ORDERED = 1

class Assignment:
    def __init__(self, estimate=None, plan=None):
        self.estimate, self.plan = estimate, plan

class Task:
    id = 0
    def __init__(self, **kwargs):
        self.id = Task.id
        Task.id += 1
        self.assign_to: List[Role] = None
        self.assignment = Assignment()
        self.state: TaskState = TaskState()
        self.attributes = kwargs
        self.__dict__.update(kwargs)
        
    @abstractmethod
    def clone():
        pass
    
    def __str__(self) -> str:
        return obj_to_string(self)

    def __hash__(self):
        return hash(self.__str__())


class TaskStatus(str, Enum):
    NOT_ASSIGNED = 'NOT_ASSIGNED'
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    PLAN_RECOVERY = 'PLAN_RECOVERY'
    COMPLETED_WITH_SUC = 'COMPLETED_WITH_SUC'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'


class TaskState:
    def __init__(self, status: TaskStatus = TaskStatus.NOT_ASSIGNED, progress: float = 0.0, task: Task = None):
        self.status, self.progress, self.task = status, progress, task
        if status == TaskStatus.COMPLETED_WITH_SUC:
            progress = 1 # 100%

    def is_status(self, status: TaskState):
        return self.status == status
    
    def is_in(self, *statuses) -> bool:
        return self.status in statuses

class TaskFailure(TaskState):
    def __init__(self, task: Task, failure_type = 'UnknownFailure', more_info=None):
        super().__init__(status=TaskStatus.FAILED, progress=None, task=task)
        self.failure_type, self.more_info = failure_type, more_info

class ElementaryTask(Task):
    def __init__(self, type, **kwargs):
        self.type = type
        self.name = None
        super().__init__(**kwargs)
        self._attrs = list(filter(lambda a: not a.startswith('__') and not callable(getattr(self, a)), dir(self)))
    
    def clone(self):
        cpy = copy(self)
        return cpy
    
    def __eq__(self, other):
        if isinstance(other, ElementaryTask):
            if self.id == other.id:
                for key in self._attrs:
                    if getattr(other, key) != getattr(other, key):
                        return False
                return True
        return False

    def __hash__(self):
        return super().__hash__()
        # str_ = obj_to_string(self.__str__())
        # return hash(str_)

class SyncTask(Task):
    class SyncType(Enum):
        WAIT_MESSAGE = 'wait_message'
        SEND_MESSAGE = 'send_message'
    def __init__(self, type: SyncType, to_role = None, from_role = None, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.to_role = to_role
        self.from_role = from_role
 
    def clone(self):
        return copy(self)

class Method:
    def __init__(self, subtasks: List[Task] =[], order = MethodOrdering.SEQUENTIAL):
        self.order: MethodOrdering = order
        self.subtasks = subtasks
    
    def clone(self):
        new_ = copy(self)
        new_.subtasks = list(map(lambda st:st.clone(), self.subtasks))
        return new_

class AbstractTask(Task):
    def __init__(self, methods: List[Method] =[], **kwargs):
        super().__init__(**kwargs)
        self.methods = methods
        self.selected_method: Method = methods[0]
        self.assign_to = get_children_assignment(methods)

    def clone(self):
        new_ = copy(self)
        new_.selected_method = self.selected_method.clone()
        new_.methods = list(map( lambda m: m.clone(), self.methods))
        return new_

def get_children_assignment(methods: List[ Method ]):

    def _seq_but_not_str(obj):
        return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray))

    assingments = set()
    for method in methods:
        for task in method.subtasks:
            if isinstance(task, ElementaryTask):
                if task.assign_to is None:
                    print(f'elementary task {task} has no assignment')
                    continue
                elif _seq_but_not_str(task.assign_to):
                    assingments.update(task.assign_to)
                else:
                    assingments.add(task.assign_to)
            elif isinstance(task,AbstractTask):
                assingments.update(get_children_assignment(task.methods))
    return assingments

