from copy import deepcopy
from mission_control.utils.contants import ConstantsProvider
from mission_control.deeco_integration.simulation.formatters import CoalitionFormationLogger
from mission_control.utils import ContextualLogger, LogFormatterManager
import pytest
from enum import Enum
from typing import List

from lagom.container import Container

from mission_control.utils import Timer
from mission_control.deeco_integration.deeco_timer import DeecoTimer

from mission_control.estimating import SkillDescriptorRegister, EnergyEstimatorConstantDischarge, EstimatingManager, Estimator, PLAN_MINIMUM_TARGET_BATTERTY_CHARGE_CONST, TimeEstimator
from mission_control.common_descriptors.generic_constant_cost_sd import generic_skill_descriptor_constant_cost_factory
from mission_control.common_descriptors.navigation_sd import NavigationSkillDescriptor
from mission_control.common_descriptors.routes_ed import Map, RoutesEnvironmentDescriptor

from hospital_world.hospital_map import create_hospital_scenario_map

from mission_control.data_model import POI, WorldModelDomain
from mission_control.coordination.coalition_formation import CoalitionFormationProcess

from mission_control.data_model.ihtn import SyncTask

class Defs(object):
    def __iter__(self):
        for attr in [attr for attr in dir(self) \
            if not callable(getattr(self, attr)) and not attr.startswith("__")]:
            yield getattr(self, attr)
    def all(self):
        return list(self)
    
    def all_but(self, *exclusion):
        return list( set(self.all()) - set(exclusion))


class task_type(Defs):
    NAV_TO = 'navigation'
    APPROACH_PERSON = 'approach_person'
    AUTHENTICATE_PERSON = 'authenticate_person'
    OPERATE_DRAWER = 'operate_drawer'
    APPROACH_ROBOT = 'approach_robot'
    PICK_UP = 'pick_up'
    DEPOSIT = 'deposit'
    MANIPULATE_DOOR = 'manipulate_door'
    APPROACH_OBJECT = 'approach_object'
    
all_skills = task_type().all()
carry_robot_skills = task_type().all_but(task_type.PICK_UP, task_type.DEPOSIT)

class poi(Enum):
    respiratory_control = POI("Respiratory Control")
    ic_corridor = POI("IC Corridor")
    pc_corridor = POI("PC Corridor")
    ic_room_1 = POI("IC Room 1")
    ic_room_2 = POI("IC Room 2")
    ic_room_3 = POI("IC Room 3")
    ic_room_4 = POI("IC Room 4")
    ic_room_5 = POI("IC Room 5")
    ic_room_6 = POI("IC Room 6")
    pc_room_1 = POI("PC Room 1")
    pc_room_2 = POI("PC Room 2")
    pc_room_3 = POI("PC Room 3")
    pc_room_4 = POI("PC Room 4")
    pc_room_5 = POI("PC Room 5")
    pc_room_6 = POI("PC Room 6")
    pc_room_7 = POI("PC Room 7")
    pc_room_8 = POI("PC Room 8")
    pc_room_9 = POI("PC Room 9")
    pc_room_10 = POI("PC Room 10")
    reception = POI("Reception")
    lab_corridor = POI("Laboratory Corridor")
    laboratory = POI("Laboratory")

all_rooms = [ poi_.value for poi_ in [ poi.ic_room_1, poi.ic_room_2, poi.ic_room_3, poi.ic_room_4, 
              poi.ic_room_5, poi.ic_room_6, poi.pc_room_1, poi.pc_room_2, 
              poi.pc_room_3, poi.pc_room_4, poi.pc_room_5, poi.pc_room_6, 
              poi.pc_room_7, poi.pc_room_8, poi.pc_room_9, poi.pc_room_10 ]]

near_ic_pc_rooms = [ poi_.value for poi_ in [   
              poi.ic_room_2, poi.ic_room_3, poi.ic_room_4, poi.ic_room_5, poi.ic_room_6,
              poi.pc_room_3, poi.pc_room_4, poi.pc_room_5, poi.pc_room_6, 
              poi.pc_room_7, poi.pc_room_8]]

# Defined as Enum so we can reference methods and tasks, and we can have references
# to names that we later on set on them with set_name()

##
# Map
hospital_map = create_hospital_scenario_map()
def get_position_of_poi(poi: POI):
    return tuple(hospital_map.get_node(poi.label).coords)

######
# Container, and processes
########

container = Container()
# env desc
container[Map] = hospital_map = create_hospital_scenario_map()

routes_ed = container[RoutesEnvironmentDescriptor]

nav_sd = container[NavigationSkillDescriptor]

# constant estimatives
approach_person_time = 2
authenticate_person_time = 2
operate_drawer_time = 2
approach_robot_time = 2
pick_up_time = 2
deposit_time = 2
send_message_time = 2
wait_message_time = 2
manipulate_door_time = 2
approach_object_time = 2

cp = ConstantsProvider()
container[ConstantsProvider] = cp
cp.set(PLAN_MINIMUM_TARGET_BATTERTY_CHARGE_CONST, 0.08)

# skill desc
nav_sd = container[NavigationSkillDescriptor]
approach_person_sd = generic_skill_descriptor_constant_cost_factory('approach_person', approach_person_time)
authenticate_person_sd = generic_skill_descriptor_constant_cost_factory('authenticate_person', authenticate_person_time)
operate_drawer_sd = generic_skill_descriptor_constant_cost_factory('operate_drawer', operate_drawer_time)
approach_robot_sd = generic_skill_descriptor_constant_cost_factory('approach_robot', approach_robot_time)
pick_up_sd = generic_skill_descriptor_constant_cost_factory('pick_up', pick_up_time)
deposit_sd = generic_skill_descriptor_constant_cost_factory('deposit', deposit_time)
manipulate_door_sd = generic_skill_descriptor_constant_cost_factory('manipulate_door', manipulate_door_time)
approach_object_sd = generic_skill_descriptor_constant_cost_factory('approach_object', approach_object_time)


send_message_sd = generic_skill_descriptor_constant_cost_factory('send_message', send_message_time)
wait_message_sd = generic_skill_descriptor_constant_cost_factory('wait_message', wait_message_time)



sync_type_SEND_MESSAGE = SyncTask.SyncType.SEND_MESSAGE.value
sync_type_WAIT_MESSAGE = SyncTask.SyncType.WAIT_MESSAGE.value
# skill desc container singleton
sd_register = SkillDescriptorRegister( 
        (task_type.NAV_TO, nav_sd), 
        (task_type.APPROACH_PERSON, approach_person_sd),
        (task_type.AUTHENTICATE_PERSON, authenticate_person_sd),
        (task_type.OPERATE_DRAWER, operate_drawer_sd),
        (task_type.APPROACH_ROBOT, approach_robot_sd),
        (task_type.PICK_UP, pick_up_sd),
        (task_type.DEPOSIT, deposit_sd),
        (task_type.MANIPULATE_DOOR, manipulate_door_sd),
        (task_type.APPROACH_OBJECT, approach_object_sd),
        (sync_type_SEND_MESSAGE, send_message_sd),
        (sync_type_WAIT_MESSAGE, wait_message_sd)
    )

container[SkillDescriptorRegister] = sd_register
container[Timer] = DeecoTimer()


lfm = container[LogFormatterManager]
container[LogFormatterManager] = lfm
CoalitionFormationLogger.register(lfm)

container[ContextualLogger] = container[ContextualLogger]
# estimate manager
# estimate manager
time_estimator = container[TimeEstimator]
energy_estimator = container[EnergyEstimatorConstantDischarge]
container[List[Estimator]] = [time_estimator, energy_estimator]

em: EstimatingManager = container[EstimatingManager]
cf_process: CoalitionFormationProcess = container[CoalitionFormationProcess]


class HospitalWorldModelDomain(WorldModelDomain):
    def __init__(self):
        super().__init__('hospital_world')
        self.register(lambda location: hospital_map.get_node(location), 'location')
        self.register_collection(all_skills, 'task_type')

world_model_domain = container[HospitalWorldModelDomain]
container[WorldModelDomain] = world_model_domain