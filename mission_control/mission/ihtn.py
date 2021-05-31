from abc import abstractmethod
from enum import Enum
from copy import copy
from collections.abc import Sequence
from typing import List 

class MethodOrdering(Enum):
    SEQUENTIAL= 0
    NON_ORDERED = 1

class Task:
    id = 0
    def __init__(self, **kwargs):
        self.id = Task.id
        Task.id += 1
        self.assign_to = None
        self.attributes = kwargs
        self.__dict__.update(kwargs)


    @abstractmethod
    def clone():
        pass


class ElementaryTask(Task):
    def __init__(self, type, **kwargs):
        self.type = type
        self.name = None
        super().__init__(**kwargs)
        self._attrs = list(filter(lambda a: not a.startswith('__'), dir(self)))
    
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
        str_ = str(list(map( lambda k:(k,getattr(self, k)), self._attrs)))
        hashx =  hash(str_)
        return hashx


class SyncTask(Task):
    class SyncType(Enum):
        WAIT_MESSAGE = 'wait_message'
        SEND_MESSAGE = 'send_message'
    def __init__(self, type: SyncType, to = None, from_=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.name = type
        self.to = to
        self.from_ = from_
 
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







