from mission_control.sequencing.skill_implementation import SkillImplementation

from mission_control.mission.ihtn import ElementaryTask

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

