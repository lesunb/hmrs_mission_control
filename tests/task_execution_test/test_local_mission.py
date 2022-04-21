
from mission_control.execution.sequencing import LocalMissionController, TickStatus

from ..world_collector import *

def test_local_mission_empty_plan():
    lm_ctrl = LocalMissionController(local_plan= None)
    assert lm_ctrl.has_no_plan()


def test_local_mission_has_plan(ihtn_collect):
    lm_ctrl = LocalMissionController(local_plan= ihtn_collect)
    assert not lm_ctrl.has_no_plan()


def test_local_mission_get_first_task(ihtn_collect, collection_ihtn):
    lm_ctrl = LocalMissionController(local_plan= ihtn_collect)
    task = lm_ctrl.next_task()
    assert collection_ihtn.navto_room3.value == task

def test_local_mission_get_second_task(ihtn_collect, collection_ihtn):
    lm_ctrl = LocalMissionController(local_plan= ihtn_collect)
    task = lm_ctrl.next_task()
    tick = TickStatus(status = TickStatus.Type.COMPLETED_WITH_SUC, task=task)
    lm_ctrl.update(tick)
    second_task = lm_ctrl.next_task()
    assert collection_ihtn.pick_up_object.value == second_task

