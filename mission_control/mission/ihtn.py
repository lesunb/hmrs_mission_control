
from enum import Enum
from collections.abc import Sequence 

class MethodOrdering(Enum):
    SEQUENTIAL= 0
    NON_ORDERED = 1

class Method:
    def __init__(self, tasks=[], order = MethodOrdering.SEQUENTIAL):
        self.order = order
        self.tasks = tasks

class Task:
    def __init__(self, **kwargs):
        self.assign_to = None
        self.attributes = kwargs
        self.__dict__.update(kwargs)

class ConcreteTask(Task):
    def __init__(self, type, **kwargs):
        super().__init__(**kwargs)
        self.type = type

def get_children_assignment(methods: [ Method ]):

    def _seq_but_not_str(obj):
        return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray))

    assingments = set()
    for method in methods:
        for task in method.tasks:
            if isinstance(task, ConcreteTask):
                if task.assign_to is None:
                    print(f'concrete task {task} has no assignment')
                    continue
                elif _seq_but_not_str(task.assign_to):
                    assingments.update(task.assign_to)
                else:
                    assingments.add(task.assign_to)
            elif isinstance(task,AbstractTask):
                assingments.update(get_children_assignment(task.methods))
    return assingments

class AbstractTask(Task):
    def __init__(self, methods=[], **kwargs):
        super().__init__(**kwargs)
        self.methods = methods
        self.selected_method = methods[0]
        self.assign_to = get_children_assignment(methods)




