from abc import abstractmethod

from typing import List

from ..data_model.ihtn import ElementaryTask
from ..data_model.restrictions import Worker, Estimate


from .component_model_interfaces import TaskContext, SkillDescriptor

def create_context_gen(worker: Worker, task_list: List[ElementaryTask]):
    task_context = TaskContext(worker=worker)
    task_context.start()

    for task in task_list:
        new_task_context = task_context.unwind(task)
        yield new_task_context
        task_context = new_task_context
    return

class SkillDescriptorRegister:
    def __init__(self, *task_type_skill_desc_pairs):
        self.descs = {pair[0]: pair[1] for pair in task_type_skill_desc_pairs}
    
    def register(self, task_type, descriptor: SkillDescriptor):
        self.descs[task_type] = descriptor

    def get(self, type) -> SkillDescriptor:
        return self.descs[type]
