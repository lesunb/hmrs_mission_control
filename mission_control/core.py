from deeco.core import Identifiable
import math


from enum import Enum
from typing import List

import json

from .mission.ihtn import Task, TaskStatus


class Role:
    class Type(str, Enum):
        MANAGED= 'MANAGED'
        NOT_MANAGED= 'NOT_MANAGED'

    def __init__(self, label, type = Type.MANAGED):
        self.label, self.type = label, type

    def __str__(self):
        return json.dumps(self.__dict__)

class POI:
    def __init__(self, label):
        self.label = label
    
    def __str__(self):
        return self.label

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


class EnergyResource:
    pass

class BatteryTimeConstantDischarge(EnergyResource):
    def __init__(self, battery, discharge_rate, minimum_useful_level):
        self.battery, self.discharge_rate, self.minimum_useful_level = battery, discharge_rate, minimum_useful_level

class Battery:
    def __init__(self, capacity=1, charge=1, minimum_useful_level=0.05):
        self.capacity, self.charge, self.minimum_useful_level = capacity, charge, minimum_useful_level

class Worker(Identifiable):
    """
    Entities that can realize tasks on missions. 
    Minimal representation or robots for realizing the task allocation. 
    Snapshot view for realizing a short living evaluation
    """
    def __init__(self, uuid=None, name=None, location=None, capabilities = [], skills = [], resources = []):
        super().__init__(uuid)
        self.name, self.location, self.skills, self.resources = name, location, skills, resources
        self.properties_register = {}
        for capability in capabilities:
            self.register(capability)

    def get(self, prop):
        return self.properties_register[prop]
    
    def get_resource(self, resource_cls):
        for res in self.resources:
            if isinstance(res, resource_cls):
                return res
        return None

    def register(self, capability: Capability):
        for prop in capability.properties:
            setattr(self, prop.key, prop.value)
            self.properties_register[prop.key]=prop.value

def worker_factory(location, capabilities, skills):
    # TODO check if have the required capabilities
    unit = Worker(location=location, capabilities=capabilities, skills=skills)
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
    def __init__(self, time=math.inf, energy=math.inf, progress: float=0.0):
        self.is_inviable = False
        self.time, self.energy, self.progress = time, energy, progress

class InviableEstimate(Estimate):
    def __init__(self, reason:str):
        super().__init__(time = math.inf, energy = math.inf)
        self.reason = reason
        self.is_inviable = True
            
class LocalMission:
    class AssignmentStatus(Enum):
        NOT_MANAGED = 0
        NOT_ASSIGNED = 1
        ASSIGNED = 2
        

    def __init__(self, local_plan: Task, role, global_mission, worker = None):
        self.plan: Task = local_plan
        self.role = role
        self.global_mission = global_mission
        self.worker: Worker = worker
        self.assignment_status: self.AssignmentStatus = LocalMission.AssignmentStatus.NOT_ASSIGNED
        
    
    def is_status(self, status: TaskStatus):
        return self.plan.state.is_status(status)

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
        self.local_missions: List[LocalMission] = []
        self.occurances = []
    

class MissionStatus:
    def __init__(self, time_remaining):
        self.time_remaining = time_remaining

    
