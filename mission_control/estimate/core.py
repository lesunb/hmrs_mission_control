from abc import abstractmethod


from mission_control.mission.ihtn import ElementaryTask



class TaskContext:
    def unwind(post_conditions):
        """ create a clone of current context and apply the post condition """
        pass

class Estimate:
    def __init__(self, tasks, time, energy):
        pass


class TaskStatusUpdate:
    pass


class Bid:
    def __init__(self, individual_plan, worker):
        self.time_individual_tasks = None
        self.power_consumption_individual_tasks = None

    def is_power_viable(self):
        pass
    
    def get_time_indivual_tasks(self):
        pass



def evaluate_assignment(mission_context, assignment):
    pass


class SkillDescriptor():
    def __init__(self, environment_descriptors):
        self.ed = environment_descriptors

    def getED(type_) -> EnvironmentDescriptor :
        ed = self.ed.get(type_)
        if ed is None:
            raise f'ev {type_} not found'
        else:
            return ed

    @abstractmethod
    def estimate(task_context: TaskContext) -> Estimate:
        pass


class EnvironmentDescriptor:
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def get(parametes):
        pass


class EnvironmentDescriptorManager:
    @abstractmethod
    def get(self, type, **parametes):
        pass
