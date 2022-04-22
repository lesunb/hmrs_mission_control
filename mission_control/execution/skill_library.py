from ..data_model import ElementaryTask
from .component_model_interfaces import SkillImplementation


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
