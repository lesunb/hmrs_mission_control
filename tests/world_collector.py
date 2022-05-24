from copy import deepcopy
from enum import Enum
from typing import List

import pytest
from lagom import Container
from mission_control.common_descriptors.generic_constant_cost_sd import \
    generic_skill_descriptor_constant_cost_factory
from mission_control.common_descriptors.navigation_sd import (
    Move, NavigationSkillDescriptor)
from mission_control.common_descriptors.routes_ed import (
    Map, Nodes, RoutesEnvironmentDescriptor)
from mission_control.coordination import (CoalitionFormationProcess,
                                          MissionHandler,
                                          MissionRepairPlannerRegister,
                                          MissionRepairStatus, RepairPlanner)
from mission_control.data_model import (POI, AbstractTask, Battery,
                                        BatteryTimeConstantDischarge,
                                        ElementaryTask, LocalMission, Method,
                                        MissionContext, Role, Task, TaskState,
                                        Worker)
from mission_control.estimating import (EnergyEstimatorConstantDischarge,
                                        EstimatingManager, Estimator,
                                        SkillDescriptorRegister, TimeEstimator)
from mission_control.execution import (SkillImplementation, SkillLibrary,
                                       TickStatus)

from mission_control.deeco_integration import CoalitionFormationLogger
from mission_control.utils import ContextualLogger, LogFormatterManager

###
# Produces:
#  - a simple mission with two tasks
#  - three robots
#  - a EnstimateManager
#  - 

##
class task_type(Enum):
    NAV_TO = 'navigation'
    PICK_UP = 'pick_up'

class poi(Enum):
    sr = POI('storage_room')
    room1 = POI('room1')
    room3 = POI('room3')

def create_map() -> Map:
    map = Map()
    ic_corridor = Nodes("IC Corridor", [-37, 15])

    sr = Nodes("storage_room", [-37, 35])
    ic_room_1 = Nodes("room1", [-38, 35])
    ic_room_2 = Nodes("room2", [-34, 35])
    ic_room_3 = Nodes("room3", [-38, 23])

    ic_corridor.add_edges([sr, ic_room_1, ic_room_2, ic_room_3])
    
    sr.add_edges([ic_corridor])
    ic_room_1.add_edges([ic_corridor])
    ic_room_2.add_edges([ic_corridor])
    ic_room_3.add_edges([ic_corridor])

    map.add_nodes([ic_corridor, sr, ic_room_1, ic_room_2,
                   ic_room_3])
    return map

for enum_item in poi:
    setattr(enum_item.value, 'name', enum_item.name)

role_r1 = Role('r1')

class robot(Enum):
    a = Worker(location = poi.sr.value, 
        capabilities=[
            Move(avg_speed = 10, u='m/s')
        ],
        resources=[
            BatteryTimeConstantDischarge(
                battery= Battery(capacity=1, charge=0.20), 
                discharge_rate=0.0001, minimum_useful_level=0.05)
        ],
        skills=[task_type.NAV_TO.value, task_type.PICK_UP.value])
    b = Worker(location = poi.room1.value, 
        capabilities=[
            Move(avg_speed = 15, u='m/s')
        ],
        resources=[
            BatteryTimeConstantDischarge(
                battery= Battery(capacity=1, charge=0.20), 
                discharge_rate=0.0001, minimum_useful_level=0.05)
        ],
        skills=[task_type.NAV_TO.value, task_type.PICK_UP.value])
    c = Worker(location = poi.room1.value, 
        capabilities=[
            Move(avg_speed = 20, u='m/s')
        ],
        resources=[
            BatteryTimeConstantDischarge(
                battery= Battery(capacity=1, charge=0.20), 
                discharge_rate=0.0001, minimum_useful_level=0.05)
        ],
        skills=[task_type.NAV_TO.value])
    d = Worker(location = poi.room1.value,
        capabilities=[
            Move(avg_speed = 25, u='m/s')
        ],
        resources=[
            BatteryTimeConstantDischarge(
                battery= Battery(capacity=1, charge=0.20),
                discharge_rate=0.02, minimum_useful_level=0.05)
        ],
        skills=[task_type.NAV_TO.value, task_type.PICK_UP.value])

for enum_item in robot:
    setattr(enum_item.value, 'name', enum_item.name)
robots = [ unit.value for unit in robot ]

# Defined as Enum so we can reference methods and tasks, and we can have references
# to names that we later on set on them with set_name()
class _collection_ihtn(Enum):
    # elementary tasks
    navto_room3 = ElementaryTask(task_type.NAV_TO.value, destination=poi.room3.value, assign_to=[role_r1])
    pick_up_object  = ElementaryTask(task_type.PICK_UP.value, target=role_r1, assign_to=[role_r1])
    m_collect = Method(subtasks=[navto_room3, pick_up_object])

    # root task
    collect = AbstractTask(methods=[m_collect])

collection_mission_type = 'collection_mission'


def collector_ihtn_plan_repair(ihtn: Task, task_state: TaskState):
    return ihtn if task_state.task == _collection_ihtn.navto_room3.value else False



for enum_item in _collection_ihtn:
    setattr(enum_item.value, 'name', enum_item.name)

@pytest.fixture
def collection_ihtn():
    return deepcopy(_collection_ihtn)

@pytest.fixture
def ihtn_collect():
    return deepcopy(_collection_ihtn.collect.value.clone())

@pytest.fixture
def r1():
    return role_r1

@pytest.fixture
def collection_robots():
    return robots

@pytest.fixture
def collection_robots_a_b_and_d():
    return [ enum_item.value for enum_item in [robot.a, robot.b, robot.d]]


######
# Container, and processes
########

container = Container()
# env desc
container[Map] = create_map()
routes_ed = container[RoutesEnvironmentDescriptor]

# skill desc
nav_sd = container[NavigationSkillDescriptor]
pick_up_sd = generic_skill_descriptor_constant_cost_factory('pick_up', 10)

# skill desc container singleton
sd_register = SkillDescriptorRegister( (task_type.NAV_TO.value, nav_sd), (task_type.PICK_UP.value, pick_up_sd))
container[SkillDescriptorRegister] = sd_register


# logs

lfm = container[LogFormatterManager]
container[LogFormatterManager] = lfm
CoalitionFormationLogger.register(lfm)
container[ContextualLogger] = container[ContextualLogger]
# end logs


# estimate manager
container[List[Worker]] = robots
time_estimator = container[TimeEstimator]
energy_estimator = container[EnergyEstimatorConstantDischarge]
container[List[Estimator]] = [time_estimator, energy_estimator]

em:EstimatingManager = container[EstimatingManager]
cfp: CoalitionFormationProcess = container[CoalitionFormationProcess]
######
# Robots
########

@pytest.fixture
def cf_process():
    return cfp

@pytest.fixture
def estimate_manager():
    return em

@pytest.fixture
def routes_envdesc():
    return routes_ed


###
# Execution
###
class OneTickSkill(SkillImplementation):
    task = None
    def on_load(self, task):
        self.tick_count = 0
        self.task = task
        print(task)

    def on_tick(self):
        if self.tick_count != 0:
            return TickStatus(status=TickStatus.Type.COMPLETED_WITH_SUC, task=self.task)
        self.tick_count = 1
        return TickStatus(status=TickStatus.Type.IN_PROGRESS, task=self.task)

    def on_complete(self):
        print('task completed')

collector_skill_library = SkillLibrary()
collector_skill_library.add(task_type.NAV_TO.value, OneTickSkill)
collector_skill_library.add(task_type.PICK_UP.value, OneTickSkill)


class MissionHandlerMock(MissionHandler):
    def start_mission(*params):
        pass

@pytest.fixture
def collection_mission():
    mission_context = MissionContext(request_id=0, global_plan = deepcopy(_collection_ihtn.collect.value.clone()), mission_type=collection_mission_type)
    cfp.do_run(mission_context, robots, MissionHandlerMock())
    robot_b = robots[1] # robot B that is the fastest that have the skills
    return {"mission": mission_context, 'robot': robot_b}


class CollectorMissionRepair(RepairPlanner):
    def try_local_repair(self, local_mission: LocalMission) -> MissionRepairStatus:
        if local_mission.failure.task == _collection_ihtn.navto_room3.value:
            local_mission.worker = None
            local_mission.assignment_status = LocalMission.AssignmentStatus.NOT_ASSIGNED
            task_states = self.reset_task_states(local_mission.plan)
            return MissionRepairStatus.REASSIGN, task_states
        else:
            return MissionRepairStatus.CANT_REPAIR, None

    def try_global_repair(self, global_mission: MissionContext) -> MissionRepairStatus:
        return MissionRepairStatus.CANT_REPAIR



    def try_handle_failure(self, failure):
        can_be_reasigned = self.can_be_reasigned(failure)
        should_reasign = can_be_reasigned and \
                (self.is_fatal(failure) or self.better_reasign(failure))

        soluction = None
        if should_reasign:
            soluction = self.reasign(failure)
        
        if not soluction:
            self.notify_not_recoverable_failure(failure, soluction)

@pytest.fixture
def collector_mission_repair_register():
    cm_repair = CollectorMissionRepair()
    repair_planner_register = MissionRepairPlannerRegister()
    repair_planner_register.register(collection_mission_type, cm_repair)
    return repair_planner_register
