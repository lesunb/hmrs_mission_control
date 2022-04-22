# -*- coding: utf-8 -*-
from .ihtn import (AbstractTask, Assignment, ElementaryTask, Method, Role,
                   TaskState, TaskStatus, TaskFailure, MethodOrdering, SyncTask)
from .ihtn_algorithms import (count_elementary_tasks, eliminate_left_task,
                              flat_plan, ihtn_aggregate, transverse_ihtn,
                              transverse_ihtn_apply_for_task)
from .restrictions import (POI, Battery, BatteryTimeConstantDischarge,
                           Capability, Estimate, InviableEstimate,
                           LocalMission, MissionContext, MissionStatus, Task,
                           Worker, MissionState, is_failed, is_success)

__all__ = [
    Task, TaskStatus, ElementaryTask,AbstractTask, TaskState, Method,
    MethodOrdering, SyncTask, TaskFailure,
    Assignment,
    MissionStatus,
    Capability,
    Battery,
    BatteryTimeConstantDischarge,
    LocalMission,
    MissionContext,
    Role,
    Worker,
    POI,
    Estimate, InviableEstimate,
    eliminate_left_task, count_elementary_tasks, flat_plan, 
    ihtn_aggregate, transverse_ihtn_apply_for_task, transverse_ihtn,
    MissionState, is_failed, is_success
    ]


# def _import_all_modules():
#     """ Dynamically imports all modules in this package. """
#     import traceback
#     import os
#     global __all__
#     __all__ = []
#     globals_, locals_ = globals(), locals()

#     # Dynamically import all the package modules in this file's directory.
#     for filename in os.listdir(__name__):
#         # Process all python files in directory that don't start
#         # with underscore (which also prevents this module from
#         # importing itself).
#         if filename[0] != '_' and filename.split('.')[-1] in ('py', 'pyw'):
#             modulename = filename.split('.')[0]  # Filename sans extension.
#             package_module = '.'.join([__name__, modulename])
#             try:
#                 module = __import__(package_module, globals_, locals_, [modulename])
#             except:
#                 traceback.print_exc()
#                 raise
#             for name in module.__dict__:
#                 if not name.startswith('_'):
#                     globals_[name] = module.__dict__[name]
#                     __all__.append(name)

# _import_all_modules()
