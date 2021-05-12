import math
from enum import Enum
from collections.abc import Iterable

from .mission.ihtn import Task

class POI:
    def __init__(self, label):
        self.label = label

class Capability:
    class Property:
        def __init__(self, key: str, value, u: str=None, *kwargs):
            self.key = key
            self.value = value
            self.u = u
    
    def __init__(self, **kwargs):
        self.properties = []
        for key, value in kwargs.items():
            params = None
            if key == 'u': continue
            if kwargs['u'] is not None:
                params = {'u': kwargs['u']}
            self.properties.append(Capability.Property(key=key, value = value, **params))


class Worker:
    """
    Entities that can realize tasks on missions. 
    Minimal representation or robots for realizing the task allocation. 
    Snapshot view for realizing a short living evaluation
    """
    def __init__(self, position=None, capabilities = [], skills = []):
        self.position = position
        self.skills = skills
        self.properties_register = {}
        for capability in capabilities:
            self.register(capability)

    def get(self, prop):
        return self.properties_register[prop]

    def register(self, capability: Capability):
        for prop in capability.properties:
            self.properties_register[prop.key]=prop.value

def worker_factory(position, capabilities, skills):
    # TODO check if have the required capabilities
    unit = Worker(position=position, capabilities=capabilities, skills=skills)
    return unit

class Request:
    counter = 0
    @staticmethod
    def __gen_id():
        identifier = Request.counter
        Request.counter += 1
        return identifier

    def __init__(self, task: Task, timestamp: int):
        self.task, self.timestamp = task, timestamp
        self.id = Request.__gen_id()

class Estimate:
    def __init__(self, task=None, time=math.inf, energy=math.inf):
        self.is_impossible_to_estimate = False
        self.task = task
        self.time = time
        self.energy = energy

class ImpossibleToEstimate(Estimate):
    def __init__(self, reason:str, ):
        super().__init__(time = math.inf, energy = math.inf)
        self.reason = reason
        self.is_impossible_to_estimate = True
            
class LocalMission:
    class Status(Enum):
        PENDING_ASSIGNMENTS = 1
        PENDING_COMMIT = 2
        ASSIGNED = 3
        CONCLUDED = 4

    def __init__(self, local_plan:Task, role, global_mission, worker = None):
        self.plan: Task = local_plan
        self.role = role
        self.global_mission = global_mission
        self.worker: Worker = worker
        self.status = LocalMission.Status.PENDING_ASSIGNMENTS
        

class MissionContext:
    class Status(Enum):
        NEW = 0
        PENDING_ASSIGNMENTS = 1
        DISTRIBUTING_TASKS = 2
        EXECUTING = 3
        CONCLUDED = 4
        REPLANNING_PENDING = 5

    def __init__(self, global_plan: Task = None):
        self.status = MissionContext.Status.NEW
        self.global_plan: Task = global_plan
        self.local_missions: Iterable[LocalMission] = {}
        self.occurances = []
    

            

    
