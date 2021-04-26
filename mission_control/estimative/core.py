from abc import abstractmethod


from mission_control.mission.ihtn import ElementaryTask


class EnvironmentDescriptorManager:
    @abstractmethod
    def get(self, type, **parametes):
        pass

class TaskContext:
    def unwind(post_conditions):
        """ create a clone of current context and apply the post condition """
        pass

class Estimative:
    def __init__(self, time, energy):
        pass


class EnvironmentDescriptor:
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def get(parametes):
        pass


class SkillDescriptor():
    @abstractmethod
    def bind(self, environment_descriptors):
        pass

    @abstractmethod
    def estimate(task: ElementaryTask, task_context: TaskContext) -> Estimative:
        pass

class TaskStatusUpdate:
    pass

class PowerComponent:
    def __init__(self, power_source: PowerSource, power_consumption_model:PowerConsumptionModel): 
        self.power_source = power_source
        self.power_consumption_model = power_consumption_model


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

